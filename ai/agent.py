import os
import requests
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv
load_dotenv()  

# 1. TOOL DEFINITION
def get_weather(city: str) -> dict:
    """Fetch current weather for a city. Input: city name (str). Output: dict with temp (F), condition (e.g., 'Rain')."""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise ValueError("OpenWeather API key not set.")
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=imperial"
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Weather API error: {response.text}")
    
    data = response.json()
    return {
        "temperature": data["main"]["temp"],
        "condition": data["weather"][0]["main"]
    }

def evaluate_conditions(activity: str, weather: dict) -> str:
    """Evaluate if weather is good for an activity. Input: activity (str), weather (dict from get_weather). Output: str recommendation."""
    temp = weather.get("temperature", 0)
    condition = weather.get("condition", "Unknown")
    
    return f"{activity}: {condition} and {temp}°F."

# 2. DIRECT OLLAMA CONFIGURATION
# We still use the LiteLlm class because it's the ADK's 
# generic bridge for local models.
model_config = LiteLlm(
    model="ollama_chat/qwen3:4b", 
    api_base="http://localhost:11434",
    stream=True
)

# 3. AGENT DEFINITION
root_agent = Agent(
    model=model_config,
    name='weather_agent',
    description='A helpful assistant for user questions about weather.',
    instruction='''You are a Weather Advisor AI. For queries like "Is it good for [activity] in [city]?", 
    reason step-by-step: 
    1. Extract city and activity.
    2. Use get_weather tool to fetch data.
    3. Use evaluate_conditions tool to decide.
    4. Summarize the recommendation.
    Only use tools when needed. If no city/activity, ask for clarification.''',
    tools=[get_weather, evaluate_conditions]
)

if __name__ == "__main__":
    # Test call
    print("Agent is thinking...")
    response = root_agent.run("What is the weather in New York?")
    print(f"Agent: {response.text}")
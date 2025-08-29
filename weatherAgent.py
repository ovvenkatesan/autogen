import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os
from pyowm import OWM
from pyowm.utils import config

load_dotenv()

# Get API keys
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
owm_api_key = os.getenv("OPENWEATHERMAP_API_KEY")

# Initialize OpenWeatherMap
owm = OWM(owm_api_key)
weather_mgr = owm.weather_manager()

def get_weather_info(city_name, country_code="US"):
    """Get current weather information for a city"""
    try:
        # Get weather observation
        observation = weather_mgr.weather_at_place(f'{city_name},{country_code}')
        weather = observation.weather
        
        # Extract weather details
        temp_celsius = weather.temperature('celsius')
        temp_fahrenheit = weather.temperature('fahrenheit')
        
        weather_info = {
            "city": city_name,
            "temperature_celsius": round(temp_celsius['temp'], 1),
            "temperature_fahrenheit": round(temp_fahrenheit['temp'], 1),
            "feels_like_celsius": round(temp_celsius['feels_like'], 1),
            "feels_like_fahrenheit": round(temp_fahrenheit['feels_like'], 1),
            "humidity": weather.humidity,
            "description": weather.detailed_status,
            "wind_speed": round(weather.wind()['speed'], 1),
            "pressure": weather.pressure['press'],
            "visibility": weather.visibility_distance if weather.visibility_distance else "N/A",
            "sunrise": weather.sunrise_time(timeformat='iso'),
            "sunset": weather.sunset_time(timeformat='iso')
        }
        
        return weather_info
    except Exception as e:
        return {"error": f"Could not get weather for {city_name}: {str(e)}"}

# Create the weather-aware assistant agent
oper_router_client = OpenAIChatCompletionClient(
    api_key=openrouter_api_key, 
    model="deepseek/deepseek-chat-v3.1", 
    base_url="https://openrouter.ai/api/v1", 
    model_info={
        "family": "deepseek",
        "provider": "openrouter/openrouter",
        "type": "chat",
        "vision": True,
        "function_calling": True,
        "json_output": True,
        "structured_output": True,
        "context_length": 8192,
        "max_tokens": 4096,
        "supported_features": ["chat", "vision", "function_calling"]
    }
)

weather_agent = AssistantAgent(
    model_client=oper_router_client, 
    name="WeatherAgent", 
    system_message="""You are a helpful AI Agent Assistant with access to real-time weather information. 
    You can provide current weather data for any city when users ask about weather conditions.
    Always be friendly and provide weather information in a clear, easy-to-understand format."""
)

async def chat_with_weather(question):
    """Chat with the weather agent"""
    # If the question is about weather, get the data first
    if any(word in question.lower() for word in ['weather', 'temperature', 'forecast', 'climate']):
        # Extract city name (simple extraction - you could make this more sophisticated)
        words = question.split()
        city_name = None
        
        # Look for common city indicators
        for i, word in enumerate(words):
            if word.lower() in ['in', 'at', 'for', 'of'] and i + 1 < len(words):
                city_name = words[i + 1].replace('?', '').replace('.', '').replace(',', '')
                break
        
        if city_name:
            weather_data = get_weather_info(city_name)
            if "error" not in weather_data:
                enhanced_question = f"{question}\n\nHere's the current weather data for {city_name}:\n{weather_data}"
                result = await weather_agent.run(task=enhanced_question)
            else:
                result = await weather_agent.run(task=f"{question}\n\nNote: {weather_data['error']}")
        else:
            result = await weather_agent.run(task=question)
    else:
        result = await weather_agent.run(task=question)
    
    print(result.messages[-1].content)

if __name__ == "__main__":
    # Test weather functionality
    print("Testing weather functionality...")
    weather_data = get_weather_info("Chennai")
    if "error" not in weather_data:
        print("Weather data retrieved successfully!")
        print(f"Temperature in {weather_data['city']}: {weather_data['temperature_celsius']}°C")
    else:
        print(f"Weather error: {weather_data['error']}")
    
    print("\n" + "="*50)
    print("Chat with Weather Agent:")
    print("="*50)
    
    # Start the chat
    asyncio.run(chat_with_weather("What's the weather like in Chennai?"))

import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
model_client = OpenAIChatCompletionClient(api_key=api_key, model="gpt-4o-mini")

owm = OWM('OPENWEATHERMAP_API_KEY')
weather_mgr = owm.weather_manager()

def getWeather(city: str) -> str:
    observation = weather_mgr.weather_at_place('Chennai,IN')
    weather = observation.weather
    return f"Temperature: {weather.temperature('celsius')['temp']}°C"

def addNumbers(a: int, b: int) -> str:
    return f"The sum of {a} and {b} is {a + b}"

assistant = AssistantAgent(
    model_client=model_client,
    name="my_assistant",
    system_message="You are a helpful assistant that can answer questions and help with tasks.",
    description="Agent that tells you a joke",
    tools=[getWeather, addNumbers])

async def main():
    result = await assistant.run(task="What is the weather in Chennai?")
    print(result.messages[-1].content)
    result = await assistant.run(task="What is the sum of 2 and 3?")
    print(result.messages[-1].content)
    

asyncio.run(main())


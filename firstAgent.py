import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
model_client = OpenAIChatCompletionClient(api_key=api_key, model="gpt-4o-mini")
assistant = AssistantAgent(model_client=model_client, name="my_assistant")


async def main():
    result = await assistant.run(task="tell me joke?")
    print(result.messages[-1].content)

asyncio.run(main())


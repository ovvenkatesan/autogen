import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage, MultiModalMessage
from autogen_core import Image as AGImage
from PIL import Image
from io import BytesIO
import requests

from dotenv import load_dotenv
import os
import uuid
from datetime import datetime, timezone

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
model_client = OpenAIChatCompletionClient(api_key=api_key, model="gpt-4o-mini")

assistant = AssistantAgent(
    model_client=model_client, 
    name="my_assistant", 
    system_message="You are a helpful assistant that can answer questions and help with tasks.")

async def text_task():
    text_message = TextMessage(content="get me the weather in Chennai?", source="user")
    result = await assistant.run(task=text_message)
    print(result.messages[-1].content)

async def image_task():
    response = requests.get("https://picsum.photos/id/237/200/300")
    image = Image.open(BytesIO(response.content))
    ag_image = AGImage(image)

    multimodal_message = MultiModalMessage(content=["What is in this image?", ag_image], source="user")
    result = await assistant.run(task=multimodal_message)
    print(result.messages[-1].content)

asyncio.run(image_task())
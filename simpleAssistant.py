import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

oper_router_client = OpenAIChatCompletionClient(api_key=api_key, model="deepseek/deepseek-chat-v3.1", base_url="https://openrouter.ai/api/v1", model_info={
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
})

router_agent = AssistantAgent(model_client=oper_router_client, name="HelpfulAgent", system_message="You are helpful AI Agent Assistant")

async def chat(question):
    result = await router_agent.run(task=question)
    print(result.messages[-1].content)

asyncio.run(chat("What is the capital of France?"))
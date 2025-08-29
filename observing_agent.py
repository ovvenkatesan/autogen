import asyncio
import time
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from autogen_agentchat.ui import Console

from dotenv import load_dotenv
import os
import uuid
from datetime import datetime, timezone

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
model_client = OpenAIChatCompletionClient(api_key=api_key, model="gpt-4o-mini")

async def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny"

assistant = AssistantAgent(
    model_client=model_client, 
    name="my_assistant", 
    tools=[get_weather],
    system_message="You are a helpful assistant that can answer questions and help with tasks.")

def print_statistics(start_time, end_time, events, response_type):
    """Print comprehensive statistics"""
    duration = end_time - start_time
    
    print(f"\n📊 {response_type} Statistics:")
    print("=" * 50)
    print(f"⏱️  Total Time: {duration:.3f} seconds")
    
    # Count different event types
    event_counts = {}
    total_tokens = 0
    
    for event in events:
        event_type = type(event).__name__
        event_counts[event_type] = event_counts.get(event_type, 0) + 1
        
        # Extract token usage if available
        if hasattr(event, 'models_usage') and event.models_usage:
            if hasattr(event.models_usage, 'prompt_tokens'):
                total_tokens += event.models_usage.prompt_tokens or 0
            if hasattr(event.models_usage, 'completion_tokens'):
                total_tokens += event.models_usage.completion_tokens or 0
    
    print(f"🔢 Total Events: {len(events)}")
    print(f"🧮 Event Breakdown:")
    for event_type, count in event_counts.items():
        print(f"   - {event_type}: {count}")
    
    print(f"🔤 Total Tokens: {total_tokens}")
    print(f"⚡ Average Time per Event: {duration/len(events):.3f}s" if events else "N/A")
    print("=" * 50)

async def assistant_task():
    """Test basic message handling with statistics"""
    print("📝 Testing Basic Message Handling...")
    
    start_time = time.time()
    
    response = await assistant.on_messages(
        messages=[TextMessage(
            id=str(uuid.uuid4()),
            content="get me the weather in Chennai?",
            source="user",
            type="TextMessage",
            created_at=datetime.now(timezone.utc),
            models_usage=None,
            metadata={}
        )],
        cancellation_token=CancellationToken()
    )
    
    end_time = time.time()
    
    print("Response inner messages:")
    print(response.inner_messages)
    print('\n' + '='*50 + '\n')
    print("Response chat message:")
    print(response.chat_message)
    
    # Print statistics
    print_statistics(start_time, end_time, response.inner_messages, "Basic Message Handling")

async def assistant_task_with_streaming():
    """Test streaming message handling with Console and statistics"""
    print("🔄 Testing Streaming Message Handling...")
    
    # Create proper TextMessage
    text_message = TextMessage(
        id=str(uuid.uuid4()),
        content="get me the weather in Chennai?",
        source="user",
        type="TextMessage",
        created_at=datetime.now(timezone.utc),
        models_usage=None,
        metadata={}
    )
    
    start_time = time.time()
    events = []
    
    # Custom event collector for streaming
    async def collect_events():
        nonlocal events
        stream = assistant.on_messages_stream(
            messages=[text_message],
            cancellation_token=CancellationToken()
        )
        async for event in stream:
            events.append(event)
            # Still show real-time events
            print(f"🔄 Event: {type(event).__name__}")
            if hasattr(event, 'content'):
                print(f"   Content: {event.content}")
    
    # Use Console without unsupported parameters
    await Console(
        assistant.on_messages_stream(
            messages=[text_message],
            cancellation_token=CancellationToken()
        )
    )
    
    # Collect events separately for statistics
    await collect_events()
    
    end_time = time.time()
    
    # Print streaming statistics
    print_statistics(start_time, end_time, events, "Streaming Message Handling")

async def detailed_streaming_analysis():
    """Detailed analysis of streaming with token tracking"""
    print("\n🔍 Detailed Streaming Analysis...")
    
    text_message = TextMessage(
        id=str(uuid.uuid4()),
        content="get me the weather in Chennai?",
        source="user",
        type="TextMessage",
        created_at=datetime.now(timezone.utc),
        models_usage=None,
        metadata={}
    )
    
    start_time = time.time()
    events = []
    token_usage = {"prompt": 0, "completion": 0}
    
    async def detailed_collector():
        nonlocal events, token_usage
        stream = assistant.on_messages_stream(
            messages=[text_message],
            cancellation_token=CancellationToken()
        )
        async for event in stream:
            events.append(event)
            
            # Track token usage
            if hasattr(event, 'models_usage') and event.models_usage:
                if hasattr(event.models_usage, 'prompt_tokens') and event.models_usage.prompt_tokens:
                    token_usage["prompt"] += event.models_usage.prompt_tokens
                if hasattr(event.models_usage, 'completion_tokens') and event.models_usage.completion_tokens:
                    token_usage["completion"] += event.models_usage.completion_tokens
            
            # Show detailed event info
            print(f"\n📋 Event: {type(event).__name__}")
            print(f"   Source: {getattr(event, 'source', 'N/A')}")
            print(f"   Created: {getattr(event, 'created_at', 'N/A')}")
            if hasattr(event, 'content'):
                print(f"   Content: {event.content}")
            if hasattr(event, 'models_usage') and event.models_usage:
                usage = event.models_usage
                print(f"   Tokens: {getattr(usage, 'prompt_tokens', 0)} prompt + {getattr(usage, 'completion_tokens', 0)} completion")
    
    await Console(
        assistant.on_messages_stream(
            messages=[text_message],
            cancellation_token=CancellationToken()
        )
    )
    
    # Collect events separately for statistics
    await detailed_collector()
    
    end_time = time.time()
    
    # Print detailed statistics
    print(f"\n📊 Detailed Streaming Analysis Statistics:")
    print("=" * 60)
    print(f"⏱️  Total Time: {end_time - start_time:.3f} seconds")
    print(f"🔢 Total Events: {len(events)}")
    print(f"🔤 Token Usage:")
    print(f"   - Prompt Tokens: {token_usage['prompt']}")
    print(f"   - Completion Tokens: {token_usage['completion']}")
    print(f"   - Total Tokens: {token_usage['prompt'] + token_usage['completion']}")
    print(f"⚡ Events per Second: {len(events)/(end_time - start_time):.2f}")
    print("=" * 60)

async def main():
    print("🤖 Observing Agent Demo with Comprehensive Statistics")
    print("=" * 70)
    
    # Test basic functionality first
    await assistant_task()
    
    print("\n" + "=" * 70)
    print("🔄 Now testing streaming...")
    
    # Test streaming functionality
    await assistant_task_with_streaming()
    
    print("\n" + "=" * 70)
    print("🔍 Now testing detailed streaming analysis...")
    
    # Test detailed streaming analysis
    await detailed_streaming_analysis()

if __name__ == "__main__":
    asyncio.run(main())
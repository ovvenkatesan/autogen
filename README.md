# AutoGen Project

This project demonstrates the use of Microsoft's AutoGen framework for creating AI agents that can interact with each other and perform various tasks.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables:**
   Create a `.env` file in the project root with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   OPENWEATHERMAP_API_KEY=your_openweathermap_api_key_here
   ```

## Files

- **`firstAgent.py`** - Simple OpenAI-based assistant agent
- **`simpleAssistant.py`** - OpenRouter-based assistant agent using DeepSeek model
- **`agent_with_tools.py`** - Multi-functional agent with weather, math, and time tools using direct OpenWeatherMap API
- **`simpleWeather.py`** - Standalone weather examples using pyowm library
- **`test_weather_api.py`** - Direct OpenWeatherMap API testing
- **`firstAgent.ipynb`** - Jupyter notebook version of the OpenAI agent

## Usage

### OpenAI Agent
```bash
python firstAgent.py
```

### OpenRouter Agent (DeepSeek)
```bash
python simpleAssistant.py
```

### Multi-Tool Agent with Weather
```bash
python agent_with_tools.py
```

### Test Weather API Directly
```bash
python test_weather_api.py
```

### Jupyter Notebook
Open `firstAgent.ipynb` in Jupyter or VS Code to run the OpenAI agent interactively.

## Features

- **OpenAI Integration**: Uses GPT-4o-mini for natural language processing
- **OpenRouter Integration**: Access to various AI models through OpenRouter
- **Direct Weather API**: Implements OpenWeatherMap API calls directly using the endpoint: `https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}`
- **Agent Communication**: Demonstrates how agents can interact and respond to user queries
- **Multi-Tool Support**: Weather, mathematical calculations, and current time functionality
- **Environment-based Configuration**: Secure API key management using environment variables

## Weather API Implementation

The `agent_with_tools.py` implements the OpenWeatherMap API directly using:

1. **Weather by Coordinates**: 
   ```
   https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric
   ```

2. **Weather by City**: Uses geocoding API first, then weather API
   ```
   http://api.openweathermap.org/geo/1.0/direct?q={city},{country}&limit=1&appid={API_KEY}
   ```

3. **Available Weather Data**:
   - Temperature (°C)
   - Feels like temperature
   - Humidity (%)
   - Pressure (hPa)
   - Weather conditions
   - Wind speed (m/s)
   - Visibility (m)

## Requirements

- Python 3.8+
- autogen-agentchat
- autogen-ext[openai]
- python-dotenv
- aiohttp (for HTTP API calls)
- pyowm (for alternative weather library)
- Valid API keys for OpenAI, OpenRouter, and OpenWeatherMap 

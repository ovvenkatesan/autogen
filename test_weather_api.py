import asyncio
import aiohttp
from dotenv import load_dotenv
import os

load_dotenv()

async def test_weather_api():
    """Test the OpenWeatherMap API directly"""
    
    # Get API key
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    
    if not api_key:
        print("❌ Error: OPENWEATHERMAP_API_KEY not found in .env file")
        print("Please add your OpenWeatherMap API key to the .env file:")
        print("OPENWEATHERMAP_API_KEY=your_api_key_here")
        return
    
    print("🌤️ Testing OpenWeatherMap API Direct Calls")
    print("=" * 50)
    
    # Test 1: Weather by coordinates (as per your example)
    print("\n1️⃣ Weather by Coordinates (44.34, 10.99):")
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat=44.34&lon=10.99&appid={api_key}&units=metric"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    print(f"   📍 Location: {data['name']}, {data['sys']['country']}")
                    print(f"   🌡️ Temperature: {data['main']['temp']}°C")
                    print(f"   💨 Feels like: {data['main']['feels_like']}°C")
                    print(f"   💧 Humidity: {data['main']['humidity']}%")
                    print(f"   📊 Pressure: {data['main']['pressure']} hPa")
                    print(f"   ☁️ Conditions: {data['weather'][0]['description']}")
                    print(f"   🌪️ Wind Speed: {data['wind']['speed']} m/s")
                    print(f"   👁️ Visibility: {data.get('visibility', 'N/A')} m")
                else:
                    print(f"   ❌ Error: HTTP {response.status}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Test 2: Weather by city name
    print("\n2️⃣ Weather by City (London, GB):")
    try:
        # First get coordinates
        geocode_url = f"http://api.openweathermap.org/geo/1.0/direct?q=London,GB&limit=1&appid={api_key}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(geocode_url) as response:
                if response.status == 200:
                    geocode_data = await response.json()
                    
                    if geocode_data:
                        lat = geocode_data[0]['lat']
                        lon = geocode_data[0]['lon']
                        
                        print(f"   📍 Coordinates: {lat}, {lon}")
                        
                        # Now get weather
                        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
                        
                        async with session.get(weather_url) as weather_response:
                            if weather_response.status == 200:
                                weather_data = await weather_response.json()
                                
                                print(f"   🌡️ Temperature: {weather_data['main']['temp']}°C")
                                print(f"   💨 Feels like: {weather_data['main']['feels_like']}°C")
                                print(f"   💧 Humidity: {weather_data['main']['humidity']}%")
                                print(f"   ☁️ Conditions: {weather_data['weather'][0]['description']}")
                            else:
                                print(f"   ❌ Weather API Error: HTTP {weather_response.status}")
                    else:
                        print("   ❌ City not found")
                else:
                    print(f"   ❌ Geocoding Error: HTTP {response.status}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Test 3: Raw API response for debugging
    print("\n3️⃣ Raw API Response (First 200 chars):")
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat=44.34&lon=10.99&appid={api_key}&units=metric"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    raw_response = str(data)[:200] + "..." if len(str(data)) > 200 else str(data)
                    print(f"   📄 Response: {raw_response}")
                else:
                    print(f"   ❌ Error: HTTP {response.status}")
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_weather_api())

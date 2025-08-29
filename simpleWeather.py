from pyowm import OWM
from pyowm.utils import config
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def get_weather_examples():
    """Demonstrate various pyowm features"""
    
    # Get your OpenWeatherMap API key from environment
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    
    if not api_key:
        print("❌ Error: OPENWEATHERMAP_API_KEY not found in .env file")
        print("Please add your OpenWeatherMap API key to the .env file:")
        print("OPENWEATHERMAP_API_KEY=your_api_key_here")
        return
    
    # Initialize OWM
    owm = OWM(api_key)
    mgr = owm.weather_manager()
    
    print("🌤️  OpenWeatherMap API Examples")
    print("=" * 50)
    
    # Example 1: Current weather for a city
    print("\n1️⃣  Current Weather for London:")
    try:
        observation = mgr.weather_at_place('London,GB')
        weather = observation.weather
        
        print(f"   📍 Location: {observation.location.name}, {observation.location.country}")
        print(f"   🌡️  Temperature: {weather.temperature('celsius')['temp']:.1f}°C")
        print(f"   💨 Wind: {weather.wind()['speed']:.1f} m/s")
        print(f"   💧 Humidity: {weather.humidity}%")
        print(f"   📊 Pressure: {weather.pressure['press']} hPa")
        print(f"   👁️  Visibility: {weather.visibility_distance if weather.visibility_distance else 'N/A'} m")
        print(f"   ☁️  Status: {weather.detailed_status}")
        print(f"   🌅 Sunrise: {weather.sunrise_time(timeformat='iso')}")
        print(f"   🌇 Sunset: {weather.sunset_time(timeformat='iso')}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Example 2: Weather forecast
    print("\n2️⃣  3-Day Forecast for New York:")
    try:
        forecaster = mgr.forecast_at_place('New York,US', '3h')
        forecast = forecaster.forecast
        
        for i, weather in enumerate(forecast[:8]):  # Show first 8 periods (24 hours)
            time = weather.reference_time('iso')
            temp = weather.temperature('celsius')['temp']
            status = weather.detailed_status
            print(f"   {time}: {temp:.1f}°C - {status}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Example 3: Weather at coordinates
    print("\n3️⃣  Weather at Coordinates (Tokyo area):")
    try:
        # Tokyo coordinates: 35.6762° N, 139.6503° E
        observation = mgr.weather_at_coords(35.6762, 139.6503)
        weather = observation.weather
        
        print(f"   📍 Coordinates: 35.6762°N, 139.6503°E")
        print(f"   🌡️  Temperature: {weather.temperature('celsius')['temp']:.1f}°C")
        print(f"   💨 Wind: {weather.wind()['speed']:.1f} m/s")
        print(f"   💧 Humidity: {weather.humidity}%")
        print(f"   ☁️  Status: {weather.detailed_status}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Example 4: Search for cities
    print("\n4️⃣  City Search Results for 'Paris':")
    try:
        cities = mgr.weather_at_places('Paris', 'like', limit=3)
        for i, city in enumerate(cities):
            print(f"   {i+1}. {city.location.name}, {city.location.country}")
            print(f"      Temperature: {city.weather.temperature('celsius')['temp']:.1f}°C")
            print(f"      Status: {city.weather.detailed_status}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def get_weather_for_city(city_name, country_code="US"):
    """Get weather for a specific city"""
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    
    if not api_key:
        print("❌ Error: OPENWEATHERMAP_API_KEY not found in .env file")
        return
    
    owm = OWM(api_key)
    mgr = owm.weather_manager()
    
    try:
        observation = mgr.weather_at_place(f'{city_name},{country_code}')
        weather = observation.weather
        
        print(f"\n🌤️  Weather in {city_name}, {country_code}")
        print("=" * 40)
        print(f"🌡️  Temperature: {weather.temperature('celsius')['temp']:.1f}°C")
        print(f"   Feels like: {weather.temperature('celsius')['feels_like']:.1f}°C")
        print(f"💨 Wind Speed: {weather.wind()['speed']:.1f} m/s")
        print(f"💧 Humidity: {weather.humidity}%")
        print(f"📊 Pressure: {weather.pressure['press']} hPa")
        print(f"👁️  Visibility: {weather.visibility_distance if weather.visibility_distance else 'N/A'} m")
        print(f"☁️  Conditions: {weather.detailed_status}")
        print(f"🌅 Sunrise: {weather.sunrise_time(timeformat='iso')}")
        print(f"🌇 Sunset: {weather.sunset_time(timeformat='iso')}")
        
    except Exception as e:
        print(f"❌ Error getting weather for {city_name}: {e}")

if __name__ == "__main__":
    # Show examples
    get_weather_examples()
    
    # Interactive weather lookup
    print("\n" + "=" * 50)
    print("🔍 Interactive Weather Lookup")
    print("=" * 50)
    
    city = input("Enter a city name (or press Enter to skip): ").strip()
    if city:
        country = input("Enter country code (e.g., US, GB, FR) or press Enter for US: ").strip() or "US"
        get_weather_for_city(city, country)

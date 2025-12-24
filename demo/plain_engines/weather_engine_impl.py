"""
Weather Engine Implementation Demo
Shows how to use the Weather Engine to analyze track conditions
"""
import asyncio
import sys
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from engines.shared_services_fastf1 import WeatherService
from engines.weather_engine.schemas import WeatherRequest


async def demo_weather_analysis():
    """Demonstrate Weather Engine capabilities"""
    print("="*70)
    print("WEATHER ENGINE - Track Conditions Analysis Demo")
    print("="*70)
    
    # Example 1: Stable conditions (Bahrain)
    print("\n🌤️  Example 1: Bahrain 2024 Race - Stable Conditions")
    print("-"*70)
    
    request = WeatherRequest(
        year=2024,
        gp="Bahrain",
        session="R"
    )
    
    result = await WeatherService.analyze_weather(request)
    print(json.dumps(result.dict(), indent=2, default=str))
    
    # Example 2: Hot conditions (Singapore)
    print("\n\n🌤️  Example 2: Singapore 2023 - Hot & Humid")
    print("-"*70)
    
    request2 = WeatherRequest(
        year=2023,
        gp="Singapore",
        session="R"
    )
    
    result2 = await WeatherService.analyze_weather(request2)
    print(json.dumps(result2.dict(), indent=2, default=str))
    
    # Example 3: Variable conditions (Spa)
    print("\n\n🌤️  Example 3: Spa 2023 - Variable Weather")
    print("-"*70)
    
    request3 = WeatherRequest(
        year=2023,
        gp="Spa",
        session="R"
    )
    
    result3 = await WeatherService.analyze_weather(request3)
    print(json.dumps(result3.dict(), indent=2, default=str))
    
    print("\n" + "="*70)
    print("✅ Weather Engine Demo Complete")
    print("="*70)


if __name__ == "__main__":
    asyncio.run(demo_weather_analysis())

"""
Car Engine Implementation Demo
Shows how to use the Car Engine to analyze vehicle performance
"""
import asyncio
import sys
import json 
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from engines.car_engine.service import CarService
from engines.car_engine.schemas import CarRequest


async def demo_car_analysis():
    """Demonstrate Car Engine capabilities"""
    print("="*70)
    print("CAR ENGINE - Vehicle Performance Demo")
    print("="*70)
    
    # Example 1: Analyze all cars in Bahrain
    print("\n🏎️  Example 1: Bahrain 2024 Race - All Cars")
    print("-"*70)
    
    request = CarRequest(
        year=2024,
        gp="Bahrain",
        session="R"
    )
    
    result = await CarService.analyze_car_performance(request)
    print(json.dumps(result.model_dump(), indent=2, default=str))
    
    # Example 2: Specific driver analysis
    print("\n\n🏎️  Example 2: Red Bull (Driver #1) Analysis")
    print("-"*70)
    
    request2 = CarRequest(
        year=2024,
        gp="Bahrain",
        session="R",
        driver_number=1  # Verstappen
    )
    
    result2 = await CarService.analyze_car_performance(request2)
    print(json.dumps(result2.model_dump(), indent=2, default=str))
    
    # Example 3: Qualifying vs Race comparison
    print("\n\n🏎️  Example 3: Qualifying Performance")
    print("-"*70)
    
    request3 = CarRequest(
        year=2024,
        gp="Monaco",
        session="Q"
    )
    
    result3 = await CarService.analyze_car_performance(request3)
    print(json.dumps(result3.model_dump(), indent=2, default=str))
    
    print("\n" + "="*70)
    print("✅ Car Engine Demo Complete")
    print("="*70)


if __name__ == "__main__":
    asyncio.run(demo_car_analysis())

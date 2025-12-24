"""
Safety Car Engine Implementation Demo
Shows how to use the Safety Car Engine to analyze race interruptions
"""
import asyncio
import sys
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from engines.shared_services_fastf1 import SafetyCarService
from engines.safetycar_engine.schemas import SafetyCarRequest


async def demo_safety_car_analysis():
    """Demonstrate Safety Car Engine capabilities"""
    print("="*70)
    print("SAFETY CAR ENGINE - Race Interruption Analysis Demo")
    print("="*70)
    
    # Example 1: Race with Safety Car
    print("\n🚨 Example 1: Bahrain 2024 Race - Safety Car Analysis")
    print("-"*70)
    
    request = SafetyCarRequest(
        year=2024,
        gp="Bahrain",
        session="R"
    )
    
    result = await SafetyCarService.analyze_safety_car(request)
    print(json.dumps(result.dict(), indent=2, default=str))
    
    # Example 2: Monaco - High SC probability
    print("\n\n🚨 Example 2: Monaco 2023 - High SC Probability")
    print("-"*70)
    
    request2 = SafetyCarRequest(
        year=2023,
        gp="Monaco",
        session="R"
    )
    
    result2 = await SafetyCarService.analyze_safety_car(request2)
    print(json.dumps(result2.dict(), indent=2, default=str))
    
    # Example 3: Clean race (Spa)
    print("\n\n🚨 Example 3: Spa 2023 - Minimal Interruptions")
    print("-"*70)
    
    request3 = SafetyCarRequest(
        year=2023,
        gp="Spa",
        session="R"
    )
    
    result3 = await SafetyCarService.analyze_safety_car(request3)
    print(json.dumps(result3.dict(), indent=2, default=str))
    
    print("\n" + "="*70)
    print("✅ Safety Car Engine Demo Complete")
    print("="*70)


if __name__ == "__main__":
    asyncio.run(demo_safety_car_analysis())

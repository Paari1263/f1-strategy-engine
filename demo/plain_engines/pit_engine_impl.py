"""
Pit Engine Implementation Demo
Shows how to use the Pit Engine to analyze pit stop strategies
"""
import asyncio
import sys
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from engines.shared_services_fastf1 import PitService
from engines.pit_engine.schemas import PitRequest


async def demo_pit_analysis():
    """Demonstrate Pit Engine capabilities"""
    print("="*70)
    print("PIT ENGINE - Pit Stop Strategy Analysis Demo")
    print("="*70)
    
    # Example 1: Full race pit analysis
    print("\n🔧 Example 1: Bahrain 2024 Race - All Pit Stops")
    print("-"*70)
    
    request = PitRequest(
        year=2024,
        gp="Bahrain",
        session="R"
    )
    
    result = await PitService.analyze_pit_stops(request)
    print(json.dumps(result.dict(), indent=2, default=str))
    
    # Example 2: Strategy analysis
    print("\n\n🔧 Example 2: Monaco 2023 - Pit Strategy")
    print("-"*70)
    
    request2 = PitRequest(
        year=2023,
        gp="Monaco",
        session="R"
    )
    
    result2 = await PitService.analyze_pit_stops(request2)
    print(json.dumps(result2.dict(), indent=2, default=str))
    
    # Example 3: High-stop strategy (Silverstone)
    print("\n\n🔧 Example 3: Silverstone 2023 - Multi-Stop Strategies")
    print("-"*70)
    
    request3 = PitRequest(
        year=2023,
        gp="Silverstone",
        session="R"
    )
    
    result3 = await PitService.analyze_pit_stops(request3)
    print(json.dumps(result3.dict(), indent=2, default=str))
    
    print("\n" + "="*70)
    print("✅ Pit Engine Demo Complete")
    print("="*70)


if __name__ == "__main__":
    asyncio.run(demo_pit_analysis())

"""
Traffic Engine Implementation Demo
Shows how to use the Traffic Engine to analyze race battles and gaps
"""
import asyncio
import sys
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from engines.shared_services_fastf1 import TrafficService
from engines.traffic_engine.schemas import TrafficRequest


async def demo_traffic_analysis():
    """Demonstrate Traffic Engine capabilities"""
    print("="*70)
    print("TRAFFIC ENGINE - Race Battles & Gaps Analysis Demo")
    print("="*70)
    
    # Example 1: Focus on race leader
    print("\n🚦 Example 1: Bahrain 2024 Race - Leader Analysis")
    print("-"*70)
    
    request = TrafficRequest(
        year=2024,
        gp="Bahrain",
        session="R",
        focus_driver=1  # Verstappen
    )
    
    result = await TrafficService.analyze_traffic(request)
    print(json.dumps(result.dict(), indent=2, default=str))
    
    # Example 2: Midfield battle
    print("\n\n🚦 Example 2: Monaco 2023 - Midfield Traffic")
    print("-"*70)
    
    request2 = TrafficRequest(
        year=2023,
        gp="Monaco",
        session="R",
        focus_driver=55  # Sainz
    )
    
    result2 = await TrafficService.analyze_traffic(request2)
    print(json.dumps(result2.dict(), indent=2, default=str))
    
    # Example 3: Full field analysis
    print("\n\n🚦 Example 3: Silverstone 2023 - Full Field")
    print("-"*70)
    
    request3 = TrafficRequest(
        year=2023,
        gp="Silverstone",
        session="R"
    )
    
    result3 = await TrafficService.analyze_traffic(request3)
    print(json.dumps(result3.dict(), indent=2, default=str))
    
    print("\n" + "="*70)
    print("✅ Traffic Engine Demo Complete")
    print("="*70)


if __name__ == "__main__":
    asyncio.run(demo_traffic_analysis())

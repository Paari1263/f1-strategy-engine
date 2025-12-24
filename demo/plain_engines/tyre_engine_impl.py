"""
Tyre Engine Implementation Demo
Shows how to use the Tyre Engine to analyze compound performance and degradation
"""
import asyncio
import sys
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from engines.shared_services_fastf1 import TyreService
from engines.tyre_engine.schemas import TyreRequest


async def demo_tyre_analysis():
    """Demonstrate Tyre Engine capabilities"""
    print("="*70)
    print("TYRE ENGINE - Compound & Degradation Analysis Demo")
    print("="*70)
    
    # Example 1: Full race tyre analysis
    print("\n🛞 Example 1: Bahrain 2024 Race - Tyre Strategy")
    print("-"*70)
    
    request = TyreRequest(
        year=2024,
        gp="Bahrain",
        session="R"
    )
    
    result = await TyreService.analyze_tyre_performance(request)
    print(json.dumps(result.dict(), indent=2, default=str))
    
    # Example 2: High degradation circuit (Silverstone)
    print("\n\n🛞 Example 2: Silverstone 2023 - High Degradation")
    print("-"*70)
    
    request2 = TyreRequest(
        year=2023,
        gp="Silverstone",
        session="R"
    )
    
    result2 = await TyreService.analyze_tyre_performance(request2)
    print(json.dumps(result2.dict(), indent=2, default=str))
    
    # Example 3: Low degradation circuit (Monaco)
    print("\n\n🛞 Example 3: Monaco 2023 - Low Degradation")
    print("-"*70)
    
    request3 = TyreRequest(
        year=2023,
        gp="Monaco",
        session="R"
    )
    
    result3 = await TyreService.analyze_tyre_performance(request3)
    print(json.dumps(result3.dict(), indent=2, default=str))
    
    print("\n" + "="*70)
    print("✅ Tyre Engine Demo Complete")
    print("="*70)


if __name__ == "__main__":
    asyncio.run(demo_tyre_analysis())

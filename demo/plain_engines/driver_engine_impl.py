"""
Driver Engine Implementation Demo
Shows how to use the Driver Engine to analyze driver performance
"""
import asyncio
import sys
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from engines.shared_services_fastf1 import DriverService
from engines.driver_engine.schemas import DriverRequest


async def demo_driver_analysis():
    """Demonstrate Driver Engine capabilities"""
    print("="*70)
    print("DRIVER ENGINE - Driver Performance Analysis Demo")
    print("="*70)
    
    # Example 1: Full field analysis
    print("\n👤 Example 1: Bahrain 2024 Race - All Drivers")
    print("-"*70)
    
    request = DriverRequest(
        year=2024,
        gp="Bahrain",
        session="R"
    )
    
    result = await DriverService.analyze_driver_performance(request)
    print(json.dumps(result.dict(), indent=2, default=str))
    
    # Example 2: Specific driver deep dive
    print("\n\n👤 Example 2: Verstappen (#1) - Detailed Analysis")
    print("-"*70)
    
    request2 = DriverRequest(
        year=2024,
        gp="Bahrain",
        session="R",
        driver_number=1
    )
    
    result2 = await DriverService.analyze_driver_performance(request2)
    print(json.dumps(result2.dict(), indent=2, default=str))
    
    # Example 3: Teammate comparison
    print("\n\n👤 Example 3: Monaco 2023 - Leclerc Analysis")
    print("-"*70)
    
    request3 = DriverRequest(
        year=2023,
        gp="Monaco",
        session="R",
        driver_number=16
    )
    
    result3 = await DriverService.analyze_driver_performance(request3)
    print(json.dumps(result3.dict(), indent=2, default=str))
    
    print("\n" + "="*70)
    print("✅ Driver Engine Demo Complete")
    print("="*70)


if __name__ == "__main__":
    asyncio.run(demo_driver_analysis())

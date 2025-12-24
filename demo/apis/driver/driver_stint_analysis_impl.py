"""
Driver Stint Analysis API Demo
Detailed analysis of driver performance during specific race stints
"""
import asyncio
import json
import httpx


async def demo_driver_stint_analysis():
    """Demonstrate Driver Stint Analysis API"""
    print("="*80)
    print("DRIVER STINT ANALYSIS API - Demo")
    print("="*80)
    
    base_url = "http://localhost:8001"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Example 1: Verstappen - Bahrain 2024 First Stint
        print("\n🏁 Example 1: VER - Bahrain 2024 Race, Stint 1")
        print("-"*80)
        
        params = {
            "year": 2024,
            "event": "Bahrain",
            "session": "R",
            "driver": "VER",
            "stint": 1
        }
        
        response = await client.get(
            f"{base_url}/api/v1/driver/stint-analysis",
            params=params
        )
        print(json.dumps(response.json(), indent=2, default=str))
        
        # Example 2: Leclerc - Monaco 2023 Second Stint
        print("\n\n🏁 Example 2: LEC - Monaco 2023 Race, Stint 2")
        print("-"*80)
        
        params2 = {
            "year": 2023,
            "event": "Monaco",
            "session": "R",
            "driver": "LEC",
            "stint": 2
        }
        
        response2 = await client.get(
            f"{base_url}/api/v1/driver/stint-analysis",
            params=params2
        )
        print(json.dumps(response2.json(), indent=2, default=str))
        
        # Example 3: Hamilton - Silverstone 2023 Third Stint
        print("\n\n🏁 Example 3: HAM - Silverstone 2023 Race, Stint 3")
        print("-"*80)
        
        params3 = {
            "year": 2023,
            "event": "Silverstone",
            "session": "R",
            "driver": "HAM",
            "stint": 3
        }
        
        response3 = await client.get(
            f"{base_url}/api/v1/driver/stint-analysis",
            params=params3
        )
        print(json.dumps(response3.json(), indent=2, default=str))
    
    print("\n" + "="*80)
    print("✅ Driver Stint Analysis Demo Complete")
    print("="*80)


if __name__ == "__main__":
    asyncio.run(demo_driver_stint_analysis())

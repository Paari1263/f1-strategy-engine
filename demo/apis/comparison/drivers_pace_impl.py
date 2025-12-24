"""
Driver Pace Comparison API Demo
Compares lap time performance and pace between drivers
"""
import asyncio
import json
import httpx


async def demo_driver_pace_comparison():
    """Demonstrate Driver Pace Comparison API"""
    print("="*80)
    print("DRIVER PACE COMPARISON API - Demo")
    print("="*80)
    
    base_url = "http://localhost:8001"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Example 1: Verstappen vs Leclerc - Standard pace
        print("\n⏱️  Example 1: VER vs LEC - Bahrain 2024 Race (Standard)")
        print("-"*80)
        
        params = {
            "year": 2024,
            "event": "Bahrain",
            "session": "R",
            "driver1": "VER",
            "driver2": "LEC",
            "fuel_corrected": False
        }
        
        response = await client.get(
            f"{base_url}/api/v1/compare/drivers/pace",
            params=params
        )
        print(json.dumps(response.json(), indent=2, default=str))
        
        # Example 2: Hamilton vs Russell - Fuel corrected
        print("\n\n⏱️  Example 2: HAM vs RUS - Silverstone 2023 Race (Fuel Corrected)")
        print("-"*80)
        
        params2 = {
            "year": 2023,
            "event": "Silverstone",
            "session": "R",
            "driver1": "HAM",
            "driver2": "RUS",
            "fuel_corrected": True
        }
        
        response2 = await client.get(
            f"{base_url}/api/v1/compare/drivers/pace",
            params=params2
        )
        print(json.dumps(response2.json(), indent=2, default=str))
        
        # Example 3: Norris vs Piastri - Qualifying pace
        print("\n\n⏱️  Example 3: NOR vs PIA - Monaco 2023 Qualifying")
        print("-"*80)
        
        params3 = {
            "year": 2023,
            "event": "Monaco",
            "session": "Q",
            "driver1": "NOR",
            "driver2": "PIA",
            "fuel_corrected": False
        }
        
        response3 = await client.get(
            f"{base_url}/api/v1/compare/drivers/pace",
            params=params3
        )
        print(json.dumps(response3.json(), indent=2, default=str))
    
    print("\n" + "="*80)
    print("✅ Driver Pace Comparison Demo Complete")
    print("="*80)


if __name__ == "__main__":
    asyncio.run(demo_driver_pace_comparison())

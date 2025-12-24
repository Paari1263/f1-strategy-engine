"""
Driver Consistency Comparison API Demo
Compares consistency metrics and lap time variation between drivers
"""
import asyncio
import json
import httpx


async def demo_driver_consistency_comparison():
    """Demonstrate Driver Consistency Comparison API"""
    print("="*80)
    print("DRIVER CONSISTENCY COMPARISON API - Demo")
    print("="*80)
    
    base_url = "http://localhost:8001"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Example 1: Verstappen vs Perez - Race consistency
        print("\n📊 Example 1: VER vs PER - Bahrain 2024 Race")
        print("-"*80)
        
        params = {
            "year": 2024,
            "event": "Bahrain",
            "session": "R",
            "driver1": "VER",
            "driver2": "PER"
        }
        
        response = await client.get(
            f"{base_url}/api/v1/compare/drivers/consistency",
            params=params
        )
        print(json.dumps(response.json(), indent=2, default=str))
        
        # Example 2: Leclerc vs Sainz - Monaco consistency
        print("\n\n📊 Example 2: LEC vs SAI - Monaco 2023 Race")
        print("-"*80)
        
        params2 = {
            "year": 2023,
            "event": "Monaco",
            "session": "R",
            "driver1": "LEC",
            "driver2": "SAI"
        }
        
        response2 = await client.get(
            f"{base_url}/api/v1/compare/drivers/consistency",
            params=params2
        )
        print(json.dumps(response2.json(), indent=2, default=str))
        
        # Example 3: Hamilton vs Russell - Silverstone qualifying
        print("\n\n📊 Example 3: HAM vs RUS - Silverstone 2023 Qualifying")
        print("-"*80)
        
        params3 = {
            "year": 2023,
            "event": "Silverstone",
            "session": "Q",
            "driver1": "HAM",
            "driver2": "RUS"
        }
        
        response3 = await client.get(
            f"{base_url}/api/v1/compare/drivers/consistency",
            params=params3
        )
        print(json.dumps(response3.json(), indent=2, default=str))
    
    print("\n" + "="*80)
    print("✅ Driver Consistency Comparison Demo Complete")
    print("="*80)


if __name__ == "__main__":
    asyncio.run(demo_driver_consistency_comparison())

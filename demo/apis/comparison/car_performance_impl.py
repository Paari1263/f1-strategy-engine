"""
Car Performance Comparison API Demo
Compares overall car performance between two drivers
"""
import asyncio
import json
import httpx


async def demo_car_performance_comparison():
    """Demonstrate Car Performance Comparison API"""
    print("="*80)
    print("CAR PERFORMANCE COMPARISON API - Demo")
    print("="*80)
    
    base_url = "http://localhost:8001"
    
    async with httpx.AsyncClient(timeout=120.0) as client:  # 2 minutes for FastF1 data loading
        # Example 1: Verstappen vs Leclerc - Bahrain 2024
        print("\n🏎️  Example 1: VER vs LEC - Bahrain 2024 Race")
        print("-"*80)
        
        params = {
            "year": 2024,
            "event": "Bahrain",
            "session": "R",
            "driver1": "VER",
            "driver2": "LEC"
        }
        
        response = await client.get(
            f"{base_url}/api/v1/compare/cars/performance",
            params=params
        )
        print(json.dumps(response.json(), indent=2, default=str))
        
        # Example 2: Hamilton vs Russell - Silverstone 2023 Qualifying
        print("\n\n🏎️  Example 2: HAM vs RUS - Silverstone 2023 Qualifying")
        print("-"*80)
        
        params2 = {
            "year": 2023,
            "event": "Silverstone",
            "session": "Q",
            "driver1": "HAM",
            "driver2": "RUS"
        }
        
        response2 = await client.get(
            f"{base_url}/api/v1/compare/cars/performance",
            params=params2
        )
        print(json.dumps(response2.json(), indent=2, default=str))
        
        # Example 3: Sainz vs Norris - Monaco 2023
        print("\n\n🏎️  Example 3: SAI vs NOR - Monaco 2023 Race")
        print("-"*80)
        
        params3 = {
            "year": 2023,
            "event": "Monaco",
            "session": "R",
            "driver1": "SAI",
            "driver2": "NOR"
        }
        
        response3 = await client.get(
            f"{base_url}/api/v1/compare/cars/performance",
            params=params3
        )
        print(json.dumps(response3.json(), indent=2, default=str))
    
    print("\n" + "="*80)
    print("✅ Car Performance Comparison Demo Complete")
    print("="*80)


if __name__ == "__main__":
    asyncio.run(demo_car_performance_comparison())

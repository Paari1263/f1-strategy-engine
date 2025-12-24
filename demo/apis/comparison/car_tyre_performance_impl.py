"""
Car Tyre Performance Comparison API Demo
Compares tyre management and degradation between drivers
"""
import asyncio
import json
import httpx


async def demo_tyre_performance_comparison():
    """Demonstrate Tyre Performance Comparison API"""
    print("="*80)
    print("TYRE PERFORMANCE COMPARISON API - Demo")
    print("="*80)
    
    base_url = "http://localhost:8001"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Example 1: Verstappen vs Hamilton - Soft tyres
        print("\n🛞 Example 1: VER vs HAM - Bahrain 2024 Race (SOFT)")
        print("-"*80)
        
        params = {
            "year": 2024,
            "event": "Bahrain",
            "session": "R",
            "driver1": "VER",
            "driver2": "HAM",
            "compound": "SOFT"
        }
        
        response = await client.get(
            f"{base_url}/api/v1/compare/cars/tyre-performance",
            params=params
        )
        print(json.dumps(response.json(), indent=2, default=str))
        
        # Example 2: Leclerc vs Sainz - Medium tyres
        print("\n\n🛞 Example 2: LEC vs SAI - Monaco 2023 Race (MEDIUM)")
        print("-"*80)
        
        params2 = {
            "year": 2023,
            "event": "Monaco",
            "session": "R",
            "driver1": "LEC",
            "driver2": "SAI",
            "compound": "MEDIUM"
        }
        
        response2 = await client.get(
            f"{base_url}/api/v1/compare/cars/tyre-performance",
            params=params2
        )
        print(json.dumps(response2.json(), indent=2, default=str))
        
        # Example 3: Norris vs Piastri - Hard tyres
        print("\n\n🛞 Example 3: NOR vs PIA - Silverstone 2023 Race (HARD)")
        print("-"*80)
        
        params3 = {
            "year": 2023,
            "event": "Silverstone",
            "session": "R",
            "driver1": "NOR",
            "driver2": "PIA",
            "compound": "HARD"
        }
        
        response3 = await client.get(
            f"{base_url}/api/v1/compare/cars/tyre-performance",
            params=params3
        )
        print(json.dumps(response3.json(), indent=2, default=str))
    
    print("\n" + "="*80)
    print("✅ Tyre Performance Comparison Demo Complete")
    print("="*80)


if __name__ == "__main__":
    asyncio.run(demo_tyre_performance_comparison())

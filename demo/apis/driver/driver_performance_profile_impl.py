"""
Driver Performance Profile API Demo
Comprehensive driver performance analysis with pace, consistency, and car metrics
"""
import asyncio
import json
import httpx


async def demo_driver_performance_profile():
    """Demonstrate Driver Performance Profile API"""
    print("="*80)
    print("DRIVER PERFORMANCE PROFILE API - Demo")
    print("="*80)
    
    base_url = "http://localhost:8001"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Example 1: Verstappen - Bahrain 2024 Race
        print("\n👤 Example 1: VER - Bahrain 2024 Race Performance Profile")
        print("-"*80)
        
        params = {
            "year": 2024,
            "event": "Bahrain",
            "session": "R",
            "driver": "VER"
        }
        
        response = await client.get(
            f"{base_url}/api/v1/driver/performance-profile",
            params=params
        )
        print(json.dumps(response.json(), indent=2, default=str))
        
        # Example 2: Leclerc - Monaco 2023 Qualifying
        print("\n\n👤 Example 2: LEC - Monaco 2023 Qualifying Profile")
        print("-"*80)
        
        params2 = {
            "year": 2023,
            "event": "Monaco",
            "session": "Q",
            "driver": "LEC"
        }
        
        response2 = await client.get(
            f"{base_url}/api/v1/driver/performance-profile",
            params=params2
        )
        print(json.dumps(response2.json(), indent=2, default=str))
        
        # Example 3: Hamilton - Silverstone 2023 Race
        print("\n\n👤 Example 3: HAM - Silverstone 2023 Race Profile")
        print("-"*80)
        
        params3 = {
            "year": 2023,
            "event": "Silverstone",
            "session": "R",
            "driver": "HAM"
        }
        
        response3 = await client.get(
            f"{base_url}/api/v1/driver/performance-profile",
            params=params3
        )
        print(json.dumps(response3.json(), indent=2, default=str))
    
    print("\n" + "="*80)
    print("✅ Driver Performance Profile Demo Complete")
    print("="*80)


if __name__ == "__main__":
    asyncio.run(demo_driver_performance_profile())

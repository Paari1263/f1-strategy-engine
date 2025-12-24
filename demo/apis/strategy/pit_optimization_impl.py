"""
Pit Optimization Strategy API Demo
Real-time pit stop strategy optimization during races
"""
import asyncio
import json
import httpx


async def demo_pit_optimization():
    """Demonstrate Pit Optimization Strategy API"""
    print("="*80)
    print("PIT OPTIMIZATION STRATEGY API - Demo")
    print("="*80)
    
    base_url = "http://localhost:8001"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Example 1: Early race decision - Lap 15 of 57
        print("\n🔧 Example 1: VER - Bahrain 2024, Lap 15/57 (Early Race)")
        print("-"*80)
        
        params = {
            "year": 2024,
            "event": "Bahrain",
            "driver": "VER",
            "current_lap": 15,
            "total_laps": 57,
            "current_compound": "MEDIUM",
            "tyre_age": 14,
            "position": 1,
            "gap_ahead": None,  # Leading
            "gap_behind": 3.2
        }
        
        response = await client.get(
            f"{base_url}/api/v1/strategy/pit-optimization",
            params={k: v for k, v in params.items() if v is not None}
        )
        print(json.dumps(response.json(), indent=2, default=str))
        
        # Example 2: Mid-race undercut opportunity
        print("\n\n🔧 Example 2: HAM - Silverstone 2023, Lap 28/52 (Undercut Window)")
        print("-"*80)
        
        params2 = {
            "year": 2023,
            "event": "Silverstone",
            "driver": "HAM",
            "current_lap": 28,
            "total_laps": 52,
            "current_compound": "MEDIUM",
            "tyre_age": 18,
            "position": 3,
            "gap_ahead": 2.1,
            "gap_behind": 4.5
        }
        
        response2 = await client.get(
            f"{base_url}/api/v1/strategy/pit-optimization",
            params=params2
        )
        print(json.dumps(response2.json(), indent=2, default=str))
        
        # Example 3: Late race decision - Managing to finish
        print("\n\n🔧 Example 3: LEC - Monaco 2023, Lap 65/78 (Tyre Management)")
        print("-"*80)
        
        params3 = {
            "year": 2023,
            "event": "Monaco",
            "driver": "LEC",
            "current_lap": 65,
            "total_laps": 78,
            "current_compound": "HARD",
            "tyre_age": 30,
            "position": 2,
            "gap_ahead": 8.5,
            "gap_behind": 12.3
        }
        
        response3 = await client.get(
            f"{base_url}/api/v1/strategy/pit-optimization",
            params=params3
        )
        print(json.dumps(response3.json(), indent=2, default=str))
    
    print("\n" + "="*80)
    print("✅ Pit Optimization Strategy Demo Complete")
    print("="*80)


if __name__ == "__main__":
    asyncio.run(demo_pit_optimization())

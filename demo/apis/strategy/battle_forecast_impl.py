"""
Battle Forecast Strategy API Demo
Predicts overtaking probability and strategic recommendations for battles
"""
import asyncio
import json
import httpx


async def demo_battle_forecast():
    """Demonstrate Battle Forecast Strategy API"""
    print("="*80)
    print("BATTLE FORECAST STRATEGY API - Demo")
    print("="*80)
    
    base_url = "http://localhost:8001"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Example 1: DRS zone attack - Monza (easy overtaking)
        print("\n⚔️  Example 1: VER attacking LEC - Monza 2023, Lap 35 (DRS)")
        print("-"*80)
        
        params = {
            "year": 2023,
            "event": "Monza",
            "session": "R",
            "lap": 35,
            "attacker": "VER",
            "defender": "LEC",
            "gap": 0.8,
            "drs_available": True
        }
        
        response = await client.get(
            f"{base_url}/api/v1/strategy/battle-forecast",
            params=params
        )
        print(json.dumps(response.json(), indent=2, default=str))
        
        # Example 2: Close battle without DRS - Monaco (hard overtaking)
        print("\n\n⚔️  Example 2: HAM vs RUS - Monaco 2023, Lap 48 (No DRS)")
        print("-"*80)
        
        params2 = {
            "year": 2023,
            "event": "Monaco",
            "session": "R",
            "lap": 48,
            "attacker": "HAM",
            "defender": "RUS",
            "gap": 0.5,
            "drs_available": False
        }
        
        response2 = await client.get(
            f"{base_url}/api/v1/strategy/battle-forecast",
            params=params2
        )
        print(json.dumps(response2.json(), indent=2, default=str))
        
        # Example 3: Medium difficulty track - Silverstone
        print("\n\n⚔️  Example 3: NOR vs PIA - Silverstone 2023, Lap 22 (DRS)")
        print("-"*80)
        
        params3 = {
            "year": 2023,
            "event": "Silverstone",
            "session": "R",
            "lap": 22,
            "attacker": "NOR",
            "defender": "PIA",
            "gap": 1.2,
            "drs_available": True
        }
        
        response3 = await client.get(
            f"{base_url}/api/v1/strategy/battle-forecast",
            params=params3
        )
        print(json.dumps(response3.json(), indent=2, default=str))
    
    print("\n" + "="*80)
    print("✅ Battle Forecast Strategy Demo Complete")
    print("="*80)


if __name__ == "__main__":
    asyncio.run(demo_battle_forecast())

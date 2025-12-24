"""
Detailed Car Performance Comparison API Demo
Comprehensive car analysis with multiple performance dimensions
"""
import asyncio
import json
import httpx


async def demo_detailed_car_performance():
    """Demonstrate Detailed Car Performance Comparison API"""
    print("="*80)
    print("DETAILED CAR PERFORMANCE COMPARISON API - Demo")
    print("="*80)
    
    base_url = "http://localhost:8001"
    
    async with httpx.AsyncClient(timeout=180.0) as client:  # 3 minutes for FastF1 data loading
        # Example 1: Verstappen vs Perez - Bahrain 2024
        print("\n🔬 Example 1: VER vs PER - Bahrain 2024 Race (Detailed)")
        print("-"*80)
        print("⏳ Loading FastF1 data... (this may take 1-2 minutes)")
        
        params = {
            "year": 2024,
            "event": "Bahrain",
            "session": "R",
            "driver1": "VER",
            "driver2": "PER"
        }
        
        response = await client.get(
            f"{base_url}/api/v1/compare/cars/performance/detailed",
            params=params
        )
        print(json.dumps(response.json(), indent=2, default=str))
        
        # Example 2: Leclerc vs Sainz - Monaco 2023 Qualifying
        print("\n\n🔬 Example 2: LEC vs SAI - Monaco 2023 Qualifying (Detailed)")
        print("-"*80)
        
        params2 = {
            "year": 2023,
            "event": "Monaco",
            "session": "Q",
            "driver1": "LEC",
            "driver2": "SAI"
        }
        
        response2 = await client.get(
            f"{base_url}/api/v1/compare/cars/performance/detailed",
            params=params2
        )
        print(json.dumps(response2.json(), indent=2, default=str))
        
        # Example 3: Norris vs Piastri - Silverstone 2023
        print("\n\n🔬 Example 3: NOR vs PIA - Silverstone 2023 Race (Detailed)")
        print("-"*80)
        
        params3 = {
            "year": 2023,
            "event": "Silverstone",
            "session": "R",
            "driver1": "NOR",
            "driver2": "PIA"
        }
        
        response3 = await client.get(
            f"{base_url}/api/v1/compare/cars/performance/detailed",
            params=params3
        )
        print(json.dumps(response3.json(), indent=2, default=str))
    
    print("\n" + "="*80)
    print("✅ Detailed Car Performance Comparison Demo Complete")
    print("="*80)


if __name__ == "__main__":
    asyncio.run(demo_detailed_car_performance())

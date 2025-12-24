"""
Test Suite for Strategy APIs
Tests all strategy endpoints with actual API calls

Prerequisites:
- Server must be running: uvicorn engines.main:app --port 8001 --reload

Run: python api/test_strategy_apis.py
"""

import httpx
import asyncio
import json
import time


BASE_URL = "http://localhost:8001"


async def test_pit_optimization_one_stop():
    """Test Pit Strategy Optimization API (One-Stop)"""
    print("\n" + "="*70)
    print("Testing: GET /api/v1/strategy/pit-optimization (One-Stop)")
    print("="*70)
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            response = await client.get(
                f"{BASE_URL}/api/v1/strategy/pit-optimization",
                params={
                    "year": 2023,  # Using 2023 for reliable data
                    "event": "Monaco",
                    "driver": "LEC",
                    "current_lap": 20,
                    "total_laps": 58,
                    "current_compound": "MEDIUM",
                    "tyre_age": 19,
                    "position": 3
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Status: {response.status_code}")
                elapsed = time.time() - start_time
                print(f"⏱️  Response time: {elapsed:.3f}s")
                print(f"📅 Year: {data.get('year', 2023)} | 🏁 Race: {data.get('event', 'Monaco')}")
                print(f"🏎️  Driver: {data.get('driver', 'N/A')} | Position: {data.get('position', 'N/A')}")
                print(f"�📍 Current: Lap {data.get('current_lap', 'N/A')}/{data.get('total_laps', 'N/A')}")
                print(f"✅ Optimal pit lap: {data.get('optimal_pit_lap', 'N/A')}")
                print(f"🪟 Pit window: Laps {data.get('pit_window_start', 'N/A')}-{data.get('pit_window_end', 'N/A')}")
                print(f"🛞 Recommended compound: {data.get('recommended_compound', 'N/A')}")
                print(f"⚡ Undercut advantage: {data.get('undercut_advantage', 0):.2f}s")
                print(f"🌪️  Overcut advantage: {data.get('overcut_advantage', 0):.2f}s")
                print(f"📋 Strategy: {data.get('strategy_type', 'N/A')}")
                print(f"✅ Confidence: {data.get('confidence', 0):.0%}")
                print(f"\n📦 Full Response:")
                print(json.dumps(data, indent=2))
            else:
                print(f"❌ Error: {response.status_code}")
                print(response.text)
                
        except httpx.ConnectError:
            print("\n❌ ERROR: Could not connect to server")
            print("Please start the server first:")
            print("  uvicorn engines.main:app --port 8001 --reload\n")
            raise
        except Exception as e:
            print(f"❌ Error during testing: {e}")
            raise


async def test_pit_optimization_two_stop():
    """Test Pit Strategy Optimization API (Two-Stop)"""
    print("\n" + "="*70)
    print("Testing: GET /api/v1/strategy/pit-optimization (Two-Stop)")
    print("="*70)
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            start_time = time.time()
            response = await client.get(
                f"{BASE_URL}/api/v1/strategy/pit-optimization",
                params={
                    "year": 2023,  # Using 2023 for reliable data
                    "event": "Silverstone",
                    "driver": "HAM",
                    "current_lap": 15,
                    "total_laps": 70,
                    "current_compound": "SOFT",
                    "tyre_age": 14,
                    "position": 5
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Status: {response.status_code}")
                elapsed = time.time() - start_time
                print(f"⏱️  Response time: {elapsed:.3f}s")
                print(f"📅 Year: {data.get('year', 2023)} | 🏁 Race: {data.get('event', 'Silverstone')}")
                print(f"🏎️  Driver: {data.get('driver', 'N/A')} | Position: {data.get('position', 'N/A')}")
                print(f"�📋 Strategy Type: {data.get('strategy_type', 'N/A')}")
                print(f"✅ Optimal pit lap: {data.get('optimal_pit_lap', 'N/A')}")
                print(f"🛞 Recommended compound: {data.get('recommended_compound', 'N/A')}")
                
                if 'second_stop' in data:
                    print(f"\n🔄 Second Stop:")
                    print(f"  Lap: {data['second_stop'].get('lap', 'N/A')}")
                    print(f"  Compound: {data['second_stop'].get('compound', 'N/A')}")
                print(f"\n📦 Full Response:")
                print(json.dumps(data, indent=2))
            else:
                print(f"❌ Error: {response.status_code}")
                print(response.text)
                
        except Exception as e:
            print(f"❌ Error during testing: {e}")
            raise


async def test_pit_optimization_different_compounds():
    """Test Pit Optimization with Different Compounds"""
    print("\n" + "="*70)
    print("Testing: Pit Optimization with Different Compounds")
    print("="*70)
    
    compounds = ["SOFT", "MEDIUM", "HARD"]
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            for compound in compounds:
                start_time = time.time()
                response = await client.get(
                    f"{BASE_URL}/api/v1/strategy/pit-optimization",
                    params={
                        "year": 2023,  # Using 2023 for reliable data
                        "event": "Monaco",
                        "driver": "VER",
                        "current_lap": 20,
                        "total_laps": 58,
                        "current_compound": compound,
                        "tyre_age": 19,
                        "position": 1
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Status: {response.status_code}")
                    elapsed = time.time() - start_time
                    print(f"⏱️  Response time: {elapsed:.3f}s")
                    print(f"\n  {compound}:")
                    print(f"    Optimal pit lap: {data.get('optimal_pit_lap', 'N/A')}")
                    print(f"    Recommended: {data.get('recommended_compound', 'N/A')}")
                    print(f"\n📦 Full Response:")
                    print(json.dumps(data, indent=2))
                else:
                    print(f"\n  {compound}: Error {response.status_code}")
                    
        except Exception as e:
            print(f"❌ Error during testing: {e}")
            raise


async def test_battle_forecast_with_drs():
    """Test Battle Forecast API (With DRS)"""
    print("\n" + "="*70)
    print("Testing: GET /api/v1/strategy/battle-forecast (With DRS)")
    print("="*70)
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            start_time = time.time()
            response = await client.get(
                f"{BASE_URL}/api/v1/strategy/battle-forecast",
                params={
                    "year": 2023,  # Using 2023 for reliable data
                    "event": "Monza",
                    "session": "R",
                    "lap": 25,
                    "attacker": "VER",
                    "defender": "LEC",
                    "gap": 0.8,
                    "drs_available": True
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Status: {response.status_code}")
                elapsed = time.time() - start_time
                print(f"⏱️  Response time: {elapsed:.3f}s")
                print(f"📅 Year: {data.get('year', 2023)} | 🏁 Race: {data.get('event', 'Monza')} | 📊 Session: {data.get('session', 'R')}")
                print(f"⚔️  Battle: {data.get('attacker', 'N/A')} vs {data.get('defender', 'N/A')}")
                print(f"📏 Lap: {data.get('lap', 'N/A')}")
                print(f"🎯 Overtake Probability: {data.get('overtake_probability', 0):.1%}")
                print(f"📍 Best Zone: {data.get('best_overtaking_zone', 'N/A')}")
                print(f"⚡ Strategy: {data.get('recommended_strategy', 'N/A')}")
                print(f"🚀 Speed Advantage: {data.get('speed_advantage', 0):.1f} km/h")
                
                if 'key_factors' in data:
                    print(f"\n💡 Key Factors:")
                    for factor in data['key_factors']:
                        print(f"  - {factor}")
                print(f"\n📦 Full Response:")
                print(json.dumps(data, indent=2))
            else:
                print(f"❌ Error: {response.status_code}")
                print(response.text)
                
        except Exception as e:
            print(f"❌ Error during testing: {e}")
            raise


async def test_battle_forecast_without_drs():
    """Test Battle Forecast API (Without DRS)"""
    print("\n" + "="*70)
    print("Testing: GET /api/v1/strategy/battle-forecast (Without DRS)")
    print("="*70)
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            start_time = time.time()
            response = await client.get(
                f"{BASE_URL}/api/v1/strategy/battle-forecast",
                params={
                    "year": 2023,  # Using 2023 for reliable data
                    "event": "Monaco",
                    "session": "R",
                    "lap": 35,
                    "attacker": "HAM",  # NOR/PIA weren't competitive in 2023, using HAM
                    "defender": "ALO",
                    "gap": 1.2,
                    "drs_available": False
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Status: {response.status_code}")
                elapsed = time.time() - start_time
                print(f"⏱️  Response time: {elapsed:.3f}s")
                print(f"📅 Year: {data.get('year', 2023)} | 🏁 Race: {data.get('event', 'Monaco')} | 📊 Session: {data.get('session', 'R')}")
                print(f"⚔️  Battle: {data.get('attacker', 'N/A')} vs {data.get('defender', 'N/A')}")
                print(f"🎯 Overtake Probability: {data.get('overtake_probability', 0):.1%}")
                print(f"🚫 DRS: Not Available")
                print(f"\n📦 Full Response:")
                print(json.dumps(data, indent=2))
            else:
                print(f"❌ Error: {response.status_code}")
                print(response.text)
                
        except Exception as e:
            print(f"❌ Error during testing: {e}")
            raise


async def test_battle_forecast_different_gaps():
    """Test Battle Forecast with Different Gaps"""
    print("\n" + "="*70)
    print("Testing: Battle Forecast with Different Gaps")
    print("="*70)
    
    gaps = [0.3, 0.8, 1.5, 2.5]
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            for gap in gaps:
                start_time = time.time()
                response = await client.get(
                    f"{BASE_URL}/api/v1/strategy/battle-forecast",
                    params={
                        "year": 2023,  # Using 2023 for reliable data
                        "event": "Monza",
                        "session": "R",
                        "lap": 25,
                        "attacker": "VER",
                        "defender": "LEC",
                        "gap": gap,
                        "drs_available": True
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Status: {response.status_code}")
                    elapsed = time.time() - start_time
                    print(f"⏱️  Response time: {elapsed:.3f}s")
                    print(f"\n  Gap {gap}s:")
                    print(f"    Overtake Probability: {data.get('overtake_probability', 0):.1%}")
                    print(f"\n📦 Full Response:")
                    print(json.dumps(data, indent=2))
                else:
                    print(f"\n  Gap {gap}s: Error {response.status_code}")
                    
        except Exception as e:
            print(f"❌ Error during testing: {e}")
            raise


async def main():
    """Run all strategy API tests"""
    print("\n" + "="*70)
    print("  STRATEGY APIs - TEST SUITE")
    print("  Testing all strategy endpoints")
    print("="*70)
    print("\n⚠️  Make sure server is running:")
    print("  uvicorn engines.main:app --port 8001 --reload\n")
    
    await asyncio.sleep(1)
    
    try:
        # Test all strategy endpoints
        await test_pit_optimization_one_stop()
        await test_pit_optimization_two_stop()
        await test_pit_optimization_different_compounds()
        await test_battle_forecast_with_drs()
        await test_battle_forecast_without_drs()
        await test_battle_forecast_different_gaps()
        
        print("\n" + "="*70)
        print("  ✅ ALL STRATEGY API TESTS COMPLETED!")
        print("="*70)
        print("\n📚 View interactive API docs at:")
        print("  http://localhost:8001/docs")
        print("="*70 + "\n")
        
    except httpx.ConnectError:
        print("\n❌ ERROR: Could not connect to server")
        print("Please start the server first:")
        print("  uvicorn engines.main:app --port 8001 --reload\n")
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())

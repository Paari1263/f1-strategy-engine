"""
Test Suite for Comparison APIs
Tests all comparison endpoints with actual API calls

Prerequisites:
- Server must be running: uvicorn engines.main:app --port 8001 --reload

Run: python api/test_comparison_apis.py
"""

import httpx
import asyncio
import json
import time


BASE_URL = "http://localhost:8001"


async def test_car_performance_comparison():
    """Test Car vs Car Performance API"""
    print("\n" + "="*70)
    print("Testing: GET /api/v1/compare/cars/performance")
    print("="*70)
    
    async with httpx.AsyncClient(timeout=120.0) as client:  # Increased timeout for data loading
        try:
            start_time = time.time()
            response = await client.get(
                f"{BASE_URL}/api/v1/compare/cars/performance",
                params={
                    "year": 2023,  # Using 2023 for reliable data
                    "event": "Monaco",
                    "session": "Q",
                    "driver1": "VER",
                    "driver2": "LEC"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Status: {response.status_code}")
                elapsed = time.time() - start_time
                print(f"⏱️  Response time: {elapsed:.3f}s")
                print(f"📅 Year: {data['year']} | 🏁 Race: {data['event']} | 📊 Session: {data['session']}")
                print(f"🏎️  Comparison: {data['driver1']} vs {data['driver2']}")
                print(f"⏱️  Lap time delta: {data['lap_time_delta']:.3f}s")
                print(f"🏆 Winner: {data['winner']}")
                print(f"\nSpeed Analysis:")
                print(f"  {json.dumps(data['speed_analysis'], indent=2)}")
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
        except httpx.ReadTimeout:
            print("\n⌛ TIMEOUT: Server took too long to respond")
            print("This usually means the server is loading F1 data for the first time.")
            print("Please wait a few minutes and try again.\n")
            raise
        except Exception as e:
            print(f"❌ Error during testing: {e}")
            raise


async def test_car_performance_detailed():
    """Test Detailed Car Performance Comparison API"""
    print("\n" + "="*70)
    print("Testing: GET /api/v1/compare/cars/performance/detailed")
    print("="*70)
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            start_time = time.time()
            response = await client.get(
                f"{BASE_URL}/api/v1/compare/cars/performance/detailed",
                params={
                    "year": 2023,  # Using 2023 for reliable data
                    "event": "Monaco",
                    "session": "Q",
                    "driver1": "VER",
                    "driver2": "LEC"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Status: {response.status_code}")
                elapsed = time.time() - start_time
                print(f"⏱️  Response time: {elapsed:.3f}s")
                print(f"📅 Year: 2023 | 🏁 Race: {data['car1']['metadata'].get('track', 'Monaco')} | 📊 Session: {data['car1']['metadata'].get('session', 'Q')}")
                print(f"\n🏎️  Car 1 ({data['car1']['metadata']['driver']}):")
                print(f"  Team: {data['car1']['metadata']['team']}")
                print(f"  Power Delta: {data['car1']['performance_profile']['powerDelta']:.3f}s")
                print(f"  Aero Delta: {data['car1']['performance_profile']['aeroDelta']:.3f}s")
                print(f"  Drag Penalty: {data['car1']['performance_profile']['dragPenalty']:.3f}s")
                print(f"  Mechanical Grip Delta: {data['car1']['performance_profile']['mechanicalGripDelta']:.3f}s")
                
                print(f"\n🏎️  Car 2 ({data['car2']['metadata']['driver']}):")
                print(f"  Team: {data['car2']['metadata']['team']}")
                print(f"  Performance Delta: {data['car2']['performance_profile']['powerDelta']:.3f}s")
                
                print(f"\n📊 Delta Analysis:")
                print(f"  Power Delta: {data['delta_analysis']['power_delta']:.3f}s")
                print(f"  Aero Delta: {data['delta_analysis']['aero_delta']:.3f}s")
                print(f"  Drag Delta: {data['delta_analysis']['drag_delta']:.3f}s")
                print(f"  Grip Delta: {data['delta_analysis']['grip_delta']:.3f}s")
                
                print(f"\n🏆 Overall Advantage: {data['overall_advantage']}")
                print(f"\n📦 Full Response:")
                print(json.dumps(data, indent=2))
            else:
                print(f"❌ Error: {response.status_code}")
                print(response.text)
                
        except Exception as e:
            print(f"❌ Error during testing: {e}")
            raise


async def test_tyre_performance_comparison():
    """Test Tyre Performance Comparison API"""
    print("\n" + "="*70)
    print("Testing: GET /api/v1/compare/cars/tyre-performance")
    print("="*70)
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            start_time = time.time()
            response = await client.get(
                f"{BASE_URL}/api/v1/compare/cars/tyre-performance",
                params={
                    "year": 2023,  # Using 2023 for reliable data
                    "event": "Barcelona",
                    "session": "R",
                    "driver1": "HAM",
                    "driver2": "RUS",
                    "compound": "HARD"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Status: {response.status_code}")
                print(f"� Year: {data['year']} | 🏁 Race: {data['event']} | 📊 Session: {data['session']}")
                print(f"�🛞 Compound: {data['compound']}")
                print(f"👥 Comparison: {data['driver1']} vs {data['driver2']}")
                print(f"🏆 Better Management: {data['better_management']}")
                print(f"\nDegradation Rate (s/lap):")
                print(f"  {json.dumps(data['degradation_rate'], indent=2)}")
                print(f"\nManagement Scores:")
                print(f"  {json.dumps(data['management_score'], indent=2)}")
                print(f"\n📦 Full Response:")
                print(json.dumps(data, indent=2))
            else:
                print(f"❌ Error: {response.status_code}")
                print(response.text)
                
        except Exception as e:
            print(f"❌ Error during testing: {e}")
            raise


async def test_driver_pace_comparison():
    """Test Driver vs Driver Pace API"""
    print("\n" + "="*70)
    print("Testing: GET /api/v1/compare/drivers/pace")
    print("="*70)
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            start_time = time.time()
            response = await client.get(
                f"{BASE_URL}/api/v1/compare/drivers/pace",
                params={
                    "year": 2023,  # Using 2023 for reliable data
                    "event": "Silverstone",
                    "session": "R",
                    "driver1": "VER",
                    "driver2": "HAM",  # NOR wasn't competitive in 2023, using HAM
                    "fuel_corrected": True
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Status: {response.status_code}")
                print(f"� Year: {data['year']} | 🏁 Race: {data['event']} | 📊 Session: {data['session']}")
                print(f"�👥 Comparison: {data['driver1']} vs {data['driver2']}")
                print(f"⚡ Pace delta: {data['pace_delta']:.3f}s")
                print(f"🏆 Advantage: {data['pace_advantage']}")
                print(f"\nFastest Laps:")
                print(f"  {json.dumps(data['fastest_lap'], indent=2)}")
                print(f"\n📦 Full Response:")
                print(json.dumps(data, indent=2))
            else:
                print(f"❌ Error: {response.status_code}")
                print(response.text)
                
        except Exception as e:
            print(f"❌ Error during testing: {e}")
            raise


async def test_driver_consistency_comparison():
    """Test Driver Consistency Comparison API"""
    print("\n" + "="*70)
    print("Testing: GET /api/v1/compare/drivers/consistency")
    print("="*70)
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            start_time = time.time()
            response = await client.get(
                f"{BASE_URL}/api/v1/compare/drivers/consistency",
                params={
                    "year": 2023,  # Using 2023 for reliable data
                    "event": "Silverstone",
                    "session": "R",
                    "driver1": "VER",
                    "driver2": "HAM"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Status: {response.status_code}")
                print(f"� Year: {data['year']} | 🏁 Race: {data['event']} | 📊 Session: {data['session']}")
                print(f"�👥 Comparison: {data['driver1']} vs {data['driver2']}")
                print(f"🎯 More Consistent: {data.get('more_consistent', 'N/A')}")
                print(f"\n📦 Full Response:")
                print(json.dumps(data, indent=2))
            else:
                print(f"❌ Error: {response.status_code}")
                print(response.text)
                
        except Exception as e:
            print(f"❌ Error during testing: {e}")
            raise


async def main():
    """Run all comparison API tests"""
    print("\n" + "="*70)
    print("  COMPARISON APIs - TEST SUITE")
    print("  Testing all comparison endpoints")
    print("="*70)
    print("\n⚠️  Make sure server is running:")
    print("  uvicorn engines.main:app --port 8001 --reload\n")
    
    await asyncio.sleep(1)
    
    try:
        # Test all comparison endpoints
        await test_car_performance_comparison()
        await test_car_performance_detailed()
        await test_tyre_performance_comparison()
        await test_driver_pace_comparison()
        await test_driver_consistency_comparison()
        
        print("\n" + "="*70)
        print("  ✅ ALL COMPARISON API TESTS COMPLETED!")
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

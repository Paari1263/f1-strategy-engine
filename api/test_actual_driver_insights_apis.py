"""
Test Suite for Driver Insights APIs
Tests all driver-specific endpoints with actual API calls

Prerequisites:
- Server must be running: uvicorn engines.main:app --port 8001 --reload

Run: python api/test_driver_insights_apis.py
"""

import httpx
import asyncio
import json
import time


BASE_URL = "http://localhost:8001"


async def test_driver_performance_profile():
    """Test Driver Performance Profile API"""
    print("\n" + "="*70)
    print("Testing: GET /api/v1/driver/performance-profile")
    print("="*70)
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            response = await client.get(
                f"{BASE_URL}/api/v1/driver/performance-profile",
                params={
                    "year": 2023,  # Using 2023 for reliable data
                    "event": "Monaco",
                    "session": "Q",
                    "driver": "VER"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Status: {response.status_code}")
                elapsed = time.time() - start_time
                print(f"⏱️  Response time: {elapsed:.3f}s")
                print(f"📅 Year: {data.get('year', 2023)} | 🏁 Race: {data.get('event', 'Monaco')} | 📊 Session: {data.get('session', 'Q')}")
                print(f"🏎️  Driver: {data.get('driver', 'N/A')}")
                print(f"⭐ Overall Rating: {data.get('overall_rating', 0)}/10")
                print(f"\n💪 Strengths:")
                for strength in data.get('strengths', []):
                    print(f"  - {strength}")
                print(f"\n⚠️  Weaknesses:")
                for weakness in data.get('weaknesses', []):
                    print(f"  - {weakness}")
                print(f"\nPace Metrics:")
                print(f"  {json.dumps(data.get('pace_metrics', {}), indent=2)}")
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


async def test_driver_performance_profile_race():
    """Test Driver Performance Profile for Race Session"""
    print("\n" + "="*70)
    print("Testing: GET /api/v1/driver/performance-profile (Race)")
    print("="*70)
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            start_time = time.time()
            response = await client.get(
                f"{BASE_URL}/api/v1/driver/performance-profile",
                params={
                    "year": 2023,  # Using 2023 for reliable data
                    "event": "Suzuka",
                    "session": "R",
                    "driver": "VER"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Status: {response.status_code}")
                elapsed = time.time() - start_time
                print(f"⏱️  Response time: {elapsed:.3f}s")
                print(f"📅 Year: {data.get('year', 2023)} | 🏁 Race: {data.get('event', 'Suzuka')} | 📊 Session: {data.get('session', 'R')}")
                print(f"🏎️  Driver: {data.get('driver', 'N/A')}")
                print(f"⭐ Overall Rating: {data.get('overall_rating', 0)}/10")
                print(f"📊 Consistency: {data.get('consistency', 'N/A')}")
                print(f"🏁 Race Craft: {data.get('race_craft', 'N/A')}")
                print(f"\n📦 Full Response:")
                print(json.dumps(data, indent=2))
            else:
                print(f"❌ Error: {response.status_code}")
                print(response.text)
                
        except httpx.ReadTimeout:
            print("\n⌛ TIMEOUT: Server took too long to respond")
            print("Please wait and try again.\n")
            raise
        except Exception as e:
            print(f"❌ Error during testing: {e}")
            raise


async def test_stint_analysis():
    """Test Stint Analysis API"""
    print("\n" + "="*70)
    print("Testing: GET /api/v1/driver/stint-analysis")
    print("="*70)
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            start_time = time.time()
            response = await client.get(
                f"{BASE_URL}/api/v1/driver/stint-analysis",
                params={
                    "year": 2023,  # Using 2023 for reliable data
                    "event": "Silverstone",
                    "session": "R",
                    "driver": "HAM",
                    "stint": 1  # First stint
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Status: {response.status_code}")
                elapsed = time.time() - start_time
                print(f"⏱️  Response time: {elapsed:.3f}s")
                print(f"📅 Year: {data.get('year', 2023)} | 🏁 Race: {data.get('event', 'Silverstone')} | 📊 Session: {data.get('session', 'R')}")
                print(f"🏎️  Driver: {data.get('driver', 'N/A')}")
                print(f"🛞 Total Stints: {len(data.get('stints', []))}")
                
                if 'stints' in data and data['stints']:
                    print(f"\n📊 Stint Details:")
                    for i, stint in enumerate(data['stints'][:3], 1):
                        print(f"\n  Stint {i}:")
                        print(f"    Compound: {stint.get('compound', 'N/A')}")
                        print(f"    Laps: {stint.get('laps', 'N/A')}")
                        print(f"    Avg Pace: {stint.get('avg_pace', 'N/A')}")
                        print(f"    Degradation: {stint.get('degradation', 'N/A')}")
                print(f"\n📦 Full Response:")
                print(json.dumps(data, indent=2))
            else:
                print(f"❌ Error: {response.status_code}")
                print(response.text)
                
        except httpx.ReadTimeout:
            print("\n⌛ TIMEOUT: Server took too long to respond")
            raise
        except Exception as e:
            print(f"❌ Error during testing: {e}")
            raise


async def test_multiple_drivers_profile():
    """Test Performance Profile for Multiple Drivers"""
    print("\n" + "="*70)
    print("Testing: Multiple Drivers Performance Profiles")
    print("="*70)
    
    drivers = ["VER", "LEC", "HAM", "NOR", "PIA"]
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            for driver in drivers:
                start_time = time.time()
                response = await client.get(
                    f"{BASE_URL}/api/v1/driver/performance-profile",
                    params={
                        "year": 2023,  # Using 2023 for reliable data
                        "event": "Monaco",
                        "session": "Q",
                        "driver": driver
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Status: {response.status_code}")
                    elapsed = time.time() - start_time
                    print(f"⏱️  Response time: {elapsed:.3f}s")
                    print(f"\n  {driver}: Rating {data.get('overall_rating', 0)}/10")
                    print(f"\n📦 Full Response:")
                    print(json.dumps(data, indent=2))
                else:
                    print(f"\n  {driver}: Error {response.status_code}")
                    
        except httpx.ReadTimeout:
            print("\n⌛ TIMEOUT: Server took too long")
            raise
        except Exception as e:
            print(f"❌ Error during testing: {e}")
            raise


async def main():
    """Run all driver insights API tests"""
    print("\n" + "="*70)
    print("  DRIVER INSIGHTS APIs - TEST SUITE")
    print("  Testing all driver-specific endpoints")
    print("="*70)
    print("\n⚠️  Make sure server is running:")
    print("  uvicorn engines.main:app --port 8001 --reload\n")
    
    await asyncio.sleep(1)
    
    try:
        # Test all driver insights endpoints
        await test_driver_performance_profile()
        await test_driver_performance_profile_race()
        await test_stint_analysis()
        await test_multiple_drivers_profile()
        
        print("\n" + "="*70)
        print("  ✅ ALL DRIVER INSIGHTS API TESTS COMPLETED!")
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

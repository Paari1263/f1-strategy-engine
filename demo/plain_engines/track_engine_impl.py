"""
Track Engine Implementation Demo
Shows how to use the Track Engine to analyze circuit characteristics
"""
import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from engines.track_engine.service import TrackService
from engines.track_engine.schemas import TrackRequest


async def demo_track_analysis():
    """Demonstrate Track Engine capabilities"""
    print("="*70)
    print("TRACK ENGINE - Circuit Analysis Demo")
    print("="*70)
    
    # Example 1: Analyze Bahrain Circuit
    print("\n📍 Example 1: Bahrain 2024 Race")
    print("-"*70)
    
    request = TrackRequest(
        year=2024,
        gp="Bahrain",
        session="R"
    )
    
    result = await TrackService.get_track_characteristics(request)
    
    print(f"\n✅ Circuit: {result.circuit_name}")
    print(f"   Location: {result.location}, {result.country}")
    print(f"   Length: {result.length_km} km")
    print(f"   Corners: {result.corners}")
    print(f"   Overtaking Difficulty: {result.overtaking_difficulty}/10")
    print(f"   Pit Lane Time Loss: {result.pit_lane_time_loss_sec}s")
    
    if result.sector_analysis:
        print(f"\n   Sector Breakdown:")
        for sector in result.sector_analysis:
            print(f"     Sector {sector.sector_number}: {sector.avg_speed_kmh} km/h avg")
    
    if result.drs_zones:
        print(f"\n   DRS Zones: {len(result.drs_zones)} zones")
        for zone in result.drs_zones:
            print(f"     Zone {zone.zone_number}: {zone.length_m}m, {zone.effectiveness_score:.1f} effectiveness")
    
    # Example 2: Monaco - Low Speed Street Circuit
    print("\n\n📍 Example 2: Monaco 2023 Race")
    print("-"*70)
    
    request2 = TrackRequest(
        year=2023,
        gp="Monaco",
        session="R"
    )
    
    result2 = await TrackService.get_track_characteristics(request2)
    
    print(f"\n✅ Circuit: {result2.circuit_name}")
    print(f"   Length: {result2.length_km} km")
    print(f"   Corners: {result2.corners}")
    print(f"   Top Speed: {result2.top_speed_kmh} km/h")
    print(f"   Slowest Corner: {result2.slowest_corner_kmh} km/h")
    print(f"   Power Sensitivity: {result2.power_sensitivity}")
    print(f"   Corner Sensitivity: {result2.corner_sensitivity}")
    
    # Example 3: Monza - High Speed Circuit
    print("\n\n📍 Example 3: Monza 2023 Race")
    print("-"*70)
    
    request3 = TrackRequest(
        year=2023,
        gp="Monza",
        session="R"
    )
    
    result3 = await TrackService.get_track_characteristics(request3)
    
    print(f"\n✅ Circuit: {result3.circuit_name}")
    print(f"   Top Speed: {result3.top_speed_kmh} km/h")
    print(f"   Grip Multiplier: {result3.grip_multiplier}")
    print(f"   Tyre Abrasion: {result3.tyre_abrasion_level}")
    print(f"   Safety Car Probability: {result3.historical_safety_car_probability:.1%}")
    
    print("\n" + "="*70)
    print("✅ Track Engine Demo Complete")
    print("="*70)


if __name__ == "__main__":
    asyncio.run(demo_track_analysis())

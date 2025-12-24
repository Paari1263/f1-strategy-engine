"""
Consolidated test script for ALL calculation engines
Runs all calculation module tests

Run: python calculation_engines/test_all_calculations.py
"""
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import all calculations
from calculation_engines import *


def print_section(title):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def test_tyre_calculations():
    print_section("TYRE CALCULATIONS (5 modules)")
    
    # Compound Delta
    result = compound_delta_calc.calculate(compound="SOFT")
    print(f"✓ Compound Delta: SOFT = {result.lap_time_delta_s}s vs MEDIUM")
    
    # Thermal Window
    result = thermal_window_calc.calculate(track_temp_c=95, compound="MEDIUM")
    print(f"✓ Thermal Window: 95°C penalty = {result.temp_penalty_s_per_lap}s, In window: {result.is_in_window}")
    
    # Push Penalty
    result = push_penalty_calc.calculate(push_level=0.7)
    print(f"✓ Push Penalty: 70% push = {result.push_multiplier}x degradation")
    
    # Degradation Curve
    result = degradation_curve_calc.calculate(wear_level=0.5, temp_factor=1.1, track_abrasion=0.6)
    print(f"✓ Degradation Curve: Rate = {result.degradation_rate_s_per_lap:.3f}s/lap")
    
    # Tyre Life Projection
    result = tyre_life_projection_calc.calculate(total_expected_life=30, laps_completed=15)
    print(f"✓ Tyre Life: {result.remaining_laps} laps remaining, cliff at lap {result.cliff_lap_estimate}")


def test_car_calculations():
    print_section("CAR CALCULATIONS (5 modules)")
    
    # Performance Index
    result = car_performance_index_calc.calculate(power=7.5, aero_efficiency=8.0, drag_coefficient=5.0, mechanical_grip=7.0)
    print(f"✓ Performance Index: {result.performance_index:.2f}/10")
    
    # Aero/Drag Balance
    result = aero_drag_balance_calc.calculate(downforce_level=7.0, drag_level=6.0, track_type='balanced')
    print(f"✓ Aero/Drag Balance: Score = {result.balance_score:.2f}/10, Rec: {result.recommendation}")
    
    # Fuel Effect
    result = fuel_effect_calc.calculate(fuel_load_kg=60.0)
    print(f"✓ Fuel Effect: 60kg = {result.fuel_penalty_s:.2f}s penalty")
    
    # Reliability Risk
    result = reliability_risk_calc.calculate(component_age_events=5, max_component_life=7, stress_level=0.6)
    print(f"✓ Reliability Risk: {result.failure_probability:.3f} probability, {result.risk_level} risk")
    
    # Tyre-Car Interaction
    result = tyre_car_interaction_calc.calculate(downforce_level=7.0, car_weight_kg=755, power_output=7.5)
    print(f"✓ Tyre-Car Interaction: {result.wear_multiplier:.2f}x wear, +{result.temp_delta_c:.1f}°C")


def test_driver_calculations():
    print_section("DRIVER CALCULATIONS (5 modules)")
    
    # Pace Delta
    result = driver_pace_calc.calculate(lap_times=[89.5, 89.6, 89.4], field_average=90.0)
    print(f"✓ Pace Delta: {result.pace_delta_s:.3f}s vs field, {result.percentile_rank:.1f}th percentile")
    
    # Consistency
    result = driver_consistency_calc.calculate(lap_times=[90.0, 90.1, 89.9, 90.0, 90.1])
    print(f"✓ Consistency: Score = {result.consistency_score:.3f}, StdDev = {result.std_dev_s:.3f}s")
    
    # Driver Form
    result = driver_form_calc.calculate(recent_positions=[6, 5, 4, 3, 4])
    print(f"✓ Driver Form: {result.form_trend}, Rating = {result.form_rating:.2f}/10")
    
    # Error Risk
    result = error_risk_calc.calculate(pressure_level=0.5, fatigue_factor=0.3, track_difficulty=0.5)
    print(f"✓ Error Risk: {result.error_probability_per_lap:.4f} per lap, {result.risk_level}")
    
    # Racecraft
    result = racecraft_calc.calculate(overtaking_success_rate=0.65, defensive_success_rate=0.70, battles_fought=12)
    print(f"✓ Racecraft: Score = {result.racecraft_score:.2f}/10")


def test_track_calculations():
    print_section("TRACK CALCULATIONS (5 modules)")
    
    # Pit Loss
    result = pit_loss_calc.calculate()
    print(f"✓ Pit Loss: {result.total_loss_s:.1f}s total ({result.stationary_time_s:.1f}s stationary)")
    
    # Overtaking Difficulty
    result = overtaking_difficulty_calc.calculate(drs_zones=2, longest_straight_m=800, track_width_m=13)
    print(f"✓ Overtaking Difficulty: {result.difficulty_rating:.2f}/10, {result.difficulty_class}")
    
    # Dirty Air Penalty
    result = dirty_air_penalty_calc.calculate(gap_s=1.5, aero_sensitivity=0.6)
    print(f"✓ Dirty Air: {result.penalty_s_per_lap:.3f}s/lap at {result.gap_s}s gap")
    
    # Track Difficulty
    result = track_difficulty_calc.calculate(corner_count=18, avg_corner_speed_kph=130, elevation_change_m=40)
    print(f"✓ Track Difficulty: {result.difficulty_rating:.2f}/10")
    
    # Safety Car Probability
    result = safety_car_probability_calc.calculate(barrier_proximity=0.7, weather_risk=0.2)
    print(f"✓ Safety Car Probability: {result.probability:.2%}")


def test_traffic_calculations():
    print_section("TRAFFIC CALCULATIONS (4 modules)")
    
    # Traffic Density
    result = traffic_density_calc.calculate(cars_on_track=20, track_length_km=5.5)
    print(f"✓ Traffic Density: {result.density_cars_per_km:.2f} cars/km, {result.density_level}")
    
    # Defense Effectiveness
    result = defense_effectiveness_calc.calculate(overtaking_difficulty=6.5, car_straight_speed=7.0, driver_defensive_skill=7.5)
    print(f"✓ Defense Effectiveness: {result.effectiveness_rating:.2f}/10")
    
    # Overtake Cost
    result = overtake_cost_calc.calculate(laps_in_battle=3, dirty_air_penalty_s=0.4, push_degradation_multiplier=1.25)
    print(f"✓ Overtake Cost: {result.time_cost_s:.2f}s, {result.tyre_life_cost_laps:.2f} laps life")
    
    # DRS Train Probability
    result = drs_train_probability_calc.calculate(cars_within_1s=3, field_spread_s=8.0, overtaking_difficulty=6.0)
    print(f"✓ DRS Train Probability: {result.train_probability:.2%}")


def test_weather_calculations():
    print_section("WEATHER CALCULATIONS (4 modules)")
    
    # Grip Evolution
    result = grip_evolution_calc.calculate(laps_completed=25, total_laps=58, initial_grip=0.88)
    print(f"✓ Grip Evolution: {result.current_grip_level:.3f} grip, {result.lap_time_delta_s:.3f}s delta")
    
    # Cooling Margin
    result = cooling_margin_calc.calculate(ambient_temp_c=32, track_temp_c=48, cooling_spec=0.6)
    print(f"✓ Cooling Margin: {result.margin:.3f}, {result.status}")
    
    # Crossover Lap
    result = crossover_lap_calc.calculate(compound_a_initial_pace=89.5, compound_b_initial_pace=89.9, compound_a_deg_rate=0.08, compound_b_deg_rate=0.04)
    print(f"✓ Crossover Lap: {result.crossover_lap if result.crossover_lap else 'No crossover'}")
    
    # Weather Volatility
    result = weather_volatility_calc.calculate(forecast_confidence=0.7, cloud_cover=0.4, wind_variability=0.3)
    print(f"✓ Weather Volatility: {result.volatility_score:.3f}, {result.volatility_level}")


def test_race_state_calculations():
    print_section("RACE STATE CALCULATIONS (4 modules)")
    
    # Gap Projection
    result = gap_projection_calc.calculate(current_gap_s=3.5, pace_delta_s=0.15, laps_remaining=20)
    print(f"✓ Gap Projection: {result.projected_gap_s:.2f}s projected, {result.laps_to_catch if result.laps_to_catch else 'N/A'} laps to catch")
    
    # Pit Window
    result = pit_window_calc.calculate(current_tyre_age=15, expected_tyre_life=28, race_laps=58, current_lap=15)
    print(f"✓ Pit Window: Optimal lap {result.optimal_lap}, Window: L{result.window_opens_lap}-{result.window_closes_lap}")
    
    # Stint State
    result = stint_state_calc.calculate(laps_on_tyre=12, expected_stint_length=25, current_pace_s=90.3, initial_pace_s=89.8)
    print(f"✓ Stint State: {result.stint_progress:.1%} complete, {result.stint_phase} phase, +{result.pace_delta_s:.2f}s degradation")
    
    # Position Pressure
    result = position_pressure_calc.calculate(gap_to_car_ahead_s=2.5, gap_to_car_behind_s=1.8, position=5)
    print(f"✓ Position Pressure: {result.pressure_rating:.2f}/10")


def test_aggregation_calculations():
    print_section("AGGREGATION CALCULATIONS (3 modules)")
    
    # Driver-Car Fusion
    result = driver_car_fusion_calc.calculate(driver_rating=7.5, car_rating=8.0, synergy_factor=0.2)
    print(f"✓ Driver-Car Fusion: Combined performance = {result.combined_performance:.2f}/10")
    
    # Tyre-Car Fusion
    result = tyre_car_fusion_calc.calculate(tyre_compound="MEDIUM", car_downforce=7.0, car_weight_kg=755, track_temp_c=32)
    print(f"✓ Tyre-Car Fusion: Pace delta = {result.expected_pace_delta_s:.3f}s, Deg rate = {result.expected_degradation_rate:.3f}")
    
    # Race Context Builder
    result = race_context_builder.calculate(
        current_lap=30, total_laps=58, current_position=6,
        gap_ahead_s=3.2, gap_behind_s=4.1, tyre_age=18,
        tyre_compound="MEDIUM", weather_condition="DRY"
    )
    print(f"✓ Race Context: {result.race_phase} phase")
    summary = race_context_builder.generate_situation_summary(result)
    print(f"  Summary: {summary}")


def run_comprehensive_test():
    print("\n" + "=" * 70)
    print("  F1 STRATEGY ENGINE - COMPREHENSIVE CALCULATION TEST")
    print("  Testing all 29 calculation modules")
    print("=" * 70)
    
    test_count = 0
    
    try:
        test_tyre_calculations()
        test_count += 5
        
        test_car_calculations()
        test_count += 5
        
        test_driver_calculations()
        test_count += 5
        
        test_track_calculations()
        test_count += 5
        
        test_traffic_calculations()
        test_count += 4
        
        test_weather_calculations()
        test_count += 4
        
        test_race_state_calculations()
        test_count += 4
        
        test_aggregation_calculations()
        test_count += 3
        
        print("\n" + "=" * 70)
        print(f"  ✓ ALL {test_count} CALCULATION MODULES TESTED SUCCESSFULLY")
        print("=" * 70)
        print("\nCalculation Engine Status:")
        print("  • Tyre Calculations: 5/5 ✓")
        print("  • Car Calculations: 5/5 ✓")
        print("  • Driver Calculations: 5/5 ✓")
        print("  • Track Calculations: 5/5 ✓")
        print("  • Traffic Calculations: 4/4 ✓")
        print("  • Weather Calculations: 4/4 ✓")
        print("  • Race State Calculations: 4/4 ✓")
        print("  • Aggregation Calculations: 3/3 ✓")
        print("\n  Total: 29/29 modules operational")
        print("=" * 70 + "\n")
        
        return True
        
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)

"""
Pit Loss Calculation
Calculates time lost during pit stop

LOGIC:
  Two components of pit loss:
  - Pit lane transit time (speed limit 80kph, ~300m pit lane)
  - Stationary time (actual stop duration, ~2.5s)
  Total loss = in-lap + stationary + out-lap - racing lap time

ROLE:
  Fundamental pit strategy metric. Determines cost of pit stops
  relative to staying out. Core input for undercut calculations.

SIGNIFICANCE:
  Single mostimportant track-specific strategy variable. Short pit
  loss circuits favor multiple stops. Long pit loss circuits
  (Monaco ~24s) strongly favor fewer stops. Drives entire strategy.
"""
from calculation_engines.interfaces.base_calculation import BaseCalculation
from calculation_engines.interfaces.calculation_output_models import PitLossOutput
from typing import Dict, Any


class PitLossCalculation(BaseCalculation):
    """
    Calculate total pit stop time loss.
    
    Components:
    - Pit lane speed limit time loss
    - Stationary time (stop duration)
    - Rejoin time loss
    """
    
    # Typical pit lane parameters
    DEFAULT_PIT_LANE_LENGTH_M = 300.0
    DEFAULT_PIT_SPEED_LIMIT_KPH = 80.0
    DEFAULT_TRACK_SPEED_KPH = 200.0
    DEFAULT_STOP_DURATION_S = 2.5
    
    @property
    def calculation_name(self) -> str:
        return "pit_loss"
    
    @property
    def description(self) -> str:
        return "Calculates time lost during pit stop"
    
    def validate_inputs(self, **kwargs) -> bool:
        """All inputs have defaults, always valid"""
        return True
    
    def calculate(
        self,
        pit_lane_length_m: float = None,
        pit_speed_limit_kph: float = None,
        track_speed_kph: float = None,
        stop_duration_s: float = None,
        **kwargs
    ) -> PitLossOutput:
        """
        Calculate pit stop time loss.
        
        Args:
            pit_lane_length_m: Length of pit lane in meters
            pit_speed_limit_kph: Pit lane speed limit (km/h)
            track_speed_kph: Average track speed (km/h)
            stop_duration_s: Stationary time in pit box (seconds)
            **kwargs: Additional parameters
            
        Returns:
            PitLossOutput with time loss breakdown
        """
        # Use defaults if not provided
        pit_lane_length_m = pit_lane_length_m or self.DEFAULT_PIT_LANE_LENGTH_M
        pit_speed_limit_kph = pit_speed_limit_kph or self.DEFAULT_PIT_SPEED_LIMIT_KPH
        track_speed_kph = track_speed_kph or self.DEFAULT_TRACK_SPEED_KPH
        stop_duration_s = stop_duration_s or self.DEFAULT_STOP_DURATION_S
        
        # Calculate time through pit lane at limit speed
        pit_lane_time_s = (pit_lane_length_m / 1000.0) / pit_speed_limit_kph * 3600.0
        
        # Calculate time if stayed on track
        track_time_s = (pit_lane_length_m / 1000.0) / track_speed_kph * 3600.0
        
        # Time lost due to speed limit
        speed_limit_loss_s = pit_lane_time_s - track_time_s
        
        # Total pit loss = speed limit loss + stop duration
        total_loss_s = speed_limit_loss_s + stop_duration_s
        
        return PitLossOutput(
            total_loss_s=total_loss_s,
            stationary_time_s=stop_duration_s
        )
    
    def calculate_optimal_pit_window(
        self,
        race_laps: int,
        tyre_life: int,
        pit_loss_s: float,
        lap_time_s: float
    ) -> Dict[str, Any]:
        """
        Calculate optimal pit window based on pit loss.
        
        Args:
            race_laps: Total race distance
            tyre_life: Expected tyre life (laps)
            pit_loss_s: Pit stop time loss
            lap_time_s: Average lap time
            
        Returns:
            Dict with pit window recommendation
        """
        # Convert pit loss to laps
        pit_loss_laps = pit_loss_s / lap_time_s
        
        # For 1-stop race, pit around mid-race accounting for tyre life
        if race_laps <= tyre_life * 2:
            # Can do 1 stop
            optimal_lap = race_laps // 2
            earliest_lap = max(10, int(optimal_lap - tyre_life * 0.2))
            latest_lap = min(race_laps - 5, int(optimal_lap + tyre_life * 0.2))
            
            return {
                'strategy': '1_stop',
                'optimal_lap': optimal_lap,
                'window_earliest': earliest_lap,
                'window_latest': latest_lap,
                'pit_loss_laps': pit_loss_laps
            }
        else:
            # Need 2+ stops
            num_stops = (race_laps // tyre_life) + 1
            return {
                'strategy': f'{num_stops}_stop',
                'pit_loss_laps': pit_loss_laps,
                'total_time_lost_s': pit_loss_s * num_stops
            }


# Singleton instance
pit_loss_calc = PitLossCalculation()

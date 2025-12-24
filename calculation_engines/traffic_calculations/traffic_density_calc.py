"""
Traffic Density Calculation
Measures congestion level on track

LOGIC:
  Calculates cars per kilometer of track:
  - Density = total_cars / track_length_km
  - Also uses average gap for density estimation
  - Classified: sparse (<3 cars/km), moderate (3-4), dense (>4)

ROLE:
  Traffic quantification metric. Determines likelihood of
  encountering traffic and impact on strategy execution.

SIGNIFICANCE:
  High density increases risk of emerging into traffic after
  pit stop. Affects optimal pit window timing. Monaco (~6 cars/km)
  makes traffic management critical. Spa (~3 cars/km) more freedom.
"""
from calculation_engines.interfaces.base_calculation import BaseCalculation
from calculation_engines.interfaces.calculation_output_models import TrafficDensityOutput
from typing import Dict, Any


class TrafficDensityCalculation(BaseCalculation):
    """
    Calculate track traffic density.
    
    Higher density = more cars per track sector = more traffic issues
    """
    
    @property
    def calculation_name(self) -> str:
        return "traffic_density"
    
    @property
    def description(self) -> str:
        return "Measures congestion level on track"
    
    def validate_inputs(
        self,
        cars_on_track: int = None,
        track_length_km: float = None,
        **kwargs
    ) -> bool:
        """Validate traffic parameters"""
        if cars_on_track is None or track_length_km is None:
            return False
        return cars_on_track > 0 and track_length_km > 0
    
    def calculate(
        self,
        cars_on_track: int,
        track_length_km: float,
        avg_gap_s: float = 1.0,
        **kwargs
    ) -> TrafficDensityOutput:
        """
        Calculate traffic density.
        
        Args:
            cars_on_track: Number of cars currently on track
            track_length_km: Circuit length in kilometers
            avg_gap_s: Average gap between cars (seconds)
            **kwargs: Additional parameters
            
        Returns:
            TrafficDensityOutput with density metrics
        """
        # Clamp inputs
        cars_on_track = max(1, min(30, cars_on_track))
        track_length_km = max(2.0, min(10.0, track_length_km))
        avg_gap_s = max(0.1, avg_gap_s)
        
        # Calculate cars per kilometer
        density = cars_on_track / track_length_km
        
        # Classify density
        # Monaco (3.3km): 20 cars = 6.1 cars/km (very high)
        # Spa (7.0km): 20 cars = 2.9 cars/km (moderate)
        if density > 5.0:
            density_level = "very_high"
        elif density > 4.0:
            density_level = "high"
        elif density > 3.0:
            density_level = "moderate"
        else:
            density_level = "low"
        
        return TrafficDensityOutput(
            density_cars_per_km=density,
            density_level=density_level
        )
    
    def estimate_traffic_impact(
        self,
        density: float,
        driver_position: int,
        total_cars: int = 20
    ) -> Dict[str, Any]:
        """
        Estimate lap time impact from traffic.
        
        Args:
            density: Traffic density (cars/km)
            driver_position: Current position
            total_cars: Total cars in race
            
        Returns:
            Dict with traffic impact estimation
        """
        # Midfield drivers encounter more traffic
        # Leaders and backmarkers less affected
        
        # Position factor (midfield = 1.0, extremes = 0.3)
        mid_position = total_cars / 2
        position_delta = abs(driver_position - mid_position)
        position_factor = max(0.3, 1.0 - (position_delta / mid_position * 0.7))
        
        # Base traffic penalty (seconds per lap)
        # High density = more time lost
        base_penalty = min(1.0, density / 10.0)  # Up to 1s per lap
        
        # Calculate effective penalty
        traffic_penalty_s = base_penalty * position_factor
        
        return {
            'traffic_penalty_s_per_lap': traffic_penalty_s,
            'density': density,
            'position_factor': position_factor,
            'affected_most': 'midfield' if position_factor > 0.7 else 'minimal'
        }


# Singleton instance
traffic_density_calc = TrafficDensityCalculation()

"""
Battle Forecast System
Predicts overtaking opportunities and battle outcomes
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class BattlePrediction(BaseModel):
    """Output model for battle prediction"""
    overtake_probability: float = Field(ge=0, le=1, description="Probability of successful overtake")
    best_overtake_zone: str = Field(description="Track zone with best overtaking chance")
    speed_advantage: float = Field(description="Speed advantage in overtake zone (km/h)")
    drs_available: bool = Field(description="Whether DRS is available")
    difficulty_rating: float = Field(ge=0, le=10, description="Overtaking difficulty (0=easy, 10=impossible)")
    recommended_strategy: str = Field(description="Strategic recommendation")
    key_factors: List[str] = Field(description="Key factors affecting overtake probability")


class BattleForecast:
    """
    Predicts battle outcomes and overtaking opportunities.
    
    LOGIC:
    - Analyzes speed deltas in DRS zones and braking zones
    - Calculates overtaking probability based on historical data
    - Identifies optimal overtaking locations on track
    - Considers track characteristics and car performance
    
    ROLE:
    - Predicts overtaking opportunities during race
    - Helps strategists decide attack/defend modes
    - Identifies critical battle locations
    
    SIGNIFICANCE:
    - Critical for race strategy decisions
    - Predicts position changes before they happen
    - Informs tyre management and battery deployment
    """
    
    @staticmethod
    def predict_overtake(attacking_tel: pd.DataFrame, defending_tel: pd.DataFrame,
                        gap_s: float, drs_available: bool = True,
                        track_difficulty: float = 5.0) -> BattlePrediction:
        """
        Predict overtaking probability.
        
        Args:
            attacking_tel: Telemetry of attacking car
            defending_tel: Telemetry of defending car
            gap_s: Current gap in seconds
            drs_available: Whether attacker has DRS
            track_difficulty: Track overtaking difficulty (0-10)
            
        Returns:
            BattlePrediction with analysis and recommendation
        """
        # Analyze speed advantages in key zones
        straight_zones = BattleForecast._identify_straight_zones(attacking_tel)
        brake_zones = BattleForecast._identify_brake_zones(attacking_tel)
        
        # Calculate speed deltas
        speed_deltas = []
        best_zone = None
        max_advantage = 0.0
        
        for zone_type, zones in [('straight', straight_zones), ('braking', brake_zones)]:
            for idx, zone in enumerate(zones):
                att_speed = attacking_tel[
                    (attacking_tel['Distance'] >= zone['start']) &
                    (attacking_tel['Distance'] <= zone['end'])
                ]['Speed'].mean()
                
                def_speed = defending_tel[
                    (defending_tel['Distance'] >= zone['start']) &
                    (defending_tel['Distance'] <= zone['end'])
                ]['Speed'].mean()
                
                advantage = att_speed - def_speed
                speed_deltas.append(advantage)
                
                if abs(advantage) > max_advantage:
                    max_advantage = abs(advantage)
                    best_zone = f"{zone_type.title()} Zone {idx + 1}"
        
        avg_speed_advantage = np.mean(speed_deltas) if speed_deltas else 0.0
        
        # DRS boost (typically +10-15 km/h)
        if drs_available:
            avg_speed_advantage += 12.0
        
        # Calculate overtake probability
        # Based on: gap, speed advantage, track difficulty
        probability = BattleForecast._calculate_probability(
            gap_s, avg_speed_advantage, track_difficulty, drs_available
        )
        
        # Difficulty rating
        difficulty = min(10.0, track_difficulty + (gap_s * 2) - (avg_speed_advantage / 5))
        difficulty = max(0.0, difficulty)
        
        # Strategic recommendation
        if probability > 0.7:
            strategy = "ATTACK - High probability of successful overtake"
        elif probability > 0.4:
            strategy = "PREPARE - Monitor and wait for opportunity"
        else:
            strategy = "DEFEND - Focus on maintaining position"
        
        # Key factors
        factors = []
        if gap_s < 1.0:
            factors.append("Within DRS range")
        if avg_speed_advantage > 5.0:
            factors.append("Significant speed advantage")
        if track_difficulty < 5.0:
            factors.append("Track favors overtaking")
        if drs_available:
            factors.append("DRS available")
        if gap_s > 2.0:
            factors.append("Gap too large - need multiple laps")
        
        return BattlePrediction(
            overtake_probability=probability,
            best_overtake_zone=best_zone or "Unknown",
            speed_advantage=avg_speed_advantage,
            drs_available=drs_available,
            difficulty_rating=difficulty,
            recommended_strategy=strategy,
            key_factors=factors
        )
    
    @staticmethod
    def _identify_straight_zones(telemetry: pd.DataFrame) -> List[Dict]:
        """Identify straight sections for overtaking"""
        straights = []
        in_straight = False
        start_dist = None
        
        for idx, row in telemetry.iterrows():
            if row['Speed'] > 250 and not in_straight:
                in_straight = True
                start_dist = row['Distance']
            elif row['Speed'] <= 250 and in_straight:
                in_straight = False
                straights.append({'start': start_dist, 'end': row['Distance']})
        
        return straights
    
    @staticmethod
    def _identify_brake_zones(telemetry: pd.DataFrame) -> List[Dict]:
        """Identify braking zones for overtaking"""
        brake_zones = []
        in_brake = False
        start_dist = None
        
        if 'Brake' not in telemetry.columns:
            return []
        
        for idx, row in telemetry.iterrows():
            if row['Brake'] and not in_brake:
                in_brake = True
                start_dist = row['Distance']
            elif not row['Brake'] and in_brake:
                in_brake = False
                brake_zones.append({'start': start_dist, 'end': row['Distance']})
        
        return brake_zones
    
    @staticmethod
    def _calculate_probability(gap_s: float, speed_adv: float, 
                               track_diff: float, drs: bool) -> float:
        """
        Calculate overtaking probability.
        
        Formula considers:
        - Gap (smaller = higher probability)
        - Speed advantage (larger = higher probability)
        - Track difficulty (lower = higher probability)
        - DRS availability (yes = higher probability)
        """
        # Base probability from gap
        if gap_s < 0.5:
            gap_factor = 0.8
        elif gap_s < 1.0:
            gap_factor = 0.6
        elif gap_s < 2.0:
            gap_factor = 0.3
        else:
            gap_factor = 0.1
        
        # Speed advantage factor
        speed_factor = min(1.0, speed_adv / 20.0)  # 20 km/h = max factor
        
        # Track factor
        track_factor = 1.0 - (track_diff / 10.0)
        
        # DRS bonus
        drs_bonus = 0.2 if drs else 0.0
        
        # Combined probability
        probability = (gap_factor * 0.4 + speed_factor * 0.3 + 
                      track_factor * 0.2 + drs_bonus)
        
        return min(1.0, max(0.0, probability))
    
    @staticmethod
    def analyze_battle_progression(attacker_laps: pd.DataFrame, 
                                   defender_laps: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze how a battle progresses over multiple laps.
        
        Args:
            attacker_laps: Lap data of attacking driver
            defender_laps: Lap data of defending driver
            
        Returns:
            Dict with battle progression analysis
        """
        # Convert lap times to seconds
        attacker_laps = attacker_laps.copy()
        defender_laps = defender_laps.copy()
        
        attacker_laps['LapTimeSec'] = attacker_laps['LapTime'].dt.total_seconds()
        defender_laps['LapTimeSec'] = defender_laps['LapTime'].dt.total_seconds()
        
        # Calculate pace difference
        pace_diff = attacker_laps['LapTimeSec'].mean() - defender_laps['LapTimeSec'].mean()
        
        # Estimate laps to close gap (if attacker is faster)
        if pace_diff < 0:  # Attacker is faster
            laps_to_close = abs(1.0 / pace_diff)  # 1 second gap
            closing_rate = abs(pace_diff)
        else:
            laps_to_close = float('inf')
            closing_rate = 0.0
        
        return {
            'pace_difference': pace_diff,
            'attacker_faster': pace_diff < 0,
            'closing_rate_per_lap': closing_rate,
            'laps_to_drs_range': laps_to_close if laps_to_close != float('inf') else None,
            'battle_duration_estimate': min(laps_to_close + 3, 10) if laps_to_close != float('inf') else None
        }

"""
DRS Train Probability Calculation
Predicts likelihood of DRS train formation

LOGIC:
  Analyzes conditions for DRS train (multiple cars within DRS range):
  - Count of cars within 1 second gaps
  - Overall field spread compression
  - Track overtaking difficulty (harder = more trains)
  Probability based on cluster formation tendency

ROLE:
  DRS train risk assessment. Trains neutralize DRS advantage
  and create strategic complications.

SIGNIFICANCE:
  DRS trains can trap faster cars mid-field, negating pace
  advantage. Affects pit stop timing to avoid emerging into
  trains. High train probability favors early or late strategy.
"""
from calculation_engines.interfaces.base_calculation import BaseCalculation
from calculation_engines.interfaces.calculation_output_models import TrainProbabilityOutput
from typing import Dict, Any


class DRSTrainProbabilityCalculation(BaseCalculation):
    """
    Calculate probability of DRS train formation.
    
    DRS train = multiple cars within 1s, all with DRS, neutralizing advantage
    """
    
    @property
    def calculation_name(self) -> str:
        return "drs_train_probability"
    
    @property
    def description(self) -> str:
        return "Predicts likelihood of DRS train formation"
    
    def validate_inputs(
        self,
        cars_within_1s: int = None,
        **kwargs
    ) -> bool:
        """Validate car count"""
        if cars_within_1s is None:
            return False
        return cars_within_1s >= 0
    
    def calculate(
        self,
        cars_within_1s: int,
        field_spread_s: float = 10.0,
        overtaking_difficulty: float = 5.0,
        **kwargs
    ) -> TrainProbabilityOutput:
        """
        Calculate DRS train probability.
        
        Args:
            cars_within_1s: Number of cars within 1 second
            field_spread_s: Total field spread (leader to last, seconds)
            overtaking_difficulty: Track overtaking difficulty (0-10)
            **kwargs: Additional parameters
            
        Returns:
            TrainProbabilityOutput with train probability
        """
        # Clamp inputs
        cars_within_1s = max(0, cars_within_1s)
        field_spread_s = max(1.0, field_spread_s)
        overtaking_difficulty = max(0.0, min(10.0, overtaking_difficulty))
        
        # More cars close together = higher train probability
        # 3+ cars within 1s = likely train
        if cars_within_1s >= 3:
            base_probability = 0.7
        elif cars_within_1s == 2:
            base_probability = 0.4
        elif cars_within_1s == 1:
            base_probability = 0.1
        else:
            base_probability = 0.0
        
        # Tight field increases probability
        # Spread < 5s = 1.3x, spread > 20s = 0.7x
        if field_spread_s < 5.0:
            spread_multiplier = 1.3
        elif field_spread_s > 20.0:
            spread_multiplier = 0.7
        else:
            # Linear interpolation
            spread_multiplier = 1.3 - ((field_spread_s - 5.0) / 15.0 * 0.6)
        
        # Harder overtaking tracks = trains persist longer
        # Difficulty 8+ = 1.2x, difficulty 2- = 0.8x
        if overtaking_difficulty > 7:
            difficulty_multiplier = 1.2
        elif overtaking_difficulty < 3:
            difficulty_multiplier = 0.8
        else:
            difficulty_multiplier = 1.0
        
        # Calculate overall probability
        train_probability = (
            base_probability *
            spread_multiplier *
            difficulty_multiplier
        )
        
        # Clamp to 0-1
        train_probability = max(0.0, min(1.0, train_probability))
        
        return TrainProbabilityOutput(
            train_probability=train_probability
        )
    
    def estimate_train_impact(
        self,
        train_probability: float,
        cars_in_train: int,
        laps_in_train: int
    ) -> Dict[str, Any]:
        """
        Estimate impact of being stuck in DRS train.
        
        Args:
            train_probability: Probability of train (0-1)
            cars_in_train: Number of cars in train
            laps_in_train: Expected laps stuck in train
            
        Returns:
            Dict with train impact assessment
        """
        # Time lost per lap in train (dirty air, no overtaking)
        time_loss_per_lap = 0.3  # Seconds
        
        # Expected total time loss
        expected_time_loss = (
            train_probability *
            laps_in_train *
            time_loss_per_lap
        )
        
        # Strategic implications
        if train_probability > 0.6:
            strategy_note = "High train risk - pit early to avoid"
        elif train_probability > 0.3:
            strategy_note = "Moderate train risk - monitor closely"
        else:
            strategy_note = "Low train risk"
        
        return {
            'train_probability': train_probability,
            'cars_in_train': cars_in_train,
            'expected_laps_stuck': laps_in_train,
            'expected_time_loss_s': expected_time_loss,
            'strategy_note': strategy_note
        }


# Singleton instance
drs_train_probability_calc = DRSTrainProbabilityCalculation()

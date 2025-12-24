"""
Racecraft Score Calculation
Evaluates driver's wheel-to-wheel racing ability

LOGIC:
  Composite score (0-10) from three components:
  - Overtaking rating: success_rate * 10 (attack ability)
  - Defensive rating: defensive_success_rate * 10 (position holding)
  - Battle efficiency: inverted time loss metric
  Weighted average with battle count factor

ROLE:
  Quantifies driver quality in traffic. Separates qualifying
  pace from race craft ability.

SIGNIFICANCE:
  Critical for evaluating alternative strategies involving battles.
  Strong racecraft enables risky strategies (early stop, traffic).
  Weak racecraft favors track position priority strategies.
"""
from calculation_engines.interfaces.base_calculation import BaseCalculation
from calculation_engines.interfaces.calculation_output_models import RacecraftOutput
from typing import Dict, Any


class RacecraftCalculation(BaseCalculation):
    """
    Calculate driver racecraft rating.
    
    Racecraft encompasses:
    - Overtaking skill
    - Defensive ability
    - Tire management in traffic
    - Battle efficiency (gaining positions vs losing time)
    """
    
    @property
    def calculation_name(self) -> str:
        return "racecraft_score"
    
    @property
    def description(self) -> str:
        return "Evaluates driver's wheel-to-wheel racing ability"
    
    def validate_inputs(
        self,
        overtaking_success_rate: float = None,
        defensive_success_rate: float = None,
        **kwargs
    ) -> bool:
        """Validate racecraft metrics"""
        if overtaking_success_rate is None or defensive_success_rate is None:
            return False
        return 0.0 <= overtaking_success_rate <= 1.0 and 0.0 <= defensive_success_rate <= 1.0
    
    def calculate(
        self,
        overtaking_success_rate: float,
        defensive_success_rate: float,
        battles_fought: int = 10,
        avg_time_lost_per_battle: float = 0.5,
        **kwargs
    ) -> RacecraftOutput:
        """
        Calculate racecraft score.
        
        Args:
            overtaking_success_rate: Success rate in overtake attempts (0-1)
            defensive_success_rate: Success rate defending position (0-1)
            battles_fought: Number of battles in sample
            avg_time_lost_per_battle: Average time lost per battle (seconds)
            **kwargs: Additional parameters
            
        Returns:
            RacecraftOutput with racecraft rating
        """
        # Clamp inputs
        overtaking_success_rate = max(0.0, min(1.0, overtaking_success_rate))
        defensive_success_rate = max(0.0, min(1.0, defensive_success_rate))
        battles_fought = max(1, battles_fought)
        avg_time_lost_per_battle = max(0.0, avg_time_lost_per_battle)
        
        # Calculate component scores (0-10 scale)
        
        # Overtaking score
        # 50% success rate = 5.0, 100% = 10.0, 0% = 0.0
        overtaking_score = overtaking_success_rate * 10.0
        
        # Defensive score
        defensive_score = defensive_success_rate * 10.0
        
        # Efficiency score (minimize time lost in battles)
        # 0.2s per battle = 10.0 (very efficient)
        # 1.0s per battle = 0.0 (very inefficient)
        if avg_time_lost_per_battle <= 0.2:
            efficiency_score = 10.0
        elif avg_time_lost_per_battle >= 1.0:
            efficiency_score = 0.0
        else:
            # Linear interpolation
            efficiency_score = 10.0 - ((avg_time_lost_per_battle - 0.2) / 0.8 * 10.0)
        
        efficiency_score = max(0.0, min(10.0, efficiency_score))
        
        # Battle frequency bonus (more battles = more data, more racecraft experience)
        # 5 battles = 1.0x, 20+ battles = 1.1x
        frequency_multiplier = 1.0 + min(0.1, (battles_fought - 5) / 150.0)
        
        # Calculate composite racecraft score
        # Weight: 40% overtaking, 30% defense, 30% efficiency
        racecraft_score = (
            (overtaking_score * 0.40 +
             defensive_score * 0.30 +
             efficiency_score * 0.30) *
            frequency_multiplier
        )
        
        racecraft_score = max(0.0, min(10.0, racecraft_score))
        
        return RacecraftOutput(
            racecraft_score=racecraft_score,
            overtaking_rating=overtaking_score,
            defensive_rating=defensive_score,
            battle_efficiency=efficiency_score
        )
    
    def classify_racecraft_style(
        self,
        overtaking_rating: float,
        defensive_rating: float,
        battle_efficiency: float
    ) -> Dict[str, Any]:
        """
        Classify driver's racecraft style.
        
        Args:
            overtaking_rating: Overtaking score (0-10)
            defensive_rating: Defensive score (0-10)
            battle_efficiency: Efficiency score (0-10)
            
        Returns:
            Dict with style classification
        """
        # Determine primary strength
        if overtaking_rating > defensive_rating + 2:
            style = "aggressive_attacker"
            description = "Excels at overtaking, prioritizes attack"
        elif defensive_rating > overtaking_rating + 2:
            style = "defensive_specialist"
            description = "Strong defender, holds position well"
        elif battle_efficiency >= 7.0:
            style = "efficient_racer"
            description = "Minimizes time loss in battles"
        elif overtaking_rating >= 7.0 and defensive_rating >= 7.0:
            style = "complete_racer"
            description = "Well-rounded wheel-to-wheel skills"
        else:
            style = "developing"
            description = "Building racecraft experience"
        
        # Overall rating
        avg_rating = (overtaking_rating + defensive_rating + battle_efficiency) / 3.0
        
        if avg_rating >= 8.0:
            overall = "elite"
        elif avg_rating >= 6.0:
            overall = "strong"
        elif avg_rating >= 4.0:
            overall = "competent"
        else:
            overall = "needs_improvement"
        
        return {
            'style': style,
            'description': description,
            'overall_rating': overall,
            'avg_score': avg_rating
        }


# Singleton instance
racecraft_calc = RacecraftCalculation()

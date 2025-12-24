"""
Reliability Risk Calculation
Assesses mechanical failure risk based on component usage and stress

LOGIC:
  Exponential risk model based on component age:
  - Risk increases exponentially with age/mileage
  - Formula: base_rate * e^(age_ratio * 2.0) * stress_multiplier
  - Components beyond max life face severe penalties
  - Stress level (0-1) multiplies base risk

ROLE:
  Component life management. Prevents unrealistic strategies that
  ignore PU/gearbox penalties. Balances performance vs reliability.

SIGNIFICANCE:
  Models real F1 constraint - grid penalties for component changes.
  Influences when to take strategic penalties. Critical for
  season-long simulations and component allocation strategy.
"""
from calculation_engines.interfaces.base_calculation import BaseCalculation
from calculation_engines.interfaces.calculation_output_models import ReliabilityRiskOutput
from typing import Dict, Any


class ReliabilityRiskCalculation(BaseCalculation):
    """
    Calculate reliability failure risk.
    
    Considers:
    - Component age (mileage/events)
    - Operating stress levels
    - Historical failure rates
    - Penalty for exceeding component allocation
    """
    
    # Risk thresholds (0-1 scale)
    LOW_RISK_THRESHOLD = 0.2
    MEDIUM_RISK_THRESHOLD = 0.5
    HIGH_RISK_THRESHOLD = 0.8
    
    @property
    def calculation_name(self) -> str:
        return "reliability_risk"
    
    @property
    def description(self) -> str:
        return "Assesses mechanical failure risk from component usage"
    
    def validate_inputs(
        self,
        component_age_events: int = None,
        max_component_life: int = None,
        **kwargs
    ) -> bool:
        """Validate component parameters"""
        if component_age_events is None or max_component_life is None:
            return False
        return component_age_events >= 0 and max_component_life > 0
    
    def calculate(
        self,
        component_age_events: int,
        max_component_life: int,
        stress_level: float = 0.5,
        base_failure_rate: float = 0.05,
        **kwargs
    ) -> ReliabilityRiskOutput:
        """
        Calculate reliability risk score.
        
        Args:
            component_age_events: Events/races on current component
            max_component_life: Maximum allowed events before penalty
            stress_level: Operating stress (0-1, 0=easy, 1=maximum)
            base_failure_rate: Historical failure rate (0-1)
            **kwargs: Additional parameters
            
        Returns:
            ReliabilityRiskOutput with risk assessment
        """
        # Clamp inputs
        component_age_events = max(0, component_age_events)
        stress_level = max(0.0, min(1.0, stress_level))
        base_failure_rate = max(0.0, min(1.0, base_failure_rate))
        
        # Calculate age factor (exponential increase near end of life)
        age_ratio = component_age_events / max(max_component_life, 1)
        
        # Risk increases exponentially as component ages
        # New component: low risk, old component: high risk
        import math
        age_risk_factor = math.exp(age_ratio * 2) - 1  # e^(2*ratio) - 1
        age_risk_factor = min(age_risk_factor, 5.0)  # Cap at 5x
        
        # Penalty for exceeding allocation
        if component_age_events > max_component_life:
            over_limit = component_age_events - max_component_life
            penalty_multiplier = 1.0 + (over_limit * 0.5)  # +50% per event over
        else:
            penalty_multiplier = 1.0
        
        # Stress multiplier (operating at high stress increases failure risk)
        stress_multiplier = 1.0 + (stress_level * 0.5)  # Up to +50% for max stress
        
        # Calculate overall failure probability
        failure_probability = (
            base_failure_rate * 
            age_risk_factor * 
            penalty_multiplier * 
            stress_multiplier
        )
        
        # Clamp to 0-1
        failure_probability = max(0.0, min(1.0, failure_probability))
        
        # Classify risk level
        if failure_probability < self.LOW_RISK_THRESHOLD:
            risk_level = "low"
        elif failure_probability < self.MEDIUM_RISK_THRESHOLD:
            risk_level = "medium"
        elif failure_probability < self.HIGH_RISK_THRESHOLD:
            risk_level = "high"
        else:
            risk_level = "critical"
        
        return ReliabilityRiskOutput(
            failure_probability=failure_probability,
            risk_level=risk_level
        )
    
    def calculate_component_recommendation(
        self,
        current_age: int,
        max_life: int,
        upcoming_events: int,
        critical_events: list = None
    ) -> Dict[str, Any]:
        """
        Recommend whether to change component before upcoming events.
        
        Args:
            current_age: Current component age (events)
            max_life: Maximum component life
            upcoming_events: Number of upcoming events
            critical_events: List of event indices that are critical (e.g., [2, 5])
            
        Returns:
            Dict with recommendation and reasoning
        """
        if critical_events is None:
            critical_events = []
        
        # Project risk for each upcoming event
        event_risks = []
        for event_idx in range(upcoming_events):
            age_at_event = current_age + event_idx + 1
            risk_result = self.calculate(
                component_age_events=age_at_event,
                max_component_life=max_life,
                stress_level=0.7 if event_idx in critical_events else 0.5
            )
            event_risks.append({
                'event': event_idx + 1,
                'age': age_at_event,
                'risk': risk_result.failure_probability,
                'risk_level': risk_result.risk_level,
                'is_critical_event': event_idx in critical_events
            })
        
        # Determine recommendation
        max_risk = max(r['risk'] for r in event_risks)
        has_high_risk = any(r['risk_level'] in ['high', 'critical'] for r in event_risks)
        critical_event_at_risk = any(
            r['risk_level'] in ['medium', 'high', 'critical'] and r['is_critical_event']
            for r in event_risks
        )
        
        if critical_event_at_risk or has_high_risk:
            recommendation = "change_component"
            reason = "High failure risk detected"
            if critical_event_at_risk:
                reason += " at critical event"
        elif max_risk > self.MEDIUM_RISK_THRESHOLD:
            recommendation = "monitor_closely"
            reason = "Medium risk, consider strategic change"
        else:
            recommendation = "continue"
            reason = "Risk acceptable for upcoming events"
        
        return {
            'recommendation': recommendation,
            'reason': reason,
            'event_risks': event_risks,
            'max_risk': max_risk
        }


# Singleton instance
reliability_risk_calc = ReliabilityRiskCalculation()

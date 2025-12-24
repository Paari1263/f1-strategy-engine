"""
Race Context Builder
Aggregates all race state information into unified context

LOGIC:
  Comprehensive race state aggregation:
  - Current position, lap, gaps (positional data)
  - Tyre age, compound, condition (tyre data)
  - Weather, track conditions (environmental data)
  - Race phase: opening/mid-race/closing/final-laps
  - Generates human-readable situation summary

ROLE:
  Unified state representation. Single source of truth for
  current race situation. Enables context-aware decisions.

SIGNIFICANCE:
  Foundation for strategy_engines layer (future). Provides all
  necessary context for AI decision making. Essential for
  generating natural language race updates and strategic insights.
"""
from calculation_engines.interfaces.base_calculation import BaseCalculation
from calculation_engines.interfaces.calculation_output_models import RaceContextOutput
from typing import Dict, Any, Optional


class RaceContextBuilder(BaseCalculation):
    """
    Build comprehensive race context.
    
    Aggregates:
    - Position and gaps
    - Tyre state
    - Weather conditions
    - Strategic pressure
    - Time remaining
    """
    
    @property
    def calculation_name(self) -> str:
        return "race_context_builder"
    
    @property
    def description(self) -> str:
        return "Aggregates all race state into unified context"
    
    def validate_inputs(
        self,
        current_lap: int = None,
        total_laps: int = None,
        **kwargs
    ) -> bool:
        """Validate lap inputs"""
        if current_lap is None or total_laps is None:
            return False
        return 0 <= current_lap <= total_laps
    
    def calculate(
        self,
        current_lap: int,
        total_laps: int,
        current_position: int = 10,
        gap_ahead_s: float = 5.0,
        gap_behind_s: float = 5.0,
        tyre_age: int = 10,
        tyre_compound: str = "MEDIUM",
        weather_condition: str = "DRY",
        **kwargs
    ) -> RaceContextOutput:
        """
        Build race context.
        
        Args:
            current_lap: Current lap number
            total_laps: Total race laps
            current_position: Current position
            gap_ahead_s: Gap to car ahead
            gap_behind_s: Gap to car behind
            tyre_age: Current tyre age
            tyre_compound: Current compound
            weather_condition: Current weather
            **kwargs: Additional parameters
            
        Returns:
            RaceContextOutput with comprehensive context
        """
        # Calculate race phase
        race_progress = current_lap / max(total_laps, 1)
        
        if race_progress < 0.2:
            race_phase = "opening"
        elif race_progress < 0.5:
            race_phase = "middle"
        elif race_progress < 0.8:
            race_phase = "late"
        else:
            race_phase = "closing"
        
        # Strategic state
        if current_position <= 3:
            strategic_importance = "critical"  # Podium
        elif current_position <= 10:
            strategic_importance = "high"  # Points
        else:
            strategic_importance = "moderate"
        
        # Battle state
        in_battle = gap_ahead_s < 3.0 or gap_behind_s < 3.0
        
        # Tyre state
        if tyre_age < 10:
            tyre_condition = "fresh"
        elif tyre_age < 20:
            tyre_condition = "used"
        elif tyre_age < 30:
            tyre_condition = "worn"
        else:
            tyre_condition = "critical"
        
        # Build context dict
        context = {
            'race_phase': race_phase,
            'race_progress': race_progress,
            'laps_remaining': total_laps - current_lap,
            'position': current_position,
            'strategic_importance': strategic_importance,
            'in_battle': in_battle,
            'gap_ahead_s': gap_ahead_s,
            'gap_behind_s': gap_behind_s,
            'tyre_age': tyre_age,
            'tyre_compound': tyre_compound,
            'tyre_condition': tyre_condition,
            'weather': weather_condition
        }
        
        return RaceContextOutput(
            race_phase=race_phase,
            context_data=context
        )
    
    def generate_situation_summary(
        self,
        context: RaceContextOutput
    ) -> str:
        """
        Generate human-readable situation summary.
        
        Args:
            context: Race context
            
        Returns:
            Situation summary string
        """
        data = context.context_data
        
        summary_parts = []
        
        # Race phase
        summary_parts.append(f"Lap {data.get('laps_remaining', 0)} to go ({context.race_phase} phase)")
        
        # Position
        pos = data.get('position', 0)
        if pos <= 3:
            pos_str = f"P{pos} (podium position)"
        elif pos <= 10:
            pos_str = f"P{pos} (points position)"
        else:
            pos_str = f"P{pos}"
        summary_parts.append(pos_str)
        
        # Battle state
        if data.get('in_battle'):
            summary_parts.append("in wheel-to-wheel battle")
        
        # Tyre state
        tyre_desc = f"{data.get('tyre_age', 0)} laps on {data.get('tyre_compound', 'unknown')} ({data.get('tyre_condition', 'unknown')})"
        summary_parts.append(tyre_desc)
        
        # Weather
        if data.get('weather', 'DRY') != 'DRY':
            summary_parts.append(f"weather: {data.get('weather')}")
        
        return ", ".join(summary_parts)


# Singleton instance
race_context_builder = RaceContextBuilder()

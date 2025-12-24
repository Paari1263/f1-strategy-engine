"""
Report Generator
Generates formatted analysis reports in text/markdown format
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime


class ReportGenerator:
    """
    Generates formatted analysis reports.
    
    Produces:
    - Executive summaries
    - Detailed technical reports
    - Strategy briefings
    - Race debriefs
    """
    
    @staticmethod
    def generate_car_comparison_report(result: Dict[str, Any],
                                       output_path: Optional[str] = None) -> str:
        """
        Generate formatted car comparison report.
        
        Args:
            result: Car comparison result dictionary
            output_path: Optional path to save report
            
        Returns:
            Formatted report string
        """
        session_info = result['session_info']
        speed = result['speed_analysis']
        braking = result['braking_analysis']
        corner = result['corner_analysis']
        straight = result['straight_line_analysis']
        
        report = f"""
╔══════════════════════════════════════════════════════════════════════╗
║                   F1 CAR COMPARISON REPORT                           ║
╚══════════════════════════════════════════════════════════════════════╝

📊 SESSION INFORMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Event:           {session_info['year']} {session_info['gp']}
  Session:         {session_info['session']}
  Comparison:      {session_info['driver1']} vs {session_info['driver2']}
  
⏱️  LAP TIME DELTA:  {session_info['lap_time_delta']:+.3f}s
🏆 OVERALL WINNER:  {result['overall_advantage']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 SPEED ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Top Speed Delta:        {speed['top_speed_delta']:+.1f} km/h
  Straight Speed Delta:   {speed['straight_speed_delta']:+.1f} km/h
  Corner Speed Delta:     {speed['corner_speed_delta']:+.1f} km/h
  Efficiency Delta:       {speed['efficiency_delta']:+.2f}/10
  
  Advantage:              {speed['advantage']}
  {session_info['driver1']} Profile:       {speed['profile1']}
  {session_info['driver2']} Profile:       {speed['profile2']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🛑 BRAKING ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Brake Distance Delta:   {braking['brake_distance_delta']:+.1f}m
  Max Decel Delta:        {braking['max_decel_delta']:+.2f} m/s²
  Late Braking Delta:     {braking['late_braking_delta']:+.2f}/10
  Stability Delta:        {braking['stability_delta']:+.2f}/10
  
  Advantage:              {braking['advantage']}
  Reason:                 {braking['advantage_reason']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏁 CORNERING ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Apex Speed Delta:       {corner['apex_speed_delta']:+.1f} km/h
  Entry Speed Delta:      {corner['entry_speed_delta']:+.1f} km/h
  Exit Speed Delta:       {corner['exit_speed_delta']:+.1f} km/h
  Corner Efficiency:      {corner['corner_efficiency_delta']:+.2f}/10
  Exit Performance:       {corner['exit_performance_delta']:+.2f}/10
  
  Advantage:              {corner['advantage']}
  Downforce:              {corner['downforce_comparison']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 STRAIGHT LINE ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Top Speed Delta:        {straight['top_speed_delta']:+.1f} km/h
  Avg Speed Delta:        {straight['avg_speed_delta']:+.1f} km/h
  Acceleration Delta:     {straight['acceleration_delta']:+.2f}/10
  Power Delta:            {straight['power_delta']:+.2f}/10
  
  Advantage:              {straight['advantage']}
  Drag Comparison:        {straight['drag_comparison']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 ADVANTAGE SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Speed:         {result['advantage_areas']['speed']}
  Braking:       {result['advantage_areas']['braking']}
  Cornering:     {result['advantage_areas']['cornering']}
  Straight Line: {result['advantage_areas']['straight_line']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
        
        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                f.write(report)
        
        return report
    
    @staticmethod
    def generate_driver_comparison_report(result: Dict[str, Any],
                                         output_path: Optional[str] = None) -> str:
        """
        Generate formatted driver comparison report.
        
        Args:
            result: Driver comparison result dictionary
            output_path: Optional path to save report
            
        Returns:
            Formatted report string
        """
        session_info = result['session_info']
        pace = result['pace_analysis']
        consistency = result['consistency_analysis']
        
        report = f"""
╔══════════════════════════════════════════════════════════════════════╗
║                 F1 DRIVER COMPARISON REPORT                          ║
╚══════════════════════════════════════════════════════════════════════╝

📊 SESSION INFORMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Event:           {session_info['year']} {session_info['gp']}
  Session:         {session_info['session']}
  Comparison:      {session_info['driver1']} vs {session_info['driver2']}
  
🏆 OVERALL ADVANTAGE:  {result['overall_advantage']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏱️  PACE ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Fastest Lap Delta:      {pace['fastest_lap_delta']:+.3f}s
  Median Lap Delta:       {pace['median_lap_delta']:+.3f}s
  Average Lap Delta:      {pace['avg_lap_delta']:+.3f}s
  Ultimate Pace Delta:    {pace['ultimate_pace_delta']:+.3f}s
  
  Gap Percentage:         {pace['gap_percentage']:.3f}%
  Pace Advantage:         {pace['advantage']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 CONSISTENCY ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Std Dev Delta:          {consistency['std_dev_delta']:+.3f}s
  Consistency Rating:     {consistency['consistency_rating_delta']:+.2f}/10
  Outlier Laps Delta:     {consistency['outlier_laps_delta']:+d}
  Clean Lap % Delta:      {consistency['clean_lap_pct_delta']:+.1f}%
  Degradation Mgmt:       {consistency['degradation_consistency_delta']:+.2f}/10
  
  Advantage:              {consistency['advantage']}
  Reason:                 {consistency['advantage_reason']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 LAP DATA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  {session_info['driver1']} Laps:          {result['lap_data']['driver1_laps']}
  {session_info['driver2']} Laps:          {result['lap_data']['driver2_laps']}
  {session_info['driver1']} Fastest:       {result['lap_data']['driver1_fastest']:.3f}s
  {session_info['driver2']} Fastest:       {result['lap_data']['driver2_fastest']:.3f}s

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
        
        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                f.write(report)
        
        return report
    
    @staticmethod
    def generate_strategy_report(strategy: Dict[str, Any],
                                output_path: Optional[str] = None) -> str:
        """
        Generate pit strategy report.
        
        Args:
            strategy: Strategy recommendation dictionary
            output_path: Optional path to save report
            
        Returns:
            Formatted report string
        """
        report = f"""
╔══════════════════════════════════════════════════════════════════════╗
║                    PIT STRATEGY REPORT                               ║
╚══════════════════════════════════════════════════════════════════════╝

🎯 STRATEGY RECOMMENDATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Strategy Type:          {strategy.get('strategy_type', 'N/A')}
  Confidence:             {strategy.get('confidence', 0)*100:.0f}%

⏱️  PIT WINDOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Optimal Pit Lap:        Lap {strategy.get('optimal_pit_lap', 'N/A')}
  Window Opens:           Lap {strategy.get('pit_window_start', 'N/A')}
  Window Closes:          Lap {strategy.get('pit_window_end', 'N/A')}

🏎️  TYRE STRATEGY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Recommended Compound:   {strategy.get('recommended_compound', 'N/A')}
  Expected Stint Length:  {strategy.get('expected_stint_length', 'N/A')} laps

⚡ TACTICAL OPPORTUNITIES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Undercut Advantage:     {strategy.get('undercut_advantage', 0):.2f}s
  Overcut Advantage:      {strategy.get('overcut_advantage', 0):.2f}s

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
        
        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                f.write(report)
        
        return report

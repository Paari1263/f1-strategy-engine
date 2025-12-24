"""
CSV Exporter
Export analysis results to CSV format for spreadsheet analysis
"""

import pandas as pd
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime


class CSVExporter:
    """
    Exports F1 analysis results to CSV format.
    
    Useful for:
    - Spreadsheet analysis
    - Data visualization tools
    - Statistical analysis
    """
    
    @staticmethod
    def export_lap_comparison(laps1: pd.DataFrame, laps2: pd.DataFrame,
                             driver1: str, driver2: str,
                             output_path: str) -> None:
        """
        Export lap-by-lap comparison to CSV.
        
        Args:
            laps1: Laps of first driver
            laps2: Laps of second driver
            driver1: First driver name
            driver2: Second driver name
            output_path: Path to save CSV file
        """
        # Prepare data
        laps1 = laps1.copy()
        laps2 = laps2.copy()
        
        laps1['Driver'] = driver1
        laps2['Driver'] = driver2
        
        # Combine and select relevant columns
        combined = pd.concat([laps1, laps2])
        
        columns = ['LapNumber', 'Driver', 'LapTime', 'Compound', 'TyreLife', 
                  'Stint', 'Position', 'TrackStatus']
        
        # Filter columns that exist
        available_columns = [col for col in columns if col in combined.columns]
        export_data = combined[available_columns]
        
        # Ensure directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Export
        export_data.to_csv(output_path, index=False)
    
    @staticmethod
    def export_telemetry_comparison(tel1: pd.DataFrame, tel2: pd.DataFrame,
                                    driver1: str, driver2: str,
                                    output_path: str) -> None:
        """
        Export telemetry comparison to CSV.
        
        Args:
            tel1: Telemetry of first driver
            tel2: Telemetry of second driver
            driver1: First driver name
            driver2: Second driver name
            output_path: Path to save CSV file
        """
        # Add driver identifier
        tel1 = tel1.copy()
        tel2 = tel2.copy()
        
        tel1['Driver'] = driver1
        tel2['Driver'] = driver2
        
        # Combine
        combined = pd.concat([tel1, tel2])
        
        # Select key columns
        columns = ['Distance', 'Driver', 'Speed', 'Throttle', 'Brake', 
                  'nGear', 'DRS', 'RPM']
        
        available_columns = [col for col in columns if col in combined.columns]
        export_data = combined[available_columns]
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        export_data.to_csv(output_path, index=False)
    
    @staticmethod
    def export_strategy_comparison(strategies: List[Dict[str, Any]],
                                   output_path: str) -> None:
        """
        Export strategy comparison to CSV.
        
        Args:
            strategies: List of strategy dictionaries
            output_path: Path to save CSV file
        """
        # Convert to DataFrame
        df = pd.DataFrame(strategies)
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)
    
    @staticmethod
    def export_season_comparison(results: List[Dict[str, Any]],
                                output_path: str) -> None:
        """
        Export season-wide comparison to CSV.
        
        Args:
            results: List of race result dictionaries
            output_path: Path to save CSV file
        """
        df = pd.DataFrame(results)
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)

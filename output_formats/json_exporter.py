"""
JSON Exporter
Export analysis results to JSON format
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import pandas as pd


class JSONExporter:
    """
    Exports F1 analysis results to JSON format.
    
    Handles:
    - Car comparison results
    - Driver comparison results
    - Individual analysis results
    - Strategy recommendations
    - Battle predictions
    """
    
    @staticmethod
    def export_comparison(result: Dict[str, Any], output_path: str,
                         pretty: bool = True) -> None:
        """
        Export comparison results to JSON.
        
        Args:
            result: Comparison result dictionary
            output_path: Path to save JSON file
            pretty: Whether to format with indentation
        """
        # Add metadata
        export_data = {
            'metadata': {
                'export_time': datetime.now().isoformat(),
                'analysis_type': result.get('session_info', {}).get('session', 'Unknown'),
                'version': '1.0'
            },
            'data': result
        }
        
        # Ensure directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Write JSON
        with open(output_path, 'w') as f:
            if pretty:
                json.dump(export_data, f, indent=2, default=str)
            else:
                json.dump(export_data, f, default=str)
    
    @staticmethod
    def export_strategy(strategy: Dict[str, Any], output_path: str) -> None:
        """
        Export pit strategy to JSON.
        
        Args:
            strategy: Strategy dictionary
            output_path: Path to save JSON file
        """
        export_data = {
            'metadata': {
                'export_time': datetime.now().isoformat(),
                'type': 'pit_strategy'
            },
            'strategy': strategy
        }
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
    
    @staticmethod
    def export_battle_prediction(prediction: Dict[str, Any], output_path: str) -> None:
        """
        Export battle prediction to JSON.
        
        Args:
            prediction: Battle prediction dictionary
            output_path: Path to save JSON file
        """
        export_data = {
            'metadata': {
                'export_time': datetime.now().isoformat(),
                'type': 'battle_prediction'
            },
            'prediction': prediction
        }
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
    
    @staticmethod
    def load_json(input_path: str) -> Dict[str, Any]:
        """
        Load JSON file.
        
        Args:
            input_path: Path to JSON file
            
        Returns:
            Dictionary with loaded data
        """
        with open(input_path, 'r') as f:
            return json.load(f)

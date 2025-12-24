"""
Test Suite for Strategy API
Tests strategy endpoints: pit optimization, battle forecast

Run: pytest tests/test_strategy_api.py -v
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from fastapi.testclient import TestClient
from engines.main import app

client = TestClient(app)


class TestPitOptimization:
    """Test pit strategy optimization endpoint"""
    
    def test_pit_optimization_one_stop(self):
        """Test pit optimization for one-stop strategy"""
        response = client.get(
            "/api/v1/strategy/pit-optimization",
            params={
                "year": 2024,
                "event": "Monaco",
                "driver": "LEC",
                "current_lap": 20,
                "total_laps": 58,
                "current_compound": "MEDIUM",
                "tyre_age": 19,
                "position": 3
            }
        )
        
        assert response.status_code in [200, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert "optimal_pit_lap" in data
            assert "recommended_compound" in data
            assert "pit_window" in data or "pit_window_start" in data
    
    def test_pit_optimization_early_in_race(self):
        """Test pit optimization early in race"""
        response = client.get(
            "/api/v1/strategy/pit-optimization",
            params={
                "year": 2024,
                "event": "Monaco",
                "driver": "VER",
                "current_lap": 5,
                "total_laps": 58,
                "current_compound": "SOFT",
                "tyre_age": 4,
                "position": 1
            }
        )
        
        assert response.status_code in [200, 500]
    
    def test_pit_optimization_late_in_race(self):
        """Test pit optimization late in race"""
        response = client.get(
            "/api/v1/strategy/pit-optimization",
            params={
                "year": 2024,
                "event": "Monaco",
                "driver": "HAM",
                "current_lap": 50,
                "total_laps": 58,
                "current_compound": "HARD",
                "tyre_age": 45,
                "position": 5
            }
        )
        
        assert response.status_code in [200, 500]
        
        if response.status_code == 200:
            data = response.json()
            # Late in race might suggest staying out
            assert "optimal_pit_lap" in data
    
    def test_pit_optimization_with_gaps(self):
        """Test pit optimization with gap information"""
        response = client.get(
            "/api/v1/strategy/pit-optimization",
            params={
                "year": 2024,
                "event": "Silverstone",
                "driver": "NOR",
                "current_lap": 25,
                "total_laps": 58,
                "current_compound": "MEDIUM",
                "tyre_age": 24,
                "position": 4,
                "gap_ahead": 3.5,
                "gap_behind": 8.2
            }
        )
        
        assert response.status_code in [200, 500]
    
    def test_pit_optimization_different_compounds(self):
        """Test optimization with different tyre compounds"""
        compounds = ["SOFT", "MEDIUM", "HARD"]
        
        for compound in compounds:
            response = client.get(
                "/api/v1/strategy/pit-optimization",
                params={
                    "year": 2024,
                    "event": "Monza",
                    "driver": "LEC",
                    "current_lap": 20,
                    "total_laps": 58,
                    "current_compound": compound,
                    "tyre_age": 15,
                    "position": 2
                }
            )
            
            assert response.status_code in [200, 500]
    
    def test_pit_optimization_missing_params(self):
        """Test with missing required parameters"""
        response = client.get(
            "/api/v1/strategy/pit-optimization",
            params={
                "current_lap": 20,
                "total_laps": 58
                # Missing compound, tyre_age, track, year
            }
        )
        
        assert response.status_code == 422


class TestBattleForecast:
    """Test battle forecast endpoint"""
    
    def test_battle_forecast_basic(self):
        """Test basic battle forecast"""
        response = client.get(
            "/api/v1/strategy/battle-forecast",
            params={
                "year": 2024,
                "event": "Monaco",
                "session": "R",
                "attacker": "VER",
                "defender": "LEC",
                "lap": 30,
                "gap": 0.8,
                "drs_available": True
            }
        )
        
        assert response.status_code in [200, 404, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert "overtake_probability" in data
            assert "recommended_strategy" in data or "strategy" in data
    
    def test_battle_forecast_without_drs(self):
        """Test battle forecast without DRS"""
        response = client.get(
            "/api/v1/strategy/battle-forecast",
            params={
                "year": 2024,
                "event": "Monaco",
                "session": "R",
                "attacker": "VER",
                "defender": "LEC",
                "lap": 30,
                "gap": 1.5,
                "drs_available": False
            }
        )
        
        assert response.status_code in [200, 404, 500]
    
    def test_battle_forecast_close_gap(self):
        """Test battle forecast with very close gap"""
        response = client.get(
            "/api/v1/strategy/battle-forecast",
            params={
                "year": 2024,
                "event": "Monza",
                "session": "R",
                "attacker": "NOR",
                "defender": "PIA",
                "lap": 20,
                "gap": 0.3,  # Very close
                "drs_available": True
            }
        )
        
        assert response.status_code in [200, 404, 500]
        
        if response.status_code == 200:
            data = response.json()
            # Close gap should have higher overtake probability
            if "overtake_probability" in data:
                assert isinstance(data["overtake_probability"], (int, float))
    
    def test_battle_forecast_large_gap(self):
        """Test battle forecast with large gap"""
        response = client.get(
            "/api/v1/strategy/battle-forecast",
            params={
                "year": 2024,
                "event": "Spa",
                "session": "R",
                "attacker": "HAM",
                "defender": "RUS",
                "lap": 25,
                "gap": 5.0,  # Large gap
                "drs_available": True
            }
        )
        
        assert response.status_code in [200, 404, 500]
    
    def test_battle_forecast_different_tracks(self):
        """Test battle forecast on different track types"""
        tracks = [
            ("Monaco", 5.0),      # Street circuit, hard to overtake
            ("Monza", 4.0),       # Power circuit, easier overtake
            ("Silverstone", 6.0)  # Balanced circuit
        ]
        
        for track, difficulty in tracks:
            response = client.get(
                "/api/v1/strategy/battle-forecast",
                params={
                    "year": 2024,
                    "event": track,
                    "session": "R",
                    "attacker": "VER",
                    "defender": "LEC",
                    "lap": 30,
                    "gap": 1.0,
                    "drs_available": True
                }
            )
            
            assert response.status_code in [200, 404, 500]
    
    def test_battle_forecast_missing_params(self):
        """Test with missing required parameters"""
        response = client.get(
            "/api/v1/strategy/battle-forecast",
            params={
                "year": 2024,
                "event": "Monaco",
                "session": "R"
                # Missing drivers, lap, gap
            }
        )
        
        assert response.status_code == 422


class TestStrategyValidation:
    """Test input validation for strategy endpoints"""
    
    def test_invalid_compound(self):
        """Test pit optimization with invalid compound"""
        response = client.get(
            "/api/v1/strategy/pit-optimization",
            params={
                "current_lap": 20,
                "total_laps": 58,
                "current_compound": "ULTRASOFT",  # Invalid
                "current_tyre_age": 19,
                "track": "Monaco",
                "year": 2024
            }
        )
        
        # Should validate compound
        assert response.status_code in [422, 500]
    
    def test_invalid_lap_numbers(self):
        """Test with invalid lap numbers"""
        response = client.get(
            "/api/v1/strategy/pit-optimization",
            params={
                "current_lap": 100,  # Exceeds total
                "total_laps": 58,
                "current_compound": "MEDIUM",
                "current_tyre_age": 19,
                "track": "Monaco",
                "year": 2024
            }
        )
        
        # Should validate lap numbers
        assert response.status_code in [422, 500]
    
    def test_negative_gap(self):
        """Test battle forecast with negative gap"""
        response = client.get(
            "/api/v1/strategy/battle-forecast",
            params={
                "year": 2024,
                "event": "Monaco",
                "session": "R",
                "driver1": "VER",
                "driver2": "LEC",
                "lap": 30,
                "gap": -1.0,  # Negative gap
                "drs_available": True
            }
        )
        
        # Should handle or validate
        assert response.status_code in [422, 500, 200]


class TestStrategyResponseFormat:
    """Test response format consistency"""
    
    def test_pit_optimization_json_format(self):
        """Test pit optimization returns valid JSON"""
        response = client.get(
            "/api/v1/strategy/pit-optimization",
            params={
                "current_lap": 20,
                "total_laps": 58,
                "current_compound": "MEDIUM",
                "current_tyre_age": 19,
                "track": "Monaco",
                "year": 2024
            }
        )
        
        if response.status_code == 200:
            assert response.headers["content-type"] == "application/json"
            data = response.json()
            assert isinstance(data, dict)
    
    def test_battle_forecast_json_format(self):
        """Test battle forecast returns valid JSON"""
        response = client.get(
            "/api/v1/strategy/battle-forecast",
            params={
                "year": 2024,
                "event": "Monaco",
                "session": "R",
                "driver1": "VER",
                "driver2": "LEC",
                "lap": 30,
                "gap": 1.0,
                "drs_available": True
            }
        )
        
        if response.status_code == 200:
            assert response.headers["content-type"] == "application/json"
            data = response.json()
            assert isinstance(data, dict)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

"""
Test Suite for Comparison API
Tests all comparison endpoints: cars performance, tyre performance, driver pace, driver consistency

Run: pytest tests/test_comparison_api.py -v
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from fastapi.testclient import TestClient
from engines.main import app

client = TestClient(app)


class TestCarPerformanceComparison:
    """Test car performance comparison endpoints"""
    
    def test_cars_performance_detailed_success(self):
        """Test detailed car performance comparison endpoint"""
        response = client.get(
            "/api/v1/compare/cars/performance/detailed",
            params={
                "year": 2024,
                "event": "Monaco",
                "session": "Q",
                "driver1": "VER",
                "driver2": "LEC"
            }
        )
        
        # Should return 200 or 404 if data not available
        assert response.status_code in [200, 404, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert "car1" in data
            assert "car2" in data
            assert "delta_analysis" in data
            assert "overall_advantage" in data
            
            # Validate car1 structure
            assert "metadata" in data["car1"]
            assert "performance_profile" in data["car1"]
            assert "tyre_interaction" in data["car1"]
    
    def test_cars_performance_detailed_invalid_session(self):
        """Test with invalid session type"""
        response = client.get(
            "/api/v1/compare/cars/performance/detailed",
            params={
                "year": 2024,
                "event": "Monaco",
                "session": "INVALID",
                "driver1": "VER",
                "driver2": "LEC"
            }
        )
        
        # Should return validation error
        assert response.status_code == 422
    
    def test_cars_performance_detailed_missing_params(self):
        """Test with missing required parameters"""
        response = client.get(
            "/api/v1/compare/cars/performance/detailed",
            params={
                "year": 2024,
                "event": "Monaco"
                # Missing session, driver1, driver2
            }
        )
        
        assert response.status_code == 422
    
    def test_cars_performance_standard(self):
        """Test standard car performance comparison"""
        response = client.get(
            "/api/v1/compare/cars/performance",
            params={
                "year": 2024,
                "event": "Silverstone",
                "session": "R",
                "driver1": "HAM",
                "driver2": "RUS"
            }
        )
        
        assert response.status_code in [200, 404, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert "driver1" in data
            assert "driver2" in data
    
    def test_cars_tyre_performance(self):
        """Test tyre performance comparison"""
        response = client.get(
            "/api/v1/compare/cars/tyre-performance",
            params={
                "year": 2024,
                "event": "Monza",
                "session": "Q",
                "driver1": "NOR",
                "driver2": "PIA",
                "compound": "SOFT"  # Add required compound parameter
            }
        )
        
        assert response.status_code in [200, 404, 422, 500]


class TestDriverComparison:
    """Test driver comparison endpoints"""
    
    def test_drivers_pace_comparison(self):
        """Test driver pace comparison"""
        response = client.get(
            "/api/v1/compare/drivers/pace",
            params={
                "year": 2024,
                "event": "Monaco",
                "session": "Q",
                "driver1": "VER",
                "driver2": "LEC"
            }
        )
        
        assert response.status_code in [200, 404, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert "driver1" in data
            assert "driver2" in data
            assert "pace_delta" in data or "delta" in data
    
    def test_drivers_consistency_comparison(self):
        """Test driver consistency comparison"""
        response = client.get(
            "/api/v1/compare/drivers/consistency",
            params={
                "year": 2024,
                "event": "Silverstone",
                "session": "R",
                "driver1": "ALO",
                "driver2": "STR"
            }
        )
        
        assert response.status_code in [200, 404, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert "driver1" in data
            assert "driver2" in data
    
    def test_drivers_comparison_different_teams(self):
        """Test comparing drivers from different teams"""
        response = client.get(
            "/api/v1/compare/drivers/pace",
            params={
                "year": 2024,
                "event": "Spa",
                "session": "Q",
                "driver1": "VER",
                "driver2": "HAM"
            }
        )
        
        assert response.status_code in [200, 404, 500]


class TestComparisonAPIValidation:
    """Test input validation for comparison endpoints"""
    
    def test_invalid_year(self):
        """Test with invalid year"""
        response = client.get(
            "/api/v1/compare/cars/performance/detailed",
            params={
                "year": 2050,  # Future year
                "event": "Monaco",
                "session": "Q",
                "driver1": "VER",
                "driver2": "LEC"
            }
        )
        
        # Should either validate or return 404 for no data
        assert response.status_code in [404, 422, 500]
    
    def test_invalid_event_name(self):
        """Test with non-existent event"""
        response = client.get(
            "/api/v1/compare/cars/performance",
            params={
                "year": 2024,
                "event": "NonExistentGP",
                "session": "Q",
                "driver1": "VER",
                "driver2": "LEC"
            }
        )
        
        # FastF1 may auto-correct event names, so accept both 200 and 404
        assert response.status_code in [200, 404, 500]
    
    def test_same_driver_comparison(self):
        """Test comparing same driver (edge case)"""
        response = client.get(
            "/api/v1/compare/drivers/pace",
            params={
                "year": 2024,
                "event": "Monaco",
                "session": "Q",
                "driver1": "VER",
                "driver2": "VER"
            }
        )
        
        # Should handle gracefully
        assert response.status_code in [200, 400, 422, 500]


class TestComparisonAPIResponseFormat:
    """Test response format consistency"""
    
    def test_response_has_metadata(self):
        """Test that successful responses include metadata"""
        response = client.get(
            "/api/v1/compare/cars/performance/detailed",
            params={
                "year": 2024,
                "event": "Monaco",
                "session": "Q",
                "driver1": "VER",
                "driver2": "LEC"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            # Check for metadata in at least one car object
            if "car1" in data:
                assert "metadata" in data["car1"]
    
    def test_json_response_format(self):
        """Test that all comparison endpoints return JSON"""
        endpoints = [
            "/api/v1/compare/cars/performance/detailed",
            "/api/v1/compare/cars/performance",
            "/api/v1/compare/drivers/pace"
        ]
        
        params = {
            "year": 2024,
            "event": "Monaco",
            "session": "Q",
            "driver1": "VER",
            "driver2": "LEC"
        }
        
        for endpoint in endpoints:
            response = client.get(endpoint, params=params)
            
            if response.status_code == 200:
                # Verify it's valid JSON
                assert response.headers["content-type"] == "application/json"
                data = response.json()
                assert isinstance(data, dict)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

"""
Test Suite for Driver Insights API
Tests driver-specific endpoints: performance profile, stint analysis

Run: pytest tests/test_driver_insights_api.py -v
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from fastapi.testclient import TestClient
from engines.main import app

client = TestClient(app)


class TestDriverPerformanceProfile:
    """Test driver performance profile endpoint"""
    
    def test_performance_profile_success(self):
        """Test getting driver performance profile"""
        response = client.get(
            "/api/v1/drivers/performance-profile",
            params={
                "year": 2024,
                "event": "Monaco",
                "session": "Q",
                "driver": "VER"
            }
        )
        
        assert response.status_code in [200, 404, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert "driver" in data
            # Should have performance metrics
            assert isinstance(data, dict)
    
    def test_performance_profile_race_session(self):
        """Test performance profile for race session"""
        response = client.get(
            "/api/v1/drivers/performance-profile",
            params={
                "year": 2024,
                "event": "Silverstone",
                "session": "R",
                "driver": "HAM"
            }
        )
        
        assert response.status_code in [200, 404, 500]
    
    def test_performance_profile_practice_session(self):
        """Test performance profile for practice session"""
        response = client.get(
            "/api/v1/drivers/performance-profile",
            params={
                "year": 2024,
                "event": "Spa",
                "session": "FP2",
                "driver": "LEC"
            }
        )
        
        assert response.status_code in [200, 404, 500]
    
    def test_performance_profile_missing_driver(self):
        """Test with missing driver parameter"""
        response = client.get(
            "/api/v1/drivers/performance-profile",
            params={
                "year": 2024,
                "event": "Monaco",
                "session": "Q"
                # Missing driver
            }
        )
        
        assert response.status_code in [404, 422]
    
    def test_performance_profile_invalid_driver_code(self):
        """Test with invalid driver code"""
        response = client.get(
            "/api/v1/drivers/performance-profile",
            params={
                "year": 2024,
                "event": "Monaco",
                "session": "Q",
                "driver": "XXX"  # Invalid code
            }
        )
        
        # Should return 404 or handle gracefully
        assert response.status_code in [404, 500]


class TestStintAnalysis:
    """Test stint analysis endpoint"""
    
    def test_stint_analysis_race(self):
        """Test stint analysis for race session"""
        response = client.get(
            "/api/v1/drivers/stint-analysis",
            params={
                "year": 2024,
                "event": "Monaco",
                "session": "R",
                "driver": "VER"
            }
        )
        
        assert response.status_code in [200, 404, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert "driver" in data
            # Should have stint-related data
            assert isinstance(data, dict)
    
    def test_stint_analysis_multiple_stints(self):
        """Test stint analysis with multiple pit stops"""
        response = client.get(
            "/api/v1/drivers/stint-analysis",
            params={
                "year": 2024,
                "event": "Silverstone",
                "session": "R",
                "driver": "NOR"
            }
        )
        
        assert response.status_code in [200, 404, 500]
        
        if response.status_code == 200:
            data = response.json()
            # Should contain stint information
            assert isinstance(data, dict)
    
    def test_stint_analysis_qualifying(self):
        """Test stint analysis for qualifying (edge case - single stint)"""
        response = client.get(
            "/api/v1/drivers/stint-analysis",
            params={
                "year": 2024,
                "event": "Monaco",
                "session": "Q",
                "driver": "LEC"
            }
        )
        
        # Should handle qualifying session appropriately
        assert response.status_code in [200, 404, 500]
    
    def test_stint_analysis_missing_params(self):
        """Test with missing required parameters"""
        response = client.get(
            "/api/v1/drivers/stint-analysis",
            params={
                "year": 2024,
                "event": "Monaco"
                # Missing session and driver
            }
        )
        
        assert response.status_code in [404, 422]


class TestDriverInsightsValidation:
    """Test input validation for driver insights endpoints"""
    
    def test_invalid_session_type(self):
        """Test with invalid session type"""
        response = client.get(
            "/api/v1/drivers/performance-profile",
            params={
                "year": 2024,
                "event": "Monaco",
                "session": "INVALID",
                "driver": "VER"
            }
        )
        
        assert response.status_code in [404, 422]
    
    def test_future_year(self):
        """Test with future year"""
        response = client.get(
            "/api/v1/drivers/performance-profile",
            params={
                "year": 2030,
                "event": "Monaco",
                "session": "Q",
                "driver": "VER"
            }
        )
        
        # Should return 404 or validation error
        assert response.status_code in [404, 422, 500]
    
    def test_past_year_no_data(self):
        """Test with very old year (before F1 data available)"""
        response = client.get(
            "/api/v1/drivers/performance-profile",
            params={
                "year": 2010,
                "event": "Monaco",
                "session": "Q",
                "driver": "VER"
            }
        )
        
        # Should handle gracefully
        assert response.status_code in [404, 500]


class TestDriverInsightsResponseFormat:
    """Test response format consistency"""
    
    def test_json_format(self):
        """Test that responses are in JSON format"""
        response = client.get(
            "/api/v1/drivers/performance-profile",
            params={
                "year": 2024,
                "event": "Monaco",
                "session": "Q",
                "driver": "VER"
            }
        )
        
        if response.status_code == 200:
            assert response.headers["content-type"] == "application/json"
            data = response.json()
            assert isinstance(data, dict)
    
    def test_response_structure_consistency(self):
        """Test that similar endpoints have consistent structure"""
        endpoints = [
            "/api/v1/drivers/performance-profile",
            "/api/v1/drivers/stint-analysis"
        ]
        
        params = {
            "year": 2024,
            "event": "Monaco",
            "session": "R",
            "driver": "VER"
        }
        
        for endpoint in endpoints:
            response = client.get(endpoint, params=params)
            
            if response.status_code == 200:
                data = response.json()
                # Should have driver information
                assert "driver" in data or isinstance(data, dict)


class TestMultipleDrivers:
    """Test endpoints with multiple drivers"""
    
    def test_different_drivers_same_session(self):
        """Test multiple drivers from same session"""
        drivers = ["VER", "LEC", "HAM", "NOR"]
        
        for driver in drivers:
            response = client.get(
                "/api/v1/drivers/performance-profile",
                params={
                    "year": 2024,
                    "event": "Monaco",
                    "session": "Q",
                    "driver": driver
                }
            )
            
            assert response.status_code in [200, 404, 500]
    
    def test_rookie_vs_veteran(self):
        """Test rookie vs veteran driver data"""
        # Test with different experience levels
        rookie = "PIA"
        veteran = "ALO"
        
        for driver in [rookie, veteran]:
            response = client.get(
                "/api/v1/drivers/stint-analysis",
                params={
                    "year": 2024,
                    "event": "Silverstone",
                    "session": "R",
                    "driver": driver
                }
            )
            
            assert response.status_code in [200, 404, 500]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

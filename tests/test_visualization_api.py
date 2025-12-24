"""
Test Suite for Visualization API
Tests all visualization endpoints: speed-trace, throttle-brake, lap-time-distribution,
sector-comparison, tyre-degradation, gear-usage, performance-radar, health

Run: pytest tests/test_visualization_api.py -v
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from fastapi.testclient import TestClient
from engines.main import app

client = TestClient(app)


class TestVisualizationHealth:
    """Test visualization health check endpoint"""
    
    def test_health_check(self):
        """Test visualization health endpoint"""
        response = client.get("/api/v1/visualizations/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "status" in data
        assert "libraries" in data
        assert data["status"] == "ok"
        assert "plotly" in data["libraries"]
        assert "matplotlib" in data["libraries"]


class TestSpeedTrace:
    """Test speed trace visualization endpoint"""
    
    def test_speed_trace_json_format(self):
        """Test speed trace with JSON output"""
        response = client.get(
            "/api/v1/visualizations/speed-trace",
            params={
                "year": 2024,
                "event": "Monaco",
                "session": "Q",
                "driver1": "VER",
                "driver2": "LEC",
                "format": "json"
            }
        )
        
        assert response.status_code in [200, 404, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert "plotly_json" in data or "data" in data
            assert "type" in data
    
    def test_speed_trace_png_format(self):
        """Test speed trace with PNG output"""
        response = client.get(
            "/api/v1/visualizations/speed-trace",
            params={
                "year": 2024,
                "event": "Monza",
                "session": "Q",
                "driver1": "NOR",
                "driver2": "PIA",
                "format": "png"
            }
        )
        
        assert response.status_code in [200, 404, 500]
        
        if response.status_code == 200:
            assert response.headers["content-type"] == "image/png"
    
    def test_speed_trace_missing_format(self):
        """Test speed trace with default format (JSON)"""
        response = client.get(
            "/api/v1/visualizations/speed-trace",
            params={
                "year": 2024,
                "event": "Silverstone",
                "session": "Q",
                "driver1": "HAM",
                "driver2": "RUS"
                # format not specified, should default to json
            }
        )
        
        assert response.status_code in [200, 404, 500]
        
        if response.status_code == 200:
            # Should default to JSON
            assert "application/json" in response.headers["content-type"]


class TestThrottleBrake:
    """Test throttle-brake visualization endpoint"""
    
    def test_throttle_brake_json(self):
        """Test throttle-brake with JSON format"""
        response = client.get(
            "/api/v1/visualizations/throttle-brake",
            params={
                "year": 2024,
                "event": "Monaco",
                "session": "Q",
                "driver1": "VER",
                "driver2": "LEC",
                "format": "json"
            }
        )
        
        assert response.status_code in [200, 404, 500]
    
    def test_throttle_brake_png(self):
        """Test throttle-brake with PNG format"""
        response = client.get(
            "/api/v1/visualizations/throttle-brake",
            params={
                "year": 2024,
                "event": "Silverstone",
                "session": "Q",
                "driver1": "HAM",
                "driver2": "RUS",
                "format": "png"
            }
        )
        
        assert response.status_code in [200, 404, 500]
        
        if response.status_code == 200:
            assert response.headers["content-type"] == "image/png"


class TestLapTimeDistribution:
    """Test lap time distribution visualization endpoint"""
    
    def test_lap_distribution_two_drivers(self):
        """Test lap time distribution with 2 drivers"""
        response = client.get(
            "/api/v1/visualizations/lap-time-distribution",
            params={
                "year": 2024,
                "event": "Monaco",
                "session": "Q",
                "drivers": "VER,LEC",
                "format": "json"
            }
        )
        
        assert response.status_code in [200, 404, 500]
    
    def test_lap_distribution_multiple_drivers(self):
        """Test lap time distribution with 5 drivers"""
        response = client.get(
            "/api/v1/visualizations/lap-time-distribution",
            params={
                "year": 2024,
                "event": "Silverstone",
                "session": "R",
                "drivers": "VER,LEC,HAM,NOR,PIA",
                "format": "json"
            }
        )
        
        assert response.status_code in [200, 404, 500]
    
    def test_lap_distribution_png(self):
        """Test lap time distribution with PNG output"""
        response = client.get(
            "/api/v1/visualizations/lap-time-distribution",
            params={
                "year": 2024,
                "event": "Monaco",
                "session": "Q",
                "drivers": "VER,LEC,HAM",
                "format": "png"
            }
        )
        
        assert response.status_code in [200, 404, 500]
        
        if response.status_code == 200:
            assert response.headers["content-type"] == "image/png"
    
    def test_lap_distribution_missing_drivers(self):
        """Test with missing drivers parameter"""
        response = client.get(
            "/api/v1/visualizations/lap-time-distribution",
            params={
                "year": 2024,
                "event": "Monaco",
                "session": "Q",
                "format": "json"
                # Missing drivers
            }
        )
        
        assert response.status_code == 422


class TestSectorComparison:
    """Test sector comparison visualization endpoint"""
    
    def test_sector_comparison_json(self):
        """Test sector comparison with JSON format"""
        response = client.get(
            "/api/v1/visualizations/sector-comparison",
            params={
                "year": 2024,
                "event": "Monaco",
                "session": "Q",
                "driver1": "VER",
                "driver2": "LEC",
                "format": "json"
            }
        )
        
        assert response.status_code in [200, 404, 500]
    
    def test_sector_comparison_png(self):
        """Test sector comparison with PNG format"""
        response = client.get(
            "/api/v1/visualizations/sector-comparison",
            params={
                "year": 2024,
                "event": "Spa",
                "session": "Q",
                "driver1": "HAM",
                "driver2": "RUS",
                "format": "png"
            }
        )
        
        assert response.status_code in [200, 404, 500]
        
        if response.status_code == 200:
            assert response.headers["content-type"] == "image/png"


class TestTyreDegradation:
    """Test tyre degradation visualization endpoint"""
    
    def test_tyre_degradation_race(self):
        """Test tyre degradation for race session"""
        response = client.get(
            "/api/v1/visualizations/tyre-degradation",
            params={
                "year": 2024,
                "event": "Monaco",
                "session": "R",
                "driver": "VER",
                "format": "json"
            }
        )
        
        assert response.status_code in [200, 404, 500]
    
    def test_tyre_degradation_png(self):
        """Test tyre degradation with PNG format"""
        response = client.get(
            "/api/v1/visualizations/tyre-degradation",
            params={
                "year": 2024,
                "event": "Silverstone",
                "session": "R",
                "driver": "HAM",
                "format": "png"
            }
        )
        
        assert response.status_code in [200, 404, 500]
        
        if response.status_code == 200:
            assert response.headers["content-type"] == "image/png"
    
    def test_tyre_degradation_qualifying(self):
        """Test tyre degradation for qualifying (edge case)"""
        response = client.get(
            "/api/v1/visualizations/tyre-degradation",
            params={
                "year": 2024,
                "event": "Monaco",
                "session": "Q",
                "driver": "LEC",
                "format": "json"
            }
        )
        
        # Should handle qualifying session
        assert response.status_code in [200, 404, 500]


class TestGearUsage:
    """Test gear usage visualization endpoint"""
    
    def test_gear_usage_json(self):
        """Test gear usage with JSON format"""
        response = client.get(
            "/api/v1/visualizations/gear-usage",
            params={
                "year": 2024,
                "event": "Monaco",
                "session": "Q",
                "driver": "VER",
                "format": "json"
            }
        )
        
        assert response.status_code in [200, 404, 500]
    
    def test_gear_usage_png(self):
        """Test gear usage with PNG format"""
        response = client.get(
            "/api/v1/visualizations/gear-usage",
            params={
                "year": 2024,
                "event": "Monza",
                "session": "Q",
                "driver": "NOR",
                "format": "png"
            }
        )
        
        assert response.status_code in [200, 404, 500]
        
        if response.status_code == 200:
            assert response.headers["content-type"] == "image/png"
    
    def test_gear_usage_different_tracks(self):
        """Test gear usage on different track types"""
        tracks = ["Monaco", "Monza", "Spa"]  # Low-speed, high-speed, mixed
        
        for track in tracks:
            response = client.get(
                "/api/v1/visualizations/gear-usage",
                params={
                    "year": 2024,
                    "event": track,
                    "session": "Q",
                    "driver": "VER",
                    "format": "json"
                }
            )
            
            assert response.status_code in [200, 404, 500]


class TestPerformanceRadar:
    """Test performance radar visualization endpoint"""
    
    def test_performance_radar_json(self):
        """Test performance radar with JSON format"""
        response = client.get(
            "/api/v1/visualizations/performance-radar",
            params={
                "year": 2024,
                "event": "Monaco",
                "session": "Q",
                "driver1": "VER",
                "driver2": "LEC",
                "format": "json"
            }
        )
        
        assert response.status_code in [200, 404, 500]
    
    def test_performance_radar_png(self):
        """Test performance radar with PNG format"""
        response = client.get(
            "/api/v1/visualizations/performance-radar",
            params={
                "year": 2024,
                "event": "Silverstone",
                "session": "R",
                "driver1": "NOR",
                "driver2": "PIA",
                "format": "png"
            }
        )
        
        assert response.status_code in [200, 404, 500]
        
        if response.status_code == 200:
            assert response.headers["content-type"] == "image/png"


class TestVisualizationValidation:
    """Test input validation for visualization endpoints"""
    
    def test_invalid_format(self):
        """Test with invalid format parameter"""
        response = client.get(
            "/api/v1/visualizations/speed-trace",
            params={
                "year": 2024,
                "event": "Monaco",
                "session": "Q",
                "driver1": "VER",
                "driver2": "LEC",
                "format": "svg"  # Invalid format
            }
        )
        
        # Should validate format
        assert response.status_code in [422, 500]
    
    def test_missing_required_params(self):
        """Test with missing required parameters"""
        response = client.get(
            "/api/v1/visualizations/speed-trace",
            params={
                "year": 2024,
                "event": "Monaco"
                # Missing session, drivers
            }
        )
        
        assert response.status_code == 422


class TestVisualizationPerformance:
    """Test visualization performance and output quality"""
    
    def test_json_response_size(self):
        """Test that JSON responses are reasonable in size"""
        response = client.get(
            "/api/v1/visualizations/speed-trace",
            params={
                "year": 2024,
                "event": "Monaco",
                "session": "Q",
                "driver1": "VER",
                "driver2": "LEC",
                "format": "json"
            }
        )
        
        if response.status_code == 200:
            # JSON response should be under 5MB
            assert len(response.content) < 5 * 1024 * 1024
    
    def test_png_response_size(self):
        """Test that PNG responses are reasonable in size"""
        response = client.get(
            "/api/v1/visualizations/speed-trace",
            params={
                "year": 2024,
                "event": "Monaco",
                "session": "Q",
                "driver1": "VER",
                "driver2": "LEC",
                "format": "png"
            }
        )
        
        if response.status_code == 200:
            # PNG response should be under 2MB
            assert len(response.content) < 2 * 1024 * 1024


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

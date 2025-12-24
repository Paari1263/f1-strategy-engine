"""
Redis Cache Integration Test
Tests the caching infrastructure without starting the full server.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from cache import get_redis_client, get_cache_manager, CacheKeys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_redis_connection():
    """Test Redis connection and basic operations"""
    print("\n" + "="*60)
    print("REDIS CACHE INTEGRATION TEST")
    print("="*60)
    
    # Test 1: Redis Connection
    print("\n[1/6] Testing Redis connection...")
    try:
        redis_client = get_redis_client()
        stats = redis_client.get_stats()
        
        if stats.get('connected'):
            print(f"✓ Redis connected successfully!")
            print(f"  • Version: {stats.get('version')}")
            print(f"  • Total keys: {stats.get('total_keys')}")
            print(f"  • Used memory: {stats.get('used_memory')}")
            print(f"  • Hit rate: {stats.get('hit_rate')}%")
        else:
            print(f"✗ Redis not connected")
            print(f"  • Error: {stats.get('error', 'Unknown')}")
            return False
    except Exception as e:
        print(f"✗ Redis connection failed: {e}")
        print("\nMake sure Redis is running:")
        print("  docker-compose up -d")
        return False
    
    # Test 2: Basic Set/Get
    print("\n[2/6] Testing basic set/get operations...")
    try:
        test_key = "test:cache:basic"
        test_value = {"message": "Hello from Redis cache!", "timestamp": "2024-12-24"}
        
        redis_client.set(test_key, test_value, ttl=60)
        retrieved = redis_client.get(test_key)
        
        if retrieved == test_value:
            print(f"✓ Basic operations working!")
            print(f"  • Stored: {test_value}")
            print(f"  • Retrieved: {retrieved}")
        else:
            print(f"✗ Data mismatch!")
            return False
    except Exception as e:
        print(f"✗ Basic operations failed: {e}")
        return False
    
    # Test 3: Cache Key Generation
    print("\n[3/6] Testing cache key generation...")
    try:
        keys = CacheKeys()
        
        session_key = keys.session_data(2024, "Monaco", "Q")
        laps_key = keys.session_laps(2024, "Monaco", "Q", "VER")
        api_key = keys.api_response("/api/v1/compare/cars", year=2024, event="Monaco")
        schedule_key = keys.season_schedule(2024)
        
        print(f"✓ Cache keys generated successfully!")
        print(f"  • Session: {session_key}")
        print(f"  • Laps: {laps_key}")
        print(f"  • API: {api_key}")
        print(f"  • Schedule: {schedule_key}")
    except Exception as e:
        print(f"✗ Key generation failed: {e}")
        return False
    
    # Test 4: Cache Manager
    print("\n[4/6] Testing cache manager...")
    try:
        cache_manager = get_cache_manager()
        
        # Test caching session data
        test_session_data = {
            "year": 2024,
            "event": "Monaco",
            "session_type": "Q",
            "laps": 78
        }
        
        cache_manager.cache_session_data(
            year=2024,
            event="Monaco",
            session_type="Q",
            data=test_session_data
        )
        
        # Retrieve
        retrieved_session = cache_manager.get_session_data(2024, "Monaco", "Q")
        
        if retrieved_session == test_session_data:
            print(f"✓ Cache manager working!")
            print(f"  • Cached and retrieved session data")
        else:
            print(f"✗ Cache manager data mismatch!")
            return False
    except Exception as e:
        print(f"✗ Cache manager failed: {e}")
        return False
    
    # Test 5: Cache Statistics
    print("\n[5/6] Testing cache statistics...")
    try:
        stats = cache_manager.get_cache_stats()
        
        print(f"✓ Cache statistics retrieved!")
        print(f"  • Total keys: {stats.get('total_keys')}")
        print(f"  • Layer counts: {stats.get('layer_counts', {})}")
        print(f"  • Hit rate: {stats.get('hit_rate')}%")
    except Exception as e:
        print(f"✗ Statistics failed: {e}")
        return False
    
    # Test 6: Cache Invalidation
    print("\n[6/6] Testing cache invalidation...")
    try:
        # Invalidate test data
        count = cache_manager.invalidate_session(2024, "Monaco", "Q")
        
        # Verify deletion
        retrieved = cache_manager.get_session_data(2024, "Monaco", "Q")
        
        if retrieved is None and count > 0:
            print(f"✓ Cache invalidation working!")
            print(f"  • Deleted {count} keys")
        else:
            print(f"✗ Invalidation failed!")
            return False
    except Exception as e:
        print(f"✗ Invalidation failed: {e}")
        return False
    
    # Cleanup test keys
    try:
        redis_client.delete("test:cache:basic")
    except:
        pass
    
    print("\n" + "="*60)
    print("✓ ALL TESTS PASSED!")
    print("="*60)
    print("\nNext steps:")
    print("  1. Start Redis: docker-compose up -d")
    print("  2. Start API server: uvicorn engines.main:app --port 8001 --reload")
    print("  3. View Redis Commander: http://localhost:8081")
    print("  4. Check cache stats: http://localhost:8001/v1/cache/stats")
    print()
    
    return True


if __name__ == "__main__":
    success = test_redis_connection()
    sys.exit(0 if success else 1)

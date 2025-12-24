"""
Cache Manager
Manages local caching of FastF1 data and processed results
"""

import pickle
import json
from pathlib import Path
from typing import Any, Optional
from datetime import datetime
import hashlib


class CacheManager:
    """
    Manages caching of FastF1 data and processed analysis results.
    
    Supports both FastF1's internal caching and custom result caching
    to avoid reprocessing data.
    """
    
    def __init__(self, cache_dir: Optional[str] = None):
        """
        Initialize cache manager.
        
        Args:
            cache_dir: Directory for cache. If None, uses ~/.f1_analysis_cache
        """
        if cache_dir:
            self.cache_dir = Path(cache_dir)
        else:
            self.cache_dir = Path.home() / '.f1_analysis_cache'
        
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        self.sessions_dir = self.cache_dir / 'sessions'
        self.results_dir = self.cache_dir / 'results'
        self.telemetry_dir = self.cache_dir / 'telemetry'
        
        self.sessions_dir.mkdir(exist_ok=True)
        self.results_dir.mkdir(exist_ok=True)
        self.telemetry_dir.mkdir(exist_ok=True)
    
    def _generate_key(self, *args) -> str:
        """
        Generate a unique cache key from arguments.
        
        Args:
            *args: Arguments to hash
            
        Returns:
            MD5 hash string
        """
        key_string = '_'.join(str(arg) for arg in args)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def cache_result(self, key: str, data: Any, category: str = 'results') -> None:
        """
        Cache analysis results.
        
        Args:
            key: Unique identifier for the data
            data: Data to cache (must be serializable)
            category: Cache category ('results', 'telemetry', 'sessions')
        """
        if category == 'results':
            cache_path = self.results_dir
        elif category == 'telemetry':
            cache_path = self.telemetry_dir
        else:
            cache_path = self.sessions_dir
        
        file_path = cache_path / f"{key}.pkl"
        
        try:
            with open(file_path, 'wb') as f:
                pickle.dump({
                    'data': data,
                    'timestamp': datetime.now().isoformat(),
                    'key': key
                }, f)
        except Exception as e:
            print(f"Warning: Failed to cache data: {e}")
    
    def load_cached_result(self, key: str, category: str = 'results') -> Optional[Any]:
        """
        Load cached analysis results.
        
        Args:
            key: Unique identifier for the data
            category: Cache category
            
        Returns:
            Cached data or None if not found
        """
        if category == 'results':
            cache_path = self.results_dir
        elif category == 'telemetry':
            cache_path = self.telemetry_dir
        else:
            cache_path = self.sessions_dir
        
        file_path = cache_path / f"{key}.pkl"
        
        if not file_path.exists():
            return None
        
        try:
            with open(file_path, 'rb') as f:
                cached = pickle.load(f)
                return cached['data']
        except Exception as e:
            print(f"Warning: Failed to load cached data: {e}")
            return None
    
    def is_cached(self, key: str, category: str = 'results') -> bool:
        """
        Check if data is cached.
        
        Args:
            key: Unique identifier
            category: Cache category
            
        Returns:
            True if cached, False otherwise
        """
        if category == 'results':
            cache_path = self.results_dir
        elif category == 'telemetry':
            cache_path = self.telemetry_dir
        else:
            cache_path = self.sessions_dir
        
        file_path = cache_path / f"{key}.pkl"
        return file_path.exists()
    
    def clear_cache(self, category: Optional[str] = None) -> None:
        """
        Clear cache.
        
        Args:
            category: Specific category to clear, or None for all
        """
        if category == 'results' or category is None:
            for file in self.results_dir.glob('*.pkl'):
                file.unlink()
        
        if category == 'telemetry' or category is None:
            for file in self.telemetry_dir.glob('*.pkl'):
                file.unlink()
        
        if category == 'sessions' or category is None:
            for file in self.sessions_dir.glob('*.pkl'):
                file.unlink()
    
    def get_cache_info(self) -> dict:
        """
        Get information about cached data.
        
        Returns:
            Dict with cache statistics
        """
        return {
            'cache_dir': str(self.cache_dir),
            'results_count': len(list(self.results_dir.glob('*.pkl'))),
            'telemetry_count': len(list(self.telemetry_dir.glob('*.pkl'))),
            'sessions_count': len(list(self.sessions_dir.glob('*.pkl'))),
            'total_size_mb': sum(
                f.stat().st_size for f in self.cache_dir.rglob('*.pkl')
            ) / (1024 * 1024)
        }
    
    def generate_session_key(self, year: int, gp: str, session_type: str, driver: Optional[str] = None) -> str:
        """
        Generate cache key for session data.
        
        Args:
            year: Season year
            gp: Grand Prix
            session_type: Session type
            driver: Optional driver filter
            
        Returns:
            Cache key string
        """
        if driver:
            return self._generate_key(year, gp, session_type, driver)
        return self._generate_key(year, gp, session_type)
    
    def generate_analysis_key(self, analysis_type: str, *args) -> str:
        """
        Generate cache key for analysis results.
        
        Args:
            analysis_type: Type of analysis
            *args: Additional parameters
            
        Returns:
            Cache key string
        """
        return self._generate_key(analysis_type, *args)

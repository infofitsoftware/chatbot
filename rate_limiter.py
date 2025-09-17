"""
Simple rate limiter to help manage API quota usage.
"""

import time
from collections import defaultdict, deque
from typing import Dict, Deque

class RateLimiter:
    """Simple rate limiter for API calls"""
    
    def __init__(self, max_requests: int = 10, time_window: int = 60):
        """
        Initialize rate limiter
        
        Args:
            max_requests: Maximum requests allowed in time window
            time_window: Time window in seconds
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests: Dict[str, Deque[float]] = defaultdict(deque)
    
    def is_allowed(self, key: str = "default") -> bool:
        """
        Check if request is allowed
        
        Args:
            key: Unique key for rate limiting (e.g., user ID)
            
        Returns:
            True if request is allowed, False otherwise
        """
        now = time.time()
        request_times = self.requests[key]
        
        # Remove old requests outside time window
        while request_times and request_times[0] <= now - self.time_window:
            request_times.popleft()
        
        # Check if we can make another request
        if len(request_times) < self.max_requests:
            request_times.append(now)
            return True
        
        return False
    
    def get_retry_after(self, key: str = "default") -> int:
        """
        Get seconds to wait before next request is allowed
        
        Args:
            key: Unique key for rate limiting
            
        Returns:
            Seconds to wait
        """
        if not self.requests[key]:
            return 0
        
        oldest_request = self.requests[key][0]
        retry_after = int(self.time_window - (time.time() - oldest_request))
        return max(0, retry_after)

# Global rate limiter instance
rate_limiter = RateLimiter(max_requests=5, time_window=60)  # 5 requests per minute

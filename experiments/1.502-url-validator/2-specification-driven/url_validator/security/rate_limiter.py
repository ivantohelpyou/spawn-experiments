"""Rate limiting utilities for URL validation."""

import time
import threading
from collections import defaultdict, deque
from typing import Dict, Optional, Tuple
from dataclasses import dataclass

from ..models.error import ValidationError, ErrorCode


@dataclass
class RateLimitConfig:
    """Configuration for rate limiting."""

    requests_per_minute: int = 60
    requests_per_hour: int = 1000
    burst_size: int = 10
    cleanup_interval: int = 300  # 5 minutes


class RateLimiter:
    """
    Provides rate limiting for URL validation requests.

    This class implements token bucket and sliding window algorithms
    to prevent abuse and limit resource consumption.
    """

    def __init__(self, config: Optional[RateLimitConfig] = None):
        """
        Initialize rate limiter.

        Args:
            config: Rate limiting configuration
        """
        self.config = config or RateLimitConfig()

        # Per-client request tracking
        self._minute_requests: Dict[str, deque] = defaultdict(deque)
        self._hour_requests: Dict[str, deque] = defaultdict(deque)

        # Token bucket for burst handling
        self._tokens: Dict[str, float] = defaultdict(lambda: self.config.burst_size)
        self._last_refill: Dict[str, float] = defaultdict(time.time)

        # Thread safety
        self._lock = threading.Lock()

        # Cleanup tracking
        self._last_cleanup = time.time()

    def check_rate_limit(self, client_id: str) -> Tuple[bool, Optional[ValidationError]]:
        """
        Check if request is within rate limits.

        Args:
            client_id: Identifier for the client making the request

        Returns:
            Tuple of (is_allowed, error_if_rate_limited)
        """
        with self._lock:
            current_time = time.time()

            # Periodic cleanup
            if current_time - self._last_cleanup > self.config.cleanup_interval:
                self._cleanup_old_entries(current_time)
                self._last_cleanup = current_time

            # Check token bucket (for burst protection)
            if not self._check_token_bucket(client_id, current_time):
                return False, ValidationError.security_error(
                    ErrorCode.RATE_LIMIT_EXCEEDED,
                    "Request rate limit exceeded (burst protection)",
                    {
                        "client_id": client_id,
                        "limit_type": "burst",
                        "burst_size": self.config.burst_size
                    }
                )

            # Check sliding window limits
            minute_allowed, minute_error = self._check_minute_limit(client_id, current_time)
            if not minute_allowed:
                return False, minute_error

            hour_allowed, hour_error = self._check_hour_limit(client_id, current_time)
            if not hour_allowed:
                return False, hour_error

            # Record the request
            self._record_request(client_id, current_time)

            return True, None

    def _check_token_bucket(self, client_id: str, current_time: float) -> bool:
        """
        Check token bucket for burst protection.

        Args:
            client_id: Client identifier
            current_time: Current timestamp

        Returns:
            True if request is allowed
        """
        # Refill tokens based on time elapsed
        time_elapsed = current_time - self._last_refill[client_id]
        tokens_to_add = time_elapsed * (self.config.requests_per_minute / 60.0)

        self._tokens[client_id] = min(
            self.config.burst_size,
            self._tokens[client_id] + tokens_to_add
        )
        self._last_refill[client_id] = current_time

        # Check if we have tokens available
        if self._tokens[client_id] >= 1.0:
            self._tokens[client_id] -= 1.0
            return True

        return False

    def _check_minute_limit(self, client_id: str, current_time: float) -> Tuple[bool, Optional[ValidationError]]:
        """
        Check requests per minute limit.

        Args:
            client_id: Client identifier
            current_time: Current timestamp

        Returns:
            Tuple of (is_allowed, error_if_rate_limited)
        """
        minute_window = current_time - 60

        # Remove old requests
        minute_queue = self._minute_requests[client_id]
        while minute_queue and minute_queue[0] < minute_window:
            minute_queue.popleft()

        # Check limit
        if len(minute_queue) >= self.config.requests_per_minute:
            return False, ValidationError.security_error(
                ErrorCode.RATE_LIMIT_EXCEEDED,
                "Requests per minute limit exceeded",
                {
                    "client_id": client_id,
                    "limit_type": "minute",
                    "current_count": len(minute_queue),
                    "limit": self.config.requests_per_minute,
                    "reset_time": minute_queue[0] + 60 if minute_queue else current_time + 60
                }
            )

        return True, None

    def _check_hour_limit(self, client_id: str, current_time: float) -> Tuple[bool, Optional[ValidationError]]:
        """
        Check requests per hour limit.

        Args:
            client_id: Client identifier
            current_time: Current timestamp

        Returns:
            Tuple of (is_allowed, error_if_rate_limited)
        """
        hour_window = current_time - 3600

        # Remove old requests
        hour_queue = self._hour_requests[client_id]
        while hour_queue and hour_queue[0] < hour_window:
            hour_queue.popleft()

        # Check limit
        if len(hour_queue) >= self.config.requests_per_hour:
            return False, ValidationError.security_error(
                ErrorCode.RATE_LIMIT_EXCEEDED,
                "Requests per hour limit exceeded",
                {
                    "client_id": client_id,
                    "limit_type": "hour",
                    "current_count": len(hour_queue),
                    "limit": self.config.requests_per_hour,
                    "reset_time": hour_queue[0] + 3600 if hour_queue else current_time + 3600
                }
            )

        return True, None

    def _record_request(self, client_id: str, current_time: float) -> None:
        """
        Record a successful request.

        Args:
            client_id: Client identifier
            current_time: Current timestamp
        """
        self._minute_requests[client_id].append(current_time)
        self._hour_requests[client_id].append(current_time)

    def _cleanup_old_entries(self, current_time: float) -> None:
        """
        Clean up old tracking entries.

        Args:
            current_time: Current timestamp
        """
        # Clean up minute tracking
        minute_cutoff = current_time - 60
        for client_id in list(self._minute_requests.keys()):
            queue = self._minute_requests[client_id]
            while queue and queue[0] < minute_cutoff:
                queue.popleft()
            if not queue:
                del self._minute_requests[client_id]

        # Clean up hour tracking
        hour_cutoff = current_time - 3600
        for client_id in list(self._hour_requests.keys()):
            queue = self._hour_requests[client_id]
            while queue and queue[0] < hour_cutoff:
                queue.popleft()
            if not queue:
                del self._hour_requests[client_id]

        # Clean up token buckets for inactive clients
        inactive_cutoff = current_time - 3600  # 1 hour
        for client_id in list(self._last_refill.keys()):
            if self._last_refill[client_id] < inactive_cutoff:
                del self._tokens[client_id]
                del self._last_refill[client_id]

    def get_client_status(self, client_id: str) -> Dict[str, any]:
        """
        Get current rate limit status for a client.

        Args:
            client_id: Client identifier

        Returns:
            Dictionary with rate limit status
        """
        with self._lock:
            current_time = time.time()

            minute_queue = self._minute_requests[client_id]
            hour_queue = self._hour_requests[client_id]

            # Calculate remaining requests
            minute_remaining = max(0, self.config.requests_per_minute - len(minute_queue))
            hour_remaining = max(0, self.config.requests_per_hour - len(hour_queue))

            # Calculate reset times
            minute_reset = None
            if minute_queue:
                minute_reset = minute_queue[0] + 60

            hour_reset = None
            if hour_queue:
                hour_reset = hour_queue[0] + 3600

            return {
                "client_id": client_id,
                "requests_per_minute": {
                    "current": len(minute_queue),
                    "limit": self.config.requests_per_minute,
                    "remaining": minute_remaining,
                    "reset_time": minute_reset
                },
                "requests_per_hour": {
                    "current": len(hour_queue),
                    "limit": self.config.requests_per_hour,
                    "remaining": hour_remaining,
                    "reset_time": hour_reset
                },
                "tokens": {
                    "current": self._tokens[client_id],
                    "max": self.config.burst_size
                }
            }

    def reset_client(self, client_id: str) -> None:
        """
        Reset rate limits for a specific client.

        Args:
            client_id: Client identifier to reset
        """
        with self._lock:
            self._minute_requests.pop(client_id, None)
            self._hour_requests.pop(client_id, None)
            self._tokens[client_id] = self.config.burst_size
            self._last_refill[client_id] = time.time()

    def update_config(self, config: RateLimitConfig) -> None:
        """
        Update rate limit configuration.

        Args:
            config: New rate limit configuration
        """
        with self._lock:
            self.config = config

            # Reset token buckets to new burst size
            current_time = time.time()
            for client_id in self._tokens:
                self._tokens[client_id] = min(config.burst_size, self._tokens[client_id])
                self._last_refill[client_id] = current_time

    def get_stats(self) -> Dict[str, any]:
        """
        Get overall rate limiter statistics.

        Returns:
            Dictionary with rate limiter statistics
        """
        with self._lock:
            return {
                "active_clients": len(self._minute_requests),
                "total_tracked_minute_requests": sum(len(q) for q in self._minute_requests.values()),
                "total_tracked_hour_requests": sum(len(q) for q in self._hour_requests.values()),
                "config": {
                    "requests_per_minute": self.config.requests_per_minute,
                    "requests_per_hour": self.config.requests_per_hour,
                    "burst_size": self.config.burst_size,
                    "cleanup_interval": self.config.cleanup_interval
                }
            }
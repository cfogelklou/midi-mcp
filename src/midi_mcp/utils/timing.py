# -*- coding: utf-8 -*-
"""
Timing utilities for MIDI MCP Server.

Provides timing measurement utilities for performance monitoring,
latency tracking, and real-time operation validation.
"""
#
#   __author__ = "Chris Fogelklou"
#   __email__ = "chris.fogelklou@gmail.com"
#   __copyright__ = "Copyright 2025"
#   __license__ = "MIT"
#
#   (with lots of help from AI agents)
#

import time
import asyncio
import logging
from typing import Optional, Callable, Any, Dict
from contextlib import contextmanager, asynccontextmanager
from functools import wraps


class Timer:
    """High-precision timer for measuring operation latency."""
    
    def __init__(self, name: Optional[str] = None) -> None:
        """
        Initialize timer.
        
        Args:
            name: Optional name for the timer (used in logging)
        """
        self.name = name or "Timer"
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.logger = logging.getLogger(__name__)
    
    def start(self) -> None:
        """Start the timer."""
        self.start_time = time.perf_counter()
        self.end_time = None
    
    def stop(self) -> float:
        """
        Stop the timer and return elapsed time.
        
        Returns:
            Elapsed time in seconds
        """
        if self.start_time is None:
            raise ValueError("Timer was not started")
        
        self.end_time = time.perf_counter()
        return self.elapsed
    
    @property
    def elapsed(self) -> float:
        """Get elapsed time in seconds."""
        if self.start_time is None:
            raise ValueError("Timer was not started")
        
        end = self.end_time or time.perf_counter()
        return end - self.start_time
    
    @property
    def elapsed_ms(self) -> float:
        """Get elapsed time in milliseconds."""
        return self.elapsed * 1000.0
    
    def reset(self) -> None:
        """Reset the timer."""
        self.start_time = None
        self.end_time = None


@contextmanager
def measure_latency(operation_name: str = "operation", log_result: bool = True):
    """
    Context manager to measure operation latency.
    
    Args:
        operation_name: Name of the operation being measured
        log_result: Whether to log the measured latency
        
    Yields:
        Timer instance for manual access to timing data
    """
    timer = Timer(operation_name)
    logger = logging.getLogger(__name__)
    
    try:
        timer.start()
        yield timer
    finally:
        elapsed_ms = timer.stop() * 1000.0
        if log_result:
            logger.debug(f"{operation_name} completed in {elapsed_ms:.2f}ms")


@asynccontextmanager
async def measure_async_latency(operation_name: str = "async_operation", log_result: bool = True):
    """
    Async context manager to measure operation latency.
    
    Args:
        operation_name: Name of the operation being measured
        log_result: Whether to log the measured latency
        
    Yields:
        Timer instance for manual access to timing data
    """
    timer = Timer(operation_name)
    logger = logging.getLogger(__name__)
    
    try:
        timer.start()
        yield timer
    finally:
        elapsed_ms = timer.stop() * 1000.0
        if log_result:
            logger.debug(f"{operation_name} completed in {elapsed_ms:.2f}ms")


def time_function(log_result: bool = True, threshold_ms: Optional[float] = None):
    """
    Decorator to measure function execution time.
    
    Args:
        log_result: Whether to log the execution time
        threshold_ms: Only log if execution time exceeds this threshold
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            timer = Timer(func.__name__)
            timer.start()
            
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                elapsed_ms = timer.stop() * 1000.0
                
                if log_result and (threshold_ms is None or elapsed_ms > threshold_ms):
                    logger = logging.getLogger(func.__module__)
                    logger.debug(f"{func.__name__} executed in {elapsed_ms:.2f}ms")
        
        return wrapper
    return decorator


def time_async_function(log_result: bool = True, threshold_ms: Optional[float] = None):
    """
    Decorator to measure async function execution time.
    
    Args:
        log_result: Whether to log the execution time
        threshold_ms: Only log if execution time exceeds this threshold
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            timer = Timer(func.__name__)
            timer.start()
            
            try:
                result = await func(*args, **kwargs)
                return result
            finally:
                elapsed_ms = timer.stop() * 1000.0
                
                if log_result and (threshold_ms is None or elapsed_ms > threshold_ms):
                    logger = logging.getLogger(func.__module__)
                    logger.debug(f"{func.__name__} executed in {elapsed_ms:.2f}ms")
        
        return wrapper
    return decorator


class LatencyTracker:
    """Track latency statistics over time."""
    
    def __init__(self, max_samples: int = 1000) -> None:
        """
        Initialize latency tracker.
        
        Args:
            max_samples: Maximum number of samples to keep in memory
        """
        self.max_samples = max_samples
        self.samples: list[float] = []
        self.logger = logging.getLogger(__name__)
    
    def add_sample(self, latency_ms: float) -> None:
        """Add a latency sample."""
        self.samples.append(latency_ms)
        
        # Keep only the most recent samples
        if len(self.samples) > self.max_samples:
            self.samples = self.samples[-self.max_samples:]
    
    def get_stats(self) -> Dict[str, float]:
        """Get latency statistics."""
        if not self.samples:
            return {
                "count": 0,
                "min": 0.0,
                "max": 0.0,
                "avg": 0.0,
                "p50": 0.0,
                "p95": 0.0,
                "p99": 0.0
            }
        
        sorted_samples = sorted(self.samples)
        count = len(sorted_samples)
        
        return {
            "count": count,
            "min": sorted_samples[0],
            "max": sorted_samples[-1],
            "avg": sum(sorted_samples) / count,
            "p50": sorted_samples[int(count * 0.5)],
            "p95": sorted_samples[int(count * 0.95)],
            "p99": sorted_samples[int(count * 0.99)]
        }
    
    def reset(self) -> None:
        """Reset all samples."""
        self.samples.clear()
        self.logger.debug("Latency tracker reset")


# Global latency tracker for the entire server
global_latency_tracker = LatencyTracker()
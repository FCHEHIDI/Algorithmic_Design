"""
Generic resource pool for managing collections of resources.
Supports concurrent access and filtering.
"""

from typing import TypeVar, Generic, List, Callable, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

logger = logging.getLogger(__name__)

# Generic type for resources (Technician or Equipment)
T = TypeVar('T')


class ResourcePool(Generic[T]):
    """
    Manages a pool of resources of a specific type.
    Thread-safe for concurrent access.
    Generic class that works with any resource type.
    """
    
    def __init__(self, resources: List[T], resource_type: str):
        """
        Initialize resource pool.
        
        Args:
            resources: List of resource objects
            resource_type: String description for logging
        """
        self._resources = resources
        self._type = resource_type
        logger.info(f"ResourcePool created: {len(resources)} {resource_type}")
    
    def find_available(self, 
                      at_time: int, 
                      filter_fn: Optional[Callable[[T], bool]] = None) -> Optional[T]:
        """
        Find first available resource matching filter at given time.
        
        Args:
            at_time: Time to check availability
            filter_fn: Optional filter function
            
        Returns:
            First available resource or None
        """
        candidates = [r for r in self._resources if r.is_available_at(at_time)]
        
        if filter_fn:
            candidates = [r for r in candidates if filter_fn(r)]
        
        if not candidates:
            return None
        
        # Return the one that becomes available earliest
        return min(candidates, key=lambda r: r.available_from)
    
    def find_all_available(self,
                          at_time: int,
                          filter_fn: Optional[Callable[[T], bool]] = None) -> List[T]:
        """
        Find all available resources matching filter at given time.
        
        Args:
            at_time: Time to check availability
            filter_fn: Optional filter function
            
        Returns:
            List of available resources
        """
        candidates = [r for r in self._resources if r.is_available_at(at_time)]
        
        if filter_fn:
            candidates = [r for r in candidates if filter_fn(r)]
        
        return candidates
    
    def find_available_concurrent(self,
                                 at_time: int,
                                 filter_fn: Optional[Callable[[T], bool]] = None,
                                 max_workers: int = 4) -> Optional[T]:
        """
        Find available resource using concurrent processing.
        Useful for large resource pools.
        
        Args:
            at_time: Time to check availability
            filter_fn: Optional filter function
            max_workers: Number of concurrent workers
            
        Returns:
            First available resource or None
        """
        if len(self._resources) < 10:
            # Not worth the overhead for small pools
            return self.find_available(at_time, filter_fn)
        
        # Split resources into chunks for parallel processing
        chunk_size = max(1, len(self._resources) // max_workers)
        chunks = [self._resources[i:i + chunk_size] 
                 for i in range(0, len(self._resources), chunk_size)]
        
        def check_chunk(chunk: List[T]) -> Optional[T]:
            """Check a chunk of resources."""
            for resource in chunk:
                if resource.is_available_at(at_time):
                    if filter_fn is None or filter_fn(resource):
                        return resource
            return None
        
        # Process chunks concurrently
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(check_chunk, chunk) for chunk in chunks]
            
            for future in as_completed(futures):
                result = future.result()
                if result is not None:
                    # Cancel remaining futures
                    for f in futures:
                        f.cancel()
                    return result
        
        return None
    
    def get_all_compatible(self, sample_type) -> List[T]:
        """
        Get all resources compatible with sample type.
        
        Args:
            sample_type: SampleType enum
            
        Returns:
            List of compatible resources
        """
        compatible = []
        for resource in self._resources:
            # Check if resource has can_handle or can_process method
            if hasattr(resource, 'can_handle') and resource.can_handle(sample_type):
                compatible.append(resource)
            elif hasattr(resource, 'can_process') and resource.can_process(sample_type):
                compatible.append(resource)
        return compatible
    
    def get_statistics(self) -> dict:
        """Get pool statistics."""
        total = len(self._resources)
        if total == 0:
            return {'total': 0, 'available': 0, 'busy': 0}
        
        available = sum(1 for r in self._resources if r.is_available_at(0))
        return {
            'total': total,
            'available': available,
            'busy': total - available,
            'utilization': ((total - available) / total) * 100
        }
    
    def __len__(self) -> int:
        """Return number of resources in pool."""
        return len(self._resources)
    
    def __iter__(self):
        """Allow iteration over resources."""
        return iter(self._resources)
    
    def __repr__(self) -> str:
        return f"ResourcePool({self._type}, {len(self._resources)} resources)"

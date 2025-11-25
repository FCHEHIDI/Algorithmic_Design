"""
Scheduling strategies implementing different algorithms.
Strategy pattern allows swapping algorithms without changing client code.
"""

from abc import ABC, abstractmethod
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

from lab_planner.domain.models import Sample, ScheduleEntry
from lab_planner.resources.manager import ResourceManager
from lab_planner.scheduling.schedule import Schedule

logger = logging.getLogger(__name__)


class SchedulingStrategy(ABC):
    """
    Abstract base class for scheduling algorithms.
    Strategy pattern - allows different scheduling approaches.
    """
    
    @abstractmethod
    def schedule(self, samples: List[Sample], resource_manager: ResourceManager) -> Schedule:
        """
        Create a schedule for given samples using available resources.
        
        Args:
            samples: List of Sample objects to schedule
            resource_manager: ResourceManager for finding resources
            
        Returns:
            Complete Schedule object with entries and metrics
        """
        pass
    
    @abstractmethod
    def name(self) -> str:
        """Return strategy name for logging and identification."""
        pass


class PriorityScheduler(SchedulingStrategy):
    """
    Priority-based scheduling strategy.
    Processes samples in strict priority order: STAT > URGENT > ROUTINE.
    Supports concurrent sample processing for improved performance.
    """
    
    def __init__(self, enable_concurrent: bool = True, max_workers: int = 4):
        """
        Initialize priority scheduler.
        
        Args:
            enable_concurrent: Enable concurrent sample processing
            max_workers: Number of worker threads for concurrent processing
        """
        self._enable_concurrent = enable_concurrent
        self._max_workers = max_workers
        logger.info(f"PriorityScheduler initialized (concurrent={enable_concurrent}, workers={max_workers})")
    
    def name(self) -> str:
        return "Priority-Based Scheduler (STAT > URGENT > ROUTINE)"
    
    def schedule(self, samples: List[Sample], resource_manager: ResourceManager) -> Schedule:
        """
        Schedule samples in strict priority order.
        
        Algorithm:
        1. Sort samples by priority (STAT > URGENT > ROUTINE)
        2. For each sample in order:
           a. Find compatible and available resources
           b. Reserve resources for calculated time slot
           c. Add entry to schedule
        3. Calculate and return metrics
        
        Args:
            samples: List of samples to schedule
            resource_manager: Manager for resource allocation
            
        Returns:
            Complete schedule with metrics
        """
        logger.info(f"Starting {self.name()}...")
        logger.info(f"Processing {len(samples)} samples")
        
        # Sort by priority (descending - highest priority first)
        sorted_samples = sorted(samples, key=lambda s: s.priority_value, reverse=True)
        
        # Log distribution
        from collections import Counter
        priority_dist = Counter(s.priority.name for s in sorted_samples)
        for priority, count in priority_dist.items():
            logger.info(f"  {priority}: {count} samples")
        
        # Choose scheduling approach based on settings and sample count
        if self._enable_concurrent and len(sorted_samples) > 10:
            logger.info("Using concurrent scheduling mode")
            schedule = self._schedule_concurrent(sorted_samples, resource_manager)
        else:
            logger.info("Using sequential scheduling mode")
            schedule = self._schedule_sequential(sorted_samples, resource_manager)
        
        logger.info(f"Scheduling complete: {len(schedule)} entries created")
        return schedule
    
    def _schedule_sequential(self, samples: List[Sample], resource_manager: ResourceManager) -> Schedule:
        """
        Schedule samples sequentially (traditional approach).
        Guaranteed to maintain strict priority order.
        
        Args:
            samples: Sorted list of samples
            resource_manager: Resource manager
            
        Returns:
            Schedule object
        """
        schedule = Schedule()
        
        for sample in samples:
            self._schedule_single_sample(sample, resource_manager, schedule)
        
        return schedule
    
    def _schedule_concurrent(self, samples: List[Sample], resource_manager: ResourceManager) -> Schedule:
        """
        Schedule samples with concurrent resource finding.
        
        Note: Maintains priority order by processing in batches of same priority.
        Within same priority level, samples can be processed concurrently.
        
        Args:
            samples: Sorted list of samples
            resource_manager: Resource manager
            
        Returns:
            Schedule object
        """
        schedule = Schedule()
        
        # Group samples by priority to maintain ordering
        from itertools import groupby
        
        for priority_value, group in groupby(samples, key=lambda s: s.priority_value):
            priority_samples = list(group)
            priority_name = priority_samples[0].priority.name
            
            logger.info(f"Processing {len(priority_samples)} {priority_name} samples concurrently")
            
            # Process samples of same priority concurrently
            with ThreadPoolExecutor(max_workers=self._max_workers) as executor:
                # Submit all samples for resource finding
                future_to_sample = {
                    executor.submit(
                        self._find_resources_for_sample,
                        sample,
                        resource_manager
                    ): sample
                    for sample in priority_samples
                }
                
                # Collect results and create schedule entries
                # Note: Entries may be created out of order within same priority
                for future in as_completed(future_to_sample):
                    sample = future_to_sample[future]
                    try:
                        tech, equip, start_time = future.result()
                        
                        if tech and equip:
                            self._create_and_add_entry(
                                sample, tech, equip, start_time, schedule
                            )
                        else:
                            schedule.add_conflict(sample.id)
                            logger.warning(f"Could not schedule {sample.id} - no resources")
                    
                    except Exception as e:
                        logger.error(f"Error scheduling {sample.id}: {e}")
                        schedule.add_conflict(sample.id)
        
        return schedule
    
    def _schedule_single_sample(self, 
                               sample: Sample, 
                               resource_manager: ResourceManager,
                               schedule: Schedule) -> None:
        """
        Schedule a single sample.
        
        Args:
            sample: Sample to schedule
            resource_manager: Resource manager
            schedule: Schedule to add entry to
        """
        tech, equip, start_time = resource_manager.find_resources_for(sample)
        
        if tech and equip:
            self._create_and_add_entry(sample, tech, equip, start_time, schedule)
            logger.info(f"✓ Scheduled {sample.id} ({sample.priority.name}, {sample.type.name}) "
                       f"→ Tech {tech.id}, Equip {equip.id}, [{start_time}-{start_time + sample.processing_time}]")
        else:
            schedule.add_conflict(sample.id)
            logger.warning(f"✗ Could not schedule {sample.id} - no available resources")
    
    def _find_resources_for_sample(self, sample: Sample, resource_manager: ResourceManager):
        """
        Find resources for a sample (used in concurrent mode).
        
        Args:
            sample: Sample to find resources for
            resource_manager: Resource manager
            
        Returns:
            (technician, equipment, start_time) tuple
        """
        return resource_manager.find_resources_for(sample)
    
    def _create_and_add_entry(self,
                             sample: Sample,
                             tech,
                             equip,
                             start_time: int,
                             schedule: Schedule) -> None:
        """
        Create schedule entry and reserve resources.
        
        Args:
            sample: Sample being scheduled
            tech: Technician resource
            equip: Equipment resource
            start_time: Calculated start time
            schedule: Schedule to add entry to
        """
        # Reserve resources (updates their availability)
        tech.reserve(start_time, sample.processing_time, sample.id)
        equip.reserve(start_time, sample.processing_time, sample.id)
        
        # Create schedule entry
        entry = ScheduleEntry(
            sample_id=sample.id,
            technician_id=tech.id,
            equipment_id=equip.id,
            start_time=start_time,
            end_time=start_time + sample.processing_time,
            priority=sample.priority
        )
        
        schedule.add_entry(entry)


class GreedyScheduler(SchedulingStrategy):
    """
    Greedy scheduling strategy - always assigns to earliest available resource.
    Ignores priority, focuses on minimizing total time.
    Useful for comparison and testing.
    """
    
    def name(self) -> str:
        return "Greedy Scheduler (Earliest Available)"
    
    def schedule(self, samples: List[Sample], resource_manager: ResourceManager) -> Schedule:
        """Schedule samples greedily without considering priority."""
        logger.info(f"Starting {self.name()}...")
        
        schedule = Schedule()
        
        # Sort by ready time instead of priority
        sorted_samples = sorted(samples, key=lambda s: s.ready_time)
        
        for sample in sorted_samples:
            tech, equip, start_time = resource_manager.find_resources_for(sample)
            
            if tech and equip:
                tech.reserve(start_time, sample.processing_time, sample.id)
                equip.reserve(start_time, sample.processing_time, sample.id)
                
                entry = ScheduleEntry(
                    sample_id=sample.id,
                    technician_id=tech.id,
                    equipment_id=equip.id,
                    start_time=start_time,
                    end_time=start_time + sample.processing_time,
                    priority=sample.priority
                )
                schedule.add_entry(entry)
            else:
                schedule.add_conflict(sample.id)
        
        return schedule

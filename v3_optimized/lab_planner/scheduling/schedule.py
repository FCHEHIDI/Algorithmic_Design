"""
Schedule aggregate - manages collection of scheduled entries.
"""

from typing import List
import logging

from lab_planner.domain.models import ScheduleEntry, Metrics

logger = logging.getLogger(__name__)


class Schedule:
    """
    Aggregate root for schedule entries.
    Manages collection of scheduled analyses and calculates metrics.
    """
    
    def __init__(self):
        self._entries: List[ScheduleEntry] = []
        self._conflicts: List[str] = []
    
    def add_entry(self, entry: ScheduleEntry) -> None:
        """
        Add a scheduled entry.
        
        Args:
            entry: ScheduleEntry to add
        """
        self._entries.append(entry)
        logger.debug(f"Added entry: {entry}")
    
    def add_conflict(self, sample_id: str) -> None:
        """
        Record a scheduling conflict (sample that couldn't be scheduled).
        
        Args:
            sample_id: ID of sample that couldn't be scheduled
        """
        self._conflicts.append(sample_id)
        logger.warning(f"Conflict recorded for sample {sample_id}")
    
    @property
    def entries(self) -> List[ScheduleEntry]:
        """Return copy of entries to prevent external modification."""
        return self._entries.copy()
    
    @property
    def conflicts(self) -> List[str]:
        """Return copy of conflicts to prevent external modification."""
        return self._conflicts.copy()
    
    @property
    def is_empty(self) -> bool:
        """Check if schedule has no entries."""
        return len(self._entries) == 0
    
    def calculate_metrics(self, total_samples: int = 0) -> Metrics:
        """
        Calculate performance metrics for this schedule.
        
        Args:
            total_samples: Total number of samples (for success rate calculation)
            
        Returns:
            Metrics object with performance data
        """
        if self.is_empty:
            return Metrics(
                total_time=0,
                efficiency=0.0,
                conflicts=len(self._conflicts),
                samples_scheduled=0,
                total_samples=total_samples
            )
        
        # Calculate time span (first start to last end)
        first_start = min(e.start_time for e in self._entries)
        last_end = max(e.end_time for e in self._entries)
        total_duration = last_end - first_start
        
        # Calculate total processing time
        total_processing = sum(e.duration for e in self._entries)
        
        # Efficiency: ratio of active processing time to total time span
        # Can exceed 100% when processing happens in parallel
        efficiency = (total_processing / total_duration) if total_duration > 0 else 0.0
        
        metrics = Metrics(
            total_time=total_duration,
            efficiency=efficiency,
            conflicts=len(self._conflicts),
            samples_scheduled=len(self._entries),
            total_samples=total_samples if total_samples > 0 else len(self._entries) + len(self._conflicts)
        )
        
        logger.info(f"Metrics calculated: duration={total_duration}, "
                   f"efficiency={efficiency:.1%}, "
                   f"scheduled={len(self._entries)}/{metrics.total_samples}")
        
        return metrics
    
    def get_entries_by_priority(self) -> dict:
        """Group entries by priority level."""
        from collections import defaultdict
        grouped = defaultdict(list)
        for entry in self._entries:
            grouped[entry.priority.name].append(entry)
        return dict(grouped)
    
    def get_timeline(self) -> List[dict]:
        """
        Get chronological timeline of all events.
        Useful for visualization and debugging.
        """
        timeline = []
        for entry in sorted(self._entries, key=lambda e: e.start_time):
            timeline.append({
                'time': entry.start_time,
                'event': 'START',
                'sample_id': entry.sample_id,
                'priority': entry.priority.name
            })
            timeline.append({
                'time': entry.end_time,
                'event': 'END',
                'sample_id': entry.sample_id,
                'priority': entry.priority.name
            })
        return sorted(timeline, key=lambda x: (x['time'], x['event']))
    
    def to_dict(self) -> dict:
        """
        Export schedule as JSON-compatible dictionary.
        
        Returns:
            Dictionary with schedule entries and metrics
        """
        total_samples = len(self._entries) + len(self._conflicts)
        metrics = self.calculate_metrics(total_samples)
        
        return {
            'schedule': [entry.to_dict() for entry in self._entries],
            'metrics': metrics.to_dict(),
            'conflicts': self._conflicts
        }
    
    def __len__(self) -> int:
        """Return number of scheduled entries."""
        return len(self._entries)
    
    def __repr__(self) -> str:
        return f"Schedule({len(self._entries)} entries, {len(self._conflicts)} conflicts)"

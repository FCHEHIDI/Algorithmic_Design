"""
Domain models, enums, and value objects for the lab planning system.
Implements immutable value objects and entities with proper encapsulation.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# ENUMS
# ============================================================================

class SampleType(Enum):
    """Types of laboratory samples."""
    BLOOD = "BLOOD"
    URINE = "URINE"
    TISSUE = "TISSUE"


class Priority(Enum):
    """Sample priority levels (value = numeric priority for sorting)."""
    STAT = 3      # Emergency - highest priority
    URGENT = 2    # Important - medium priority
    ROUTINE = 1   # Standard - lowest priority


class Speciality(Enum):
    """Technician specialities."""
    BLOOD = "BLOOD"
    URINE = "URINE"
    TISSUE = "TISSUE"
    GENERAL = "GENERAL"  # Can handle any type


# ============================================================================
# VALUE OBJECTS (Immutable)
# ============================================================================

@dataclass(frozen=True)
class Sample:
    """
    Represents a laboratory sample to be analyzed.
    Value object - immutable once created.
    """
    id: str
    type: SampleType
    priority: Priority
    ready_time: int
    processing_time: int
    patient_id: Optional[str] = None
    
    def __post_init__(self):
        """Validate sample data."""
        if self.processing_time <= 0:
            raise ValueError(f"Sample {self.id}: processing_time must be positive")
        if self.ready_time < 0:
            raise ValueError(f"Sample {self.id}: ready_time cannot be negative")
    
    @property
    def priority_value(self) -> int:
        """Numeric priority for sorting (higher = more urgent)."""
        return self.priority.value
    
    def can_be_handled_by(self, technician: 'Technician', equipment: 'Equipment') -> bool:
        """Check if this sample is compatible with given resources."""
        return (technician.can_handle(self.type) and 
                equipment.can_process(self.type))
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Sample':
        """Create Sample from dictionary (JSON deserialization)."""
        return cls(
            id=data['id'],
            type=SampleType[data['type']] if isinstance(data['type'], str) else data['type'],
            priority=Priority[data['priority']] if isinstance(data['priority'], str) else data['priority'],
            ready_time=data['ready_time'],
            processing_time=data['processing_time'],
            patient_id=data.get('patient_id')
        )
    
    def __repr__(self) -> str:
        return f"Sample({self.id}, {self.type.name}, {self.priority.name})"


@dataclass(frozen=True)
class ScheduleEntry:
    """
    Represents one scheduled analysis.
    Value object - immutable.
    """
    sample_id: str
    technician_id: str
    equipment_id: str
    start_time: int
    end_time: int
    priority: Priority
    
    def __post_init__(self):
        if self.end_time <= self.start_time:
            raise ValueError(f"Entry {self.sample_id}: end_time must be after start_time")
    
    @property
    def duration(self) -> int:
        """Duration of this scheduled entry."""
        return self.end_time - self.start_time
    
    def to_dict(self) -> dict:
        """Convert to JSON-serializable dictionary."""
        return {
            'sample_id': self.sample_id,
            'technician_id': self.technician_id,
            'equipment_id': self.equipment_id,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'priority': self.priority.name
        }
    
    def __repr__(self) -> str:
        return f"ScheduleEntry({self.sample_id}[{self.start_time}-{self.end_time}])"


@dataclass(frozen=True)
class Metrics:
    """Performance metrics for a schedule."""
    total_time: int
    efficiency: float
    conflicts: int
    samples_scheduled: int = 0
    total_samples: int = 0
    
    @property
    def success_rate(self) -> float:
        """Percentage of samples successfully scheduled."""
        if self.total_samples == 0:
            return 0.0
        return (self.samples_scheduled / self.total_samples) * 100
    
    def to_dict(self) -> dict:
        """Convert to JSON-serializable dictionary."""
        return {
            'total_time': self.total_time,
            'efficiency': round(self.efficiency, 4),
            'conflicts': self.conflicts,
            'samples_scheduled': self.samples_scheduled,
            'total_samples': self.total_samples,
            'success_rate': round(self.success_rate, 2)
        }


# ============================================================================
# ENTITIES (Mutable state)
# ============================================================================

class Technician:
    """
    Represents a laboratory technician resource.
    Entity - manages its own availability state.
    """
    
    def __init__(self, id: str, speciality: Speciality, available_from: int = 0):
        self._id = id
        self._speciality = speciality
        self._available_from = available_from
        self._assigned_samples: List[str] = []
        logger.debug(f"Created Technician {id} ({speciality.name})")
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def speciality(self) -> Speciality:
        return self._speciality
    
    @property
    def available_from(self) -> int:
        return self._available_from
    
    @property
    def assigned_samples(self) -> List[str]:
        """Return copy to prevent external modification."""
        return self._assigned_samples.copy()
    
    def can_handle(self, sample_type: SampleType) -> bool:
        """Check if technician can handle this sample type."""
        return (self._speciality == Speciality.GENERAL or 
                self._speciality.name == sample_type.name)
    
    def reserve(self, start_time: int, duration: int, sample_id: str) -> None:
        """
        Reserve this technician for a time slot.
        Updates availability and tracks assignment.
        """
        end_time = start_time + duration
        self._available_from = max(self._available_from, end_time)
        self._assigned_samples.append(sample_id)
        logger.debug(f"Technician {self._id} reserved until {self._available_from} for {sample_id}")
    
    def is_available_at(self, time: int) -> bool:
        """Check if technician is available at given time."""
        return self._available_from <= time
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Technician':
        """Create Technician from dictionary."""
        return cls(
            id=data['id'],
            speciality=Speciality[data['speciality']] if isinstance(data['speciality'], str) else data['speciality'],
            available_from=data.get('available_from', 0)
        )
    
    def __repr__(self) -> str:
        return f"Technician({self._id}, {self._speciality.name}, available_from={self._available_from})"


class Equipment:
    """
    Represents laboratory equipment resource.
    Entity - manages its own availability state.
    """
    
    def __init__(self, id: str, equipment_type: SampleType, available_from: int = 0):
        self._id = id
        self._type = equipment_type
        self._available_from = available_from
        self._assigned_samples: List[str] = []
        logger.debug(f"Created Equipment {id} ({equipment_type.name})")
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def type(self) -> SampleType:
        return self._type
    
    @property
    def available_from(self) -> int:
        return self._available_from
    
    @property
    def assigned_samples(self) -> List[str]:
        """Return copy to prevent external modification."""
        return self._assigned_samples.copy()
    
    def can_process(self, sample_type: SampleType) -> bool:
        """Check if equipment can process this sample type."""
        return self._type == sample_type
    
    def reserve(self, start_time: int, duration: int, sample_id: str) -> None:
        """
        Reserve this equipment for a time slot.
        Updates availability and tracks assignment.
        """
        end_time = start_time + duration
        self._available_from = max(self._available_from, end_time)
        self._assigned_samples.append(sample_id)
        logger.debug(f"Equipment {self._id} reserved until {self._available_from} for {sample_id}")
    
    def is_available_at(self, time: int) -> bool:
        """Check if equipment is available at given time."""
        return self._available_from <= time
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Equipment':
        """Create Equipment from dictionary."""
        return cls(
            id=data['id'],
            equipment_type=SampleType[data['type']] if isinstance(data['type'], str) else data['type'],
            available_from=data.get('available_from', 0)
        )
    
    def __repr__(self) -> str:
        return f"Equipment({self._id}, {self._type.name}, available_from={self._available_from})"

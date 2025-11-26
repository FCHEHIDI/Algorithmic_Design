# 🏗️ V3 ARCHITECTURE DESIGN - OOP + SOLID

## 🎯 Design Goals

1. **Single Responsibility Principle (SRP)**: Each class has one clear purpose
2. **Open/Closed Principle (OCP)**: Extensible without modifying existing code
3. **Liskov Substitution Principle (LSP)**: Subtypes can replace base types
4. **Interface Segregation Principle (ISP)**: Small, focused interfaces
5. **Dependency Inversion Principle (DIP)**: Depend on abstractions, not concretions

---

## 📦 Class Structure Overview

```
┌────────────────────────────────────────────────────────────┐
│                     DOMAIN MODELS                          │
├────────────────────────────────────────────────────────────┤
│  Sample          │ Represents a lab sample (immutable)     │
│  Technician      │ Represents a lab technician             │
│  Equipment       │ Represents lab equipment                │
│  ScheduleEntry   │ Represents one scheduled analysis       │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│                   RESOURCE MANAGEMENT                      │
├────────────────────────────────────────────────────────────┤
│  Resource        │ Abstract base for schedulable resources │
│  ResourcePool    │ Manages resources of one type           │
│  ResourceManager │ Coordinates all resource pools          │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│                    SCHEDULING ENGINE                       │
├────────────────────────────────────────────────────────────┤
│  SchedulingStrategy  │ Abstract scheduling algorithm       │
│  PriorityScheduler   │ Concrete: priority-based scheduling │
│  Schedule            │ Collection of schedule entries      │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│                     ORCHESTRATION                          │
├────────────────────────────────────────────────────────────┤
│  LabPlanner      │ Main facade/orchestrator                │
│  Validator       │ Input validation logic                  │
│  MetricsCalculator│ Performance metrics computation        │
└────────────────────────────────────────────────────────────┘
```

---

## 🔷 Domain Models (Value Objects & Entities)

### 1. **Sample** (Value Object - Immutable)

```python
@dataclass(frozen=True)
class Sample:
    """Represents a lab sample to be analyzed."""
    id: str
    type: SampleType  # Enum: BLOOD, URINE, TISSUE
    priority: Priority  # Enum: STAT, URGENT, ROUTINE
    ready_time: int
    processing_time: int
    patient_id: Optional[str] = None
    
    def __post_init__(self):
        """Validate sample data."""
        if self.processing_time <= 0:
            raise ValueError("Processing time must be positive")
        if self.ready_time < 0:
            raise ValueError("Ready time cannot be negative")
    
    @property
    def priority_value(self) -> int:
        """Numeric priority for sorting."""
        return self.priority.value
    
    def can_be_handled_by(self, technician: 'Technician', equipment: 'Equipment') -> bool:
        """Check if this sample is compatible with given resources."""
        return (technician.can_handle(self.type) and 
                equipment.can_process(self.type))
```

**Why frozen?** Samples shouldn't change once created. Immutability prevents bugs.

---

### 2. **Technician** (Entity - Mutable availability)

```python
class Technician:
    """Represents a lab technician resource."""
    
    def __init__(self, id: str, speciality: Speciality, available_from: int = 0):
        self._id = id
        self._speciality = speciality
        self._available_from = available_from
        self._assigned_samples: List[str] = []
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def speciality(self) -> Speciality:
        return self._speciality
    
    @property
    def available_from(self) -> int:
        return self._available_from
    
    def can_handle(self, sample_type: SampleType) -> bool:
        """Check if technician can handle this sample type."""
        return (self._speciality == Speciality.GENERAL or 
                self._speciality.name == sample_type.name)
    
    def reserve(self, start_time: int, duration: int, sample_id: str) -> None:
        """Reserve this technician for a time slot."""
        end_time = start_time + duration
        self._available_from = max(self._available_from, end_time)
        self._assigned_samples.append(sample_id)
        logger.debug(f"Technician {self._id} reserved until {self._available_from}")
    
    def is_available_at(self, time: int) -> bool:
        """Check if technician is available at given time."""
        return self._available_from <= time
```

**Key features:**
- Encapsulation: Private attributes with public properties
- Self-validating: Checks compatibility
- Tracks own availability

---

### 3. **Equipment** (Entity - Similar to Technician)

```python
class Equipment:
    """Represents lab equipment resource."""
    
    def __init__(self, id: str, equipment_type: SampleType, available_from: int = 0):
        self._id = id
        self._type = equipment_type
        self._available_from = available_from
        self._assigned_samples: List[str] = []
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def type(self) -> SampleType:
        return self._type
    
    @property
    def available_from(self) -> int:
        return self._available_from
    
    def can_process(self, sample_type: SampleType) -> bool:
        """Check if equipment can process this sample type."""
        return self._type == sample_type
    
    def reserve(self, start_time: int, duration: int, sample_id: str) -> None:
        """Reserve this equipment for a time slot."""
        end_time = start_time + duration
        self._available_from = max(self._available_from, end_time)
        self._assigned_samples.append(sample_id)
```

---

### 4. **ScheduleEntry** (Value Object)

```python
@dataclass(frozen=True)
class ScheduleEntry:
    """Represents one scheduled analysis."""
    sample_id: str
    technician_id: str
    equipment_id: str
    start_time: int
    end_time: int
    priority: Priority
    
    def __post_init__(self):
        if self.end_time <= self.start_time:
            raise ValueError("End time must be after start time")
    
    @property
    def duration(self) -> int:
        return self.end_time - self.start_time
    
    def to_dict(self) -> dict:
        """Convert to JSON-serializable dict."""
        return {
            'sample_id': self.sample_id,
            'technician_id': self.technician_id,
            'equipment_id': self.equipment_id,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'priority': self.priority.name
        }
```

---

## 🔧 Resource Management Layer

### 5. **ResourcePool[T]** (Generic Collection)

```python
from typing import TypeVar, Generic, List, Callable

T = TypeVar('T', Technician, Equipment)

class ResourcePool(Generic[T]):
    """Manages a pool of resources of a specific type."""
    
    def __init__(self, resources: List[T], resource_type: str):
        self._resources = resources
        self._type = resource_type
        logger.info(f"ResourcePool created: {len(resources)} {resource_type}")
    
    def find_available(self, 
                      at_time: int, 
                      filter_fn: Callable[[T], bool] = None) -> Optional[T]:
        """Find first available resource matching filter."""
        candidates = [r for r in self._resources if r.is_available_at(at_time)]
        
        if filter_fn:
            candidates = [r for r in candidates if filter_fn(r)]
        
        if not candidates:
            return None
        
        # Return the one that becomes available earliest
        return min(candidates, key=lambda r: r.available_from)
    
    def get_all_compatible(self, sample_type: SampleType) -> List[T]:
        """Get all resources compatible with sample type."""
        return [r for r in self._resources 
                if hasattr(r, 'can_handle') and r.can_handle(sample_type)
                or hasattr(r, 'can_process') and r.can_process(sample_type)]
    
    def __len__(self) -> int:
        return len(self._resources)
```

**Why Generic?** Same logic works for Technicians and Equipment.

---

### 6. **ResourceManager** (Facade Pattern)

```python
class ResourceManager:
    """Coordinates access to all resource pools."""
    
    def __init__(self, technicians: List[Technician], equipment: List[Equipment]):
        # Index technicians by speciality
        self._tech_pools: Dict[Speciality, ResourcePool[Technician]] = {}
        for speciality in Speciality:
            techs = [t for t in technicians if t.speciality == speciality]
            if techs:
                self._tech_pools[speciality] = ResourcePool(techs, f"Technician-{speciality.name}")
        
        # Index equipment by type
        self._equip_pools: Dict[SampleType, ResourcePool[Equipment]] = {}
        for sample_type in SampleType:
            equips = [e for e in equipment if e.type == sample_type]
            if equips:
                self._equip_pools[sample_type] = ResourcePool(equips, f"Equipment-{sample_type.name}")
    
    def find_resources_for(self, sample: Sample) -> Tuple[Optional[Technician], Optional[Equipment], int]:
        """
        Find compatible and available technician + equipment for sample.
        
        Returns:
            (technician, equipment, earliest_start_time)
        """
        # Get compatible technicians (specific + GENERAL)
        compatible_techs: List[Technician] = []
        if sample.type.name in [s.name for s in Speciality if s != Speciality.GENERAL]:
            pool = self._tech_pools.get(Speciality[sample.type.name])
            if pool:
                compatible_techs.extend(pool.get_all_compatible(sample.type))
        
        # Always add GENERAL techs
        if Speciality.GENERAL in self._tech_pools:
            compatible_techs.extend(self._tech_pools[Speciality.GENERAL]._resources)
        
        # Get compatible equipment
        equip_pool = self._equip_pools.get(sample.type)
        if not equip_pool:
            logger.warning(f"No equipment available for {sample.type}")
            return None, None, -1
        
        compatible_equips = equip_pool.get_all_compatible(sample.type)
        
        # Find best combination
        best_tech = None
        best_equip = None
        best_start = float('inf')
        
        for tech in compatible_techs:
            for equip in compatible_equips:
                start = max(sample.ready_time, tech.available_from, equip.available_from)
                if start < best_start:
                    best_start = start
                    best_tech = tech
                    best_equip = equip
        
        if best_tech and best_equip:
            return best_tech, best_equip, int(best_start)
        
        return None, None, -1
```

**Responsibilities:**
- Abstracts resource lookup complexity
- Single point of coordination
- Hides internal pool structure

---

## 🎯 Scheduling Engine

### 7. **SchedulingStrategy** (Strategy Pattern)

```python
from abc import ABC, abstractmethod

class SchedulingStrategy(ABC):
    """Abstract base for scheduling algorithms."""
    
    @abstractmethod
    def schedule(self, 
                samples: List[Sample], 
                resource_manager: ResourceManager) -> 'Schedule':
        """
        Create a schedule for given samples using available resources.
        
        Returns:
            Complete Schedule object
        """
        pass
    
    @abstractmethod
    def name(self) -> str:
        """Return strategy name for logging."""
        pass
```

**Why Abstract?** Allows multiple algorithms (priority-based, time-optimized, etc.)

---

### 8. **PriorityScheduler** (Concrete Strategy)

```python
class PriorityScheduler(SchedulingStrategy):
    """Priority-based scheduling: STAT > URGENT > ROUTINE."""
    
    def name(self) -> str:
        return "Priority-Based Scheduler"
    
    def schedule(self, samples: List[Sample], resource_manager: ResourceManager) -> 'Schedule':
        """Schedule samples in strict priority order."""
        logger.info(f"Starting {self.name()}...")
        
        # Sort by priority (already sorted if using index, but explicit)
        sorted_samples = sorted(samples, key=lambda s: s.priority_value, reverse=True)
        
        schedule = Schedule()
        
        for sample in sorted_samples:
            tech, equip, start_time = resource_manager.find_resources_for(sample)
            
            if tech and equip:
                # Reserve resources
                tech.reserve(start_time, sample.processing_time, sample.id)
                equip.reserve(start_time, sample.processing_time, sample.id)
                
                # Create entry
                entry = ScheduleEntry(
                    sample_id=sample.id,
                    technician_id=tech.id,
                    equipment_id=equip.id,
                    start_time=start_time,
                    end_time=start_time + sample.processing_time,
                    priority=sample.priority
                )
                
                schedule.add_entry(entry)
                logger.info(f"Scheduled {sample.id} ({sample.priority.name}) at [{start_time}-{entry.end_time}]")
            else:
                schedule.add_conflict(sample.id)
                logger.warning(f"Could not schedule {sample.id} - no resources available")
        
        return schedule
```

---

### 9. **Schedule** (Aggregate Root)

```python
class Schedule:
    """Collection of scheduled entries with metrics."""
    
    def __init__(self):
        self._entries: List[ScheduleEntry] = []
        self._conflicts: List[str] = []
    
    def add_entry(self, entry: ScheduleEntry) -> None:
        """Add a scheduled entry."""
        self._entries.append(entry)
    
    def add_conflict(self, sample_id: str) -> None:
        """Record a scheduling conflict."""
        self._conflicts.append(sample_id)
    
    @property
    def entries(self) -> List[ScheduleEntry]:
        return self._entries.copy()  # Return copy to prevent modification
    
    @property
    def conflicts(self) -> List[str]:
        return self._conflicts.copy()
    
    def calculate_metrics(self) -> 'Metrics':
        """Calculate performance metrics."""
        if not self._entries:
            return Metrics(total_time=0, efficiency=0.0, conflicts=len(self._conflicts))
        
        first_start = min(e.start_time for e in self._entries)
        last_end = max(e.end_time for e in self._entries)
        total_duration = last_end - first_start
        
        total_processing = sum(e.duration for e in self._entries)
        efficiency = (total_processing / total_duration) if total_duration > 0 else 0.0
        
        return Metrics(
            total_time=total_duration,
            efficiency=efficiency,
            conflicts=len(self._conflicts)
        )
    
    def to_dict(self) -> dict:
        """Export as JSON-compatible dict."""
        metrics = self.calculate_metrics()
        return {
            'schedule': [entry.to_dict() for entry in self._entries],
            'metrics': metrics.to_dict()
        }
```

---

## 🎭 Orchestration Layer

### 10. **LabPlanner** (Facade)

```python
class LabPlanner:
    """
    Main entry point - orchestrates the entire planning process.
    Facade pattern: Simple interface hiding complex subsystems.
    """
    
    def __init__(self, strategy: SchedulingStrategy = None):
        self._strategy = strategy or PriorityScheduler()
        self._validator = Validator()
    
    def planify(self, 
                samples_data: List[dict], 
                techs_data: List[dict], 
                equips_data: List[dict]) -> dict:
        """
        Main planning function - coordinates all components.
        
        Steps:
        1. Validate inputs
        2. Build domain objects
        3. Create resource manager
        4. Run scheduling strategy
        5. Return results with metrics
        """
        logger.info("="*60)
        logger.info(f"LAB PLANNER V3 - {self._strategy.name()}")
        logger.info("="*60)
        
        # Step 1: Validate
        self._validator.validate_all(samples_data, techs_data, equips_data)
        
        # Step 2: Build domain objects
        samples = [Sample(**s) for s in samples_data]
        technicians = [Technician(**t) for t in techs_data]
        equipment = [Equipment(**e) for e in equips_data]
        
        logger.info(f"Loaded: {len(samples)} samples, {len(technicians)} techs, {len(equipment)} equips")
        
        # Step 3: Create resource manager
        resource_manager = ResourceManager(technicians, equipment)
        
        # Step 4: Run scheduling
        schedule = self._strategy.schedule(samples, resource_manager)
        
        # Step 5: Return results
        result = schedule.to_dict()
        
        logger.info("="*60)
        logger.info(f"COMPLETED: {len(schedule.entries)}/{len(samples)} samples scheduled")
        logger.info("="*60)
        
        return result
```

**Why Facade?**
- Simple interface for complex system
- Hides subsystem complexity
- Single point of entry

---

## 📊 Supporting Classes

### Enums

```python
from enum import Enum

class SampleType(Enum):
    BLOOD = "BLOOD"
    URINE = "URINE"
    TISSUE = "TISSUE"

class Priority(Enum):
    STAT = 3
    URGENT = 2
    ROUTINE = 1

class Speciality(Enum):
    BLOOD = "BLOOD"
    URINE = "URINE"
    TISSUE = "TISSUE"
    GENERAL = "GENERAL"
```

### Metrics

```python
@dataclass
class Metrics:
    total_time: int
    efficiency: float
    conflicts: int
    
    def to_dict(self) -> dict:
        return {
            'total_time': self.total_time,
            'efficiency': self.efficiency,
            'conflicts': self.conflicts
        }
```

---

## 🔄 Dependency Flow

```
User Code
    ↓
LabPlanner (Facade)
    ↓
    ├─→ Validator
    ├─→ Domain Objects (Sample, Technician, Equipment)
    ├─→ ResourceManager
    │       ↓
    │   ResourcePools
    ↓
SchedulingStrategy
    ↓
Schedule + Metrics
```

---

## ✅ SOLID Compliance

| Principle | How We Comply |
|-----------|---------------|
| **SRP** | Each class has one responsibility (Sample = data, ResourcePool = resource management, etc.) |
| **OCP** | New strategies can be added without modifying existing code (SchedulingStrategy interface) |
| **LSP** | Any SchedulingStrategy can replace another without breaking LabPlanner |
| **ISP** | Small, focused interfaces (can_handle, can_process) |
| **DIP** | LabPlanner depends on SchedulingStrategy interface, not concrete implementation |

---

## 🎯 Benefits Over V2

1. **Testability**: Each class can be unit tested independently
2. **Extensibility**: Easy to add new scheduling algorithms
3. **Maintainability**: Clear separation of concerns
4. **Type Safety**: Enums prevent invalid states
5. **Immutability**: Value objects prevent bugs
6. **Encapsulation**: Resources manage their own state
7. **Documentation**: Code structure documents itself

---

## 🚀 Next Steps

1. Implement the full class structure
2. Add unit tests for each component
3. Add advanced features (backtracking, optimization)
4. Performance profiling
5. Add time format conversion (HH:MM strings)

---

## 💬 Discussion Points

1. Should we use dependency injection framework?
2. Add event system for tracking state changes?
3. Implement command pattern for undo/redo?
4. Add persistence layer (database/file)?
5. Create separate validation rules classes?

Ready to implement! 🎯

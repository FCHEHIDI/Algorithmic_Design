"""
Main Lab Planner - Facade and orchestrator for the entire system.
Provides simple interface to complex subsystems.
"""

from typing import List, Dict, Any, Optional
import logging
import time

from lab_planner.domain.models import Sample, Technician, Equipment
from lab_planner.resources.manager import ResourceManager
from lab_planner.scheduling.strategies import SchedulingStrategy, PriorityScheduler
from lab_planner.orchestration.validator import Validator, ValidationError

logger = logging.getLogger(__name__)


class LabPlanner:
    """
    Main entry point for lab planning system.
    
    Facade pattern: Provides simple interface hiding complex subsystems.
    Orchestrates validation, resource management, and scheduling.
    
    Usage:
        planner = LabPlanner()
        result = planner.planify(samples_data, technicians_data, equipment_data)
    """
    
    def __init__(self, 
                 strategy: Optional[SchedulingStrategy] = None,
                 enable_concurrent: bool = True,
                 max_workers: int = 4):
        """
        Initialize lab planner.
        
        Args:
            strategy: Scheduling strategy to use (default: PriorityScheduler)
            enable_concurrent: Enable concurrent processing
            max_workers: Number of worker threads
        """
        self._strategy = strategy or PriorityScheduler(
            enable_concurrent=enable_concurrent,
            max_workers=max_workers
        )
        self._validator = Validator()
        self._enable_concurrent = enable_concurrent
        
        logger.info(f"LabPlanner initialized with {self._strategy.name()}")
        logger.info(f"Concurrent mode: {'enabled' if enable_concurrent else 'disabled'}")
    
    def planify(self,
               samples_data: List[Dict[str, Any]],
               technicians_data: List[Dict[str, Any]],
               equipment_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Main planning function - coordinates all components.
        
        Process:
        1. Validate inputs
        2. Build domain objects
        3. Create resource manager
        4. Run scheduling strategy
        5. Return results with metrics
        
        Args:
            samples_data: List of sample dictionaries
            technicians_data: List of technician dictionaries
            equipment_data: List of equipment dictionaries
            
        Returns:
            Dictionary with 'schedule', 'metrics', and 'conflicts'
            
        Raises:
            ValidationError: If input validation fails
        """
        start_time = time.time()
        
        logger.info("=" * 70)
        logger.info(f"LAB PLANNER V3 - {self._strategy.name()}")
        logger.info("=" * 70)
        
        try:
            # Step 1: Validate inputs
            self._validator.validate_all(samples_data, technicians_data, equipment_data)
            
            # Step 2: Build domain objects
            samples = self._build_samples(samples_data)
            technicians = self._build_technicians(technicians_data)
            equipment = self._build_equipment(equipment_data)
            
            logger.info(f"Domain objects created: {len(samples)} samples, "
                       f"{len(technicians)} technicians, {len(equipment)} equipment")
            
            # Step 3: Create resource manager
            resource_manager = ResourceManager(technicians, equipment)
            resource_manager.enable_concurrent_mode(self._enable_concurrent)
            
            # Step 4: Run scheduling strategy
            schedule = self._strategy.schedule(samples, resource_manager)
            
            # Step 5: Prepare results
            result = schedule.to_dict()
            
            # Ajouter métriques kernel si disponibles (pour KernelScheduler)
            if hasattr(self._strategy, 'kernel_metrics'):
                result['metrics'].update(self._strategy.kernel_metrics)
            
            # Add execution metadata
            execution_time = time.time() - start_time
            result['metadata'] = {
                'execution_time_seconds': round(execution_time, 3),
                'strategy': self._strategy.name(),
                'concurrent_mode': self._enable_concurrent,
                'version': '3.0.0'
            }
            
            logger.info("=" * 70)
            logger.info(f"COMPLETED: {len(schedule)}/{len(samples)} samples scheduled")
            logger.info(f"Execution time: {execution_time:.3f}s")
            logger.info(f"Efficiency: {result['metrics']['efficiency']:.1%}")
            logger.info("=" * 70)
            
            return result
        
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            raise
        
        except Exception as e:
            logger.error(f"Planning error: {e}", exc_info=True)
            raise
    
    def _build_samples(self, samples_data: List[Dict[str, Any]]) -> List[Sample]:
        """
        Build Sample domain objects from dictionaries.
        
        Args:
            samples_data: List of sample dictionaries
            
        Returns:
            List of Sample objects
        """
        samples = []
        for data in samples_data:
            try:
                sample = Sample.from_dict(data)
                samples.append(sample)
            except Exception as e:
                logger.error(f"Error creating sample from {data}: {e}")
                raise ValidationError(f"Invalid sample data: {e}")
        
        return samples
    
    def _build_technicians(self, technicians_data: List[Dict[str, Any]]) -> List[Technician]:
        """
        Build Technician domain objects from dictionaries.
        
        Args:
            technicians_data: List of technician dictionaries
            
        Returns:
            List of Technician objects
        """
        technicians = []
        for data in technicians_data:
            try:
                tech = Technician.from_dict(data)
                technicians.append(tech)
            except Exception as e:
                logger.error(f"Error creating technician from {data}: {e}")
                raise ValidationError(f"Invalid technician data: {e}")
        
        return technicians
    
    def _build_equipment(self, equipment_data: List[Dict[str, Any]]) -> List[Equipment]:
        """
        Build Equipment domain objects from dictionaries.
        
        Args:
            equipment_data: List of equipment dictionaries
            
        Returns:
            List of Equipment objects
        """
        equipment = []
        for data in equipment_data:
            try:
                equip = Equipment.from_dict(data)
                equipment.append(equip)
            except Exception as e:
                logger.error(f"Error creating equipment from {data}: {e}")
                raise ValidationError(f"Invalid equipment data: {e}")
        
        return equipment
    
    def set_strategy(self, strategy: SchedulingStrategy) -> None:
        """
        Change scheduling strategy.
        
        Args:
            strategy: New scheduling strategy to use
        """
        self._strategy = strategy
        logger.info(f"Scheduling strategy changed to: {strategy.name()}")
    
    def enable_concurrent_mode(self, enable: bool = True) -> None:
        """
        Enable or disable concurrent processing.
        
        Args:
            enable: True to enable, False to disable
        """
        self._enable_concurrent = enable
        logger.info(f"Concurrent mode {'enabled' if enable else 'disabled'}")

"""
Resource Manager - Facade for coordinating all resource pools.
Provides concurrent resource matching capabilities.
"""

from typing import List, Tuple, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

from lab_planner.domain.models import (
    Sample, Technician, Equipment, 
    SampleType, Speciality
)
from lab_planner.resources.pool import ResourcePool

logger = logging.getLogger(__name__)


class ResourceManager:
    """
    Coordinates access to all resource pools.
    Facade pattern - provides simple interface to complex resource management.
    Supports concurrent resource finding for improved performance.
    """
    
    def __init__(self, technicians: List[Technician], equipment: List[Equipment]):
        """
        Initialize resource manager with technician and equipment pools.
        
        Args:
            technicians: List of Technician objects
            equipment: List of Equipment objects
        """
        self._build_technician_pools(technicians)
        self._build_equipment_pools(equipment)
        self._enable_concurrent = len(technicians) > 10 or len(equipment) > 10
        
        logger.info(f"ResourceManager initialized (concurrent={'enabled' if self._enable_concurrent else 'disabled'})")
    
    def _build_technician_pools(self, technicians: List[Technician]) -> None:
        """Build indexed pools for technicians by speciality."""
        self._tech_pools = {}
        
        for speciality in Speciality:
            techs = [t for t in technicians if t.speciality == speciality]
            if techs:
                self._tech_pools[speciality] = ResourcePool(
                    techs, 
                    f"Technician-{speciality.name}"
                )
        
        logger.info(f"  Technician pools: {list(self._tech_pools.keys())}")
    
    def _build_equipment_pools(self, equipment: List[Equipment]) -> None:
        """Build indexed pools for equipment by type."""
        self._equip_pools = {}
        
        for sample_type in SampleType:
            equips = [e for e in equipment if e.type == sample_type]
            if equips:
                self._equip_pools[sample_type] = ResourcePool(
                    equips,
                    f"Equipment-{sample_type.name}"
                )
        
        logger.info(f"  Equipment pools: {list(self._equip_pools.keys())}")
    
    def find_resources_for(self, sample: Sample) -> Tuple[Optional[Technician], Optional[Equipment], int]:
        """
        Find compatible and available technician + equipment for sample.
        Uses indexed pools for O(1) type lookup.
        
        Args:
            sample: Sample object to find resources for
            
        Returns:
            (technician, equipment, earliest_start_time) or (None, None, -1)
        """
        # Get compatible technicians (specific type + GENERAL)
        compatible_techs = self._get_compatible_technicians(sample.type)
        
        # Get compatible equipment
        compatible_equips = self._get_compatible_equipment(sample.type)
        
        if not compatible_techs:
            logger.warning(f"No compatible technicians for {sample.id} (type: {sample.type.name})")
            return None, None, -1
        
        if not compatible_equips:
            logger.warning(f"No compatible equipment for {sample.id} (type: {sample.type.name})")
            return None, None, -1
        
        # Find best resource combination
        if self._enable_concurrent and len(compatible_techs) * len(compatible_equips) > 20:
            return self._find_best_combination_concurrent(
                sample, compatible_techs, compatible_equips
            )
        else:
            return self._find_best_combination(
                sample, compatible_techs, compatible_equips
            )
    
    def _get_compatible_technicians(self, sample_type: SampleType) -> List[Technician]:
        """Get all technicians compatible with sample type."""
        compatible = []
        
        # Add specific type technicians
        specific_speciality = Speciality[sample_type.name]
        if specific_speciality in self._tech_pools:
            compatible.extend(self._tech_pools[specific_speciality]._resources)
        
        # Add GENERAL technicians
        if Speciality.GENERAL in self._tech_pools:
            compatible.extend(self._tech_pools[Speciality.GENERAL]._resources)
        
        return compatible
    
    def _get_compatible_equipment(self, sample_type: SampleType) -> List[Equipment]:
        """Get all equipment compatible with sample type."""
        if sample_type in self._equip_pools:
            return list(self._equip_pools[sample_type]._resources)
        return []
    
    def _find_best_combination(self, 
                              sample: Sample,
                              techs: List[Technician],
                              equips: List[Equipment]) -> Tuple[Optional[Technician], Optional[Equipment], int]:
        """
        Find best technician-equipment combination (sequential).
        
        Returns:
            (best_tech, best_equip, earliest_start_time)
        """
        best_tech = None
        best_equip = None
        best_start = float('inf')
        
        for tech in techs:
            for equip in equips:
                start = max(
                    sample.ready_time,
                    tech.available_from,
                    equip.available_from
                )
                
                if start < best_start:
                    best_start = start
                    best_tech = tech
                    best_equip = equip
        
        if best_tech and best_equip:
            return best_tech, best_equip, int(best_start)
        
        return None, None, -1
    
    def _find_best_combination_concurrent(self,
                                         sample: Sample,
                                         techs: List[Technician],
                                         equips: List[Equipment]) -> Tuple[Optional[Technician], Optional[Equipment], int]:
        """
        Find best technician-equipment combination using concurrent processing.
        Useful for large resource pools.
        
        Returns:
            (best_tech, best_equip, earliest_start_time)
        """
        logger.debug(f"Using concurrent search for {sample.id} "
                    f"({len(techs)} techs × {len(equips)} equips)")
        
        def check_combination(tech: Technician, equip: Equipment) -> Tuple[int, Technician, Equipment]:
            """Calculate start time for this combination."""
            start = max(
                sample.ready_time,
                tech.available_from,
                equip.available_from
            )
            return (start, tech, equip)
        
        best_result = None
        best_start = float('inf')
        
        # Create all combinations and process concurrently
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [
                executor.submit(check_combination, tech, equip)
                for tech in techs
                for equip in equips
            ]
            
            for future in as_completed(futures):
                start, tech, equip = future.result()
                if start < best_start:
                    best_start = start
                    best_result = (tech, equip, int(start))
        
        if best_result:
            return best_result
        
        return None, None, -1
    
    def get_statistics(self) -> dict:
        """Get statistics for all resource pools."""
        stats = {
            'technicians': {},
            'equipment': {}
        }
        
        for speciality, pool in self._tech_pools.items():
            stats['technicians'][speciality.name] = pool.get_statistics()
        
        for sample_type, pool in self._equip_pools.items():
            stats['equipment'][sample_type.name] = pool.get_statistics()
        
        return stats
    
    def enable_concurrent_mode(self, enable: bool = True) -> None:
        """Enable or disable concurrent resource finding."""
        self._enable_concurrent = enable
        logger.info(f"Concurrent mode {'enabled' if enable else 'disabled'}")
    
    def get_all_technicians(self) -> List[Technician]:
        """Get all technicians from all pools (helper for kernel scheduler)."""
        all_techs = []
        for pool in self._tech_pools.values():
            all_techs.extend(pool._resources)
        return all_techs
    
    def get_all_equipment(self) -> List[Equipment]:
        """Get all equipment from all pools."""
        all_equip = []
        for pool in self._equip_pools.values():
            all_equip.extend(pool._resources)
        return all_equip
    
    def __repr__(self) -> str:
        return (f"ResourceManager("
                f"techs={sum(len(p) for p in self._tech_pools.values())}, "
                f"equips={sum(len(p) for p in self._equip_pools.values())})")

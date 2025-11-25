"""
Input validation for lab planning system.
Validates structure, data types, and business rules.
"""

from typing import List, Dict, Any
import logging

from lab_planner.domain.models import SampleType, Priority, Speciality

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class Validator:
    """
    Validates input data for the lab planning system.
    Single Responsibility: Input validation only.
    """
    
    # Valid values for enums
    VALID_SAMPLE_TYPES = {t.name for t in SampleType}
    VALID_PRIORITIES = {p.name for p in Priority}
    VALID_SPECIALITIES = {s.name for s in Speciality}
    
    def validate_all(self,
                    samples_data: List[Dict[str, Any]],
                    technicians_data: List[Dict[str, Any]],
                    equipment_data: List[Dict[str, Any]]) -> None:
        """
        Validate all input data.
        
        Args:
            samples_data: List of sample dictionaries
            technicians_data: List of technician dictionaries
            equipment_data: List of equipment dictionaries
            
        Raises:
            ValidationError: If validation fails
        """
        logger.info("Validating inputs...")
        
        # Check for empty inputs
        self._validate_not_empty(samples_data, technicians_data, equipment_data)
        
        # Validate each category
        self._validate_samples(samples_data)
        self._validate_technicians(technicians_data)
        self._validate_equipment(equipment_data)
        
        logger.info(f"✓ Validation successful: {len(samples_data)} samples, "
                   f"{len(technicians_data)} technicians, {len(equipment_data)} equipment")
    
    def _validate_not_empty(self,
                           samples: List,
                           technicians: List,
                           equipment: List) -> None:
        """Check that input lists are not empty."""
        if not samples:
            raise ValidationError("Samples list cannot be empty")
        if not technicians:
            raise ValidationError("Technicians list cannot be empty")
        if not equipment:
            raise ValidationError("Equipment list cannot be empty")
    
    def _validate_samples(self, samples: List[Dict[str, Any]]) -> None:
        """
        Validate sample data.
        
        Required fields: id, type, priority, ready_time, processing_time
        """
        required_fields = ['id', 'type', 'priority', 'ready_time', 'processing_time']
        
        for i, sample in enumerate(samples):
            # Check required fields
            for field in required_fields:
                if field not in sample:
                    raise ValidationError(
                        f"Sample {i} (id: {sample.get('id', 'unknown')}): "
                        f"missing required field '{field}'"
                    )
            
            # Validate types
            sample_id = sample['id']
            
            if not isinstance(sample['id'], str):
                raise ValidationError(f"Sample {i}: 'id' must be a string")
            
            if sample['type'] not in self.VALID_SAMPLE_TYPES:
                raise ValidationError(
                    f"Sample {sample_id}: invalid type '{sample['type']}'. "
                    f"Must be one of: {', '.join(self.VALID_SAMPLE_TYPES)}"
                )
            
            if sample['priority'] not in self.VALID_PRIORITIES:
                raise ValidationError(
                    f"Sample {sample_id}: invalid priority '{sample['priority']}'. "
                    f"Must be one of: {', '.join(self.VALID_PRIORITIES)}"
                )
            
            # Validate numeric values
            if not isinstance(sample['ready_time'], (int, float)) or sample['ready_time'] < 0:
                raise ValidationError(
                    f"Sample {sample_id}: 'ready_time' must be non-negative number"
                )
            
            if not isinstance(sample['processing_time'], (int, float)) or sample['processing_time'] <= 0:
                raise ValidationError(
                    f"Sample {sample_id}: 'processing_time' must be positive number"
                )
    
    def _validate_technicians(self, technicians: List[Dict[str, Any]]) -> None:
        """
        Validate technician data.
        
        Required fields: id, speciality, available_from
        """
        required_fields = ['id', 'speciality', 'available_from']
        
        for i, tech in enumerate(technicians):
            # Check required fields
            for field in required_fields:
                if field not in tech:
                    raise ValidationError(
                        f"Technician {i} (id: {tech.get('id', 'unknown')}): "
                        f"missing required field '{field}'"
                    )
            
            # Validate types
            tech_id = tech['id']
            
            if not isinstance(tech['id'], str):
                raise ValidationError(f"Technician {i}: 'id' must be a string")
            
            if tech['speciality'] not in self.VALID_SPECIALITIES:
                raise ValidationError(
                    f"Technician {tech_id}: invalid speciality '{tech['speciality']}'. "
                    f"Must be one of: {', '.join(self.VALID_SPECIALITIES)}"
                )
            
            if not isinstance(tech['available_from'], (int, float)) or tech['available_from'] < 0:
                raise ValidationError(
                    f"Technician {tech_id}: 'available_from' must be non-negative number"
                )
    
    def _validate_equipment(self, equipment: List[Dict[str, Any]]) -> None:
        """
        Validate equipment data.
        
        Required fields: id, type, available_from
        """
        required_fields = ['id', 'type', 'available_from']
        
        for i, equip in enumerate(equipment):
            # Check required fields
            for field in required_fields:
                if field not in equip:
                    raise ValidationError(
                        f"Equipment {i} (id: {equip.get('id', 'unknown')}): "
                        f"missing required field '{field}'"
                    )
            
            # Validate types
            equip_id = equip['id']
            
            if not isinstance(equip['id'], str):
                raise ValidationError(f"Equipment {i}: 'id' must be a string")
            
            if equip['type'] not in self.VALID_SAMPLE_TYPES:
                raise ValidationError(
                    f"Equipment {equip_id}: invalid type '{equip['type']}'. "
                    f"Must be one of: {', '.join(self.VALID_SAMPLE_TYPES)}"
                )
            
            if not isinstance(equip['available_from'], (int, float)) or equip['available_from'] < 0:
                raise ValidationError(
                    f"Equipment {equip_id}: 'available_from' must be non-negative number"
                )

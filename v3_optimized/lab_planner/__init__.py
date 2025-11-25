"""
Lab Planner V3 - Optimized OOP Implementation
Main package initialization and public API
"""

from lab_planner.orchestration.planner import LabPlanner
from lab_planner.domain.models import Sample, SampleType, Priority
from lab_planner.scheduling.strategies import PriorityScheduler

__version__ = "3.0.0"
__all__ = [
    'LabPlanner',
    'Sample',
    'SampleType',
    'Priority',
    'PriorityScheduler'
]

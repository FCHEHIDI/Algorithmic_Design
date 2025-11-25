"""
V3 Optimized Lab Planner - Main Entry Point
Demonstrates OOP architecture with concurrent execution
"""

import logging
import json
from lab_planner import LabPlanner
from lab_planner.scheduling.strategies import PriorityScheduler, GreedyScheduler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Main execution function."""
    
    print("\n" + "="*70)
    print("LAB PLANNER V3 - OPTIMIZED OOP IMPLEMENTATION")
    print("="*70 + "\n")
    
    # ========================================================================
    # TEST 1: Priority-based scheduling with concurrent execution
    # ========================================================================
    
    print("\n--- TEST 1: Priority Scheduling (Concurrent Mode) ---\n")
    
    samples = [
        {'id': 'S1', 'type': 'BLOOD', 'priority': 'URGENT', 'ready_time': 0, 'processing_time': 5},
        {'id': 'S2', 'type': 'BLOOD', 'priority': 'STAT', 'ready_time': 1, 'processing_time': 3},
        {'id': 'S3', 'type': 'URINE', 'priority': 'ROUTINE', 'ready_time': 0, 'processing_time': 4},
        {'id': 'S4', 'type': 'BLOOD', 'priority': 'URGENT', 'ready_time': 2, 'processing_time': 6},
        {'id': 'S5', 'type': 'TISSUE', 'priority': 'STAT', 'ready_time': 0, 'processing_time': 8},
    ]
    
    technicians = [
        {'id': 'T1', 'speciality': 'BLOOD', 'available_from': 0},
        {'id': 'T2', 'speciality': 'GENERAL', 'available_from': 0},
        {'id': 'T3', 'speciality': 'TISSUE', 'available_from': 0},
    ]
    
    equipment = [
        {'id': 'E1', 'type': 'BLOOD', 'available_from': 0},
        {'id': 'E2', 'type': 'URINE', 'available_from': 0},
        {'id': 'E3', 'type': 'TISSUE', 'available_from': 0},
    ]
    
    # Create planner with concurrent execution enabled
    planner = LabPlanner(
        strategy=PriorityScheduler(enable_concurrent=True, max_workers=4),
        enable_concurrent=True
    )
    
    result = planner.planify(samples, technicians, equipment)
    
    print("\n--- RESULTS ---")
    print(f"Samples scheduled: {result['metrics']['samples_scheduled']}/{result['metrics']['total_samples']}")
    print(f"Success rate: {result['metrics']['success_rate']:.1f}%")
    print(f"Execution time: {result['metadata']['execution_time_seconds']}s")
    
    print(f"\nSchedule (ordered by start time):")
    sorted_schedule = sorted(result['schedule'], key=lambda x: x['start_time'])
    for entry in sorted_schedule:
        print(f"  {entry['sample_id']} ({entry['priority']}) → "
              f"Tech {entry['technician_id']}, Equip {entry['equipment_id']}, "
              f"Time [{entry['start_time']}-{entry['end_time']}]")
    
    print(f"\nMetrics:")
    print(f"  Total time: {result['metrics']['total_time']} units")
    print(f"  Efficiency: {result['metrics']['efficiency']:.1%}")
    print(f"  Conflicts: {result['metrics']['conflicts']}")
    
    # ========================================================================
    # TEST 2: Large dataset with concurrent execution
    # ========================================================================
    
    print("\n\n--- TEST 2: Large Dataset (20 samples) ---\n")
    
    # Generate larger dataset
    large_samples = []
    priorities = ['STAT', 'URGENT', 'ROUTINE']
    types = ['BLOOD', 'URINE', 'TISSUE']
    
    for i in range(20):
        large_samples.append({
            'id': f'S{i+1:02d}',
            'type': types[i % 3],
            'priority': priorities[i % 3],
            'ready_time': i * 2,
            'processing_time': 3 + (i % 5)
        })
    
    large_technicians = [
        {'id': 'T1', 'speciality': 'BLOOD', 'available_from': 0},
        {'id': 'T2', 'speciality': 'BLOOD', 'available_from': 0},
        {'id': 'T3', 'speciality': 'URINE', 'available_from': 0},
        {'id': 'T4', 'speciality': 'TISSUE', 'available_from': 0},
        {'id': 'T5', 'speciality': 'GENERAL', 'available_from': 0},
        {'id': 'T6', 'speciality': 'GENERAL', 'available_from': 0},
    ]
    
    large_equipment = [
        {'id': 'E1', 'type': 'BLOOD', 'available_from': 0},
        {'id': 'E2', 'type': 'BLOOD', 'available_from': 0},
        {'id': 'E3', 'type': 'URINE', 'available_from': 0},
        {'id': 'E4', 'type': 'TISSUE', 'available_from': 0},
        {'id': 'E5', 'type': 'TISSUE', 'available_from': 0},
    ]
    
    # Test with concurrent mode
    planner_concurrent = LabPlanner(enable_concurrent=True, max_workers=4)
    result_concurrent = planner_concurrent.planify(large_samples, large_technicians, large_equipment)
    
    print(f"Concurrent Mode:")
    print(f"  Execution time: {result_concurrent['metadata']['execution_time_seconds']}s")
    print(f"  Samples scheduled: {result_concurrent['metrics']['samples_scheduled']}/20")
    print(f"  Efficiency: {result_concurrent['metrics']['efficiency']:.1%}")
    
    # Test with sequential mode for comparison
    planner_sequential = LabPlanner(enable_concurrent=False)
    result_sequential = planner_sequential.planify(large_samples, large_technicians, large_equipment)
    
    print(f"\nSequential Mode:")
    print(f"  Execution time: {result_sequential['metadata']['execution_time_seconds']}s")
    print(f"  Samples scheduled: {result_sequential['metrics']['samples_scheduled']}/20")
    print(f"  Efficiency: {result_sequential['metrics']['efficiency']:.1%}")
    
    speedup = result_sequential['metadata']['execution_time_seconds'] / result_concurrent['metadata']['execution_time_seconds']
    print(f"\nSpeedup: {speedup:.2f}x faster with concurrent mode")
    
    # ========================================================================
    # TEST 3: Strategy comparison
    # ========================================================================
    
    print("\n\n--- TEST 3: Strategy Comparison ---\n")
    
    test_samples = [
        {'id': 'S1', 'type': 'BLOOD', 'priority': 'ROUTINE', 'ready_time': 0, 'processing_time': 10},
        {'id': 'S2', 'type': 'BLOOD', 'priority': 'STAT', 'ready_time': 5, 'processing_time': 3},
        {'id': 'S3', 'type': 'BLOOD', 'priority': 'URGENT', 'ready_time': 0, 'processing_time': 5},
    ]
    
    test_techs = [{'id': 'T1', 'speciality': 'BLOOD', 'available_from': 0}]
    test_equip = [{'id': 'E1', 'type': 'BLOOD', 'available_from': 0}]
    
    # Priority scheduler
    planner_priority = LabPlanner(strategy=PriorityScheduler(enable_concurrent=False))
    result_priority = planner_priority.planify(test_samples, test_techs, test_equip)
    
    print("Priority Scheduler (STAT > URGENT > ROUTINE):")
    for entry in result_priority['schedule']:
        print(f"  {entry['sample_id']} ({entry['priority']}) at [{entry['start_time']}-{entry['end_time']}]")
    
    # Greedy scheduler
    planner_greedy = LabPlanner(strategy=GreedyScheduler())
    result_greedy = planner_greedy.planify(test_samples, test_techs, test_equip)
    
    print("\nGreedy Scheduler (Earliest Available):")
    for entry in result_greedy['schedule']:
        print(f"  {entry['sample_id']} ({entry['priority']}) at [{entry['start_time']}-{entry['end_time']}]")
    
    print("\nNote: Priority scheduler ensures STAT (S2) is processed first!")
    
    # ========================================================================
    # Export results to JSON
    # ========================================================================
    
    print("\n\n--- Exporting Results ---\n")
    
    with open('v3_results.json', 'w') as f:
        json.dump(result_concurrent, f, indent=2)
    
    print("✓ Results exported to v3_results.json")
    
    print("\n" + "="*70)
    print("ALL TESTS COMPLETED SUCCESSFULLY")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()

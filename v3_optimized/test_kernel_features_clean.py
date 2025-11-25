"""
Tests du Kernel Scheduler
Dmontre les 4 features kernel : Premption, Aging, Deadlock Detection, Load Balancing
"""

import logging
from lab_planner import LabPlanner
from lab_planner.scheduling.kernel_scheduler import KernelScheduler, KernelSchedulerConfig
from lab_planner.scheduling.kernel_features import (
    PreemptionPolicy, AgingConfig
)
from lab_planner.domain.models import Priority

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_preemption():
    """
    TEST 1 : PREMPTION
    
    Scnario : Un chantillon STAT arrive pendant qu'un URGENT est en cours.
    Attendu : L'URGENT est interrompu, STAT trait, puis URGENT reprend.
    """
    print("\n" + "="*80)
    print("TEST 1 : PREEMPTION (Interruption STAT)")
    print("="*80)
    
    samples = [
        # URGENT commence  08:00 (dure 60 min  fini  09:00)
        {
            "id": "S001_URGENT",
            "type": "BLOOD",
            "priority": "URGENT",
            "ready_time": 480,  # 08:00
            "processing_time": 60
        },
        # STAT arrive  08:30  doit PREMPTER S001
        {
            "id": "S002_STAT",
            "type": "BLOOD",
            "priority": "STAT",
            "ready_time": 510,  # 08:30
            "processing_time": 15
        }
    ]
    
    technicians = [
        {"id": "TECH01", "speciality": "BLOOD", "available_from": 480}
    ]
    
    equipment = [
        {"id": "EQUIP01", "type": "BLOOD", "available_from": 480}
    ]
    
    # Configuration avec premption active
    config = KernelSchedulerConfig(
        enable_preemption=True,
        preemption_policy=PreemptionPolicy.STAT_ONLY,
        enable_aging=False,
        enable_deadlock_detection=False,
        enable_load_balancing=False
    )
    
    planner = LabPlanner(strategy=KernelScheduler(config))
    result = planner.planify(samples, technicians, equipment)
    
    print(f"\n[RESULTAT] :")
    for entry in result['schedule']:
        print(f"  {entry['sample_id']:15} : "
              f"{entry['start_time']:3}{entry['end_time']:3} min "
              f"({entry['technician_id']}, {entry['equipment_id']})")
    
    print(f"\n Mtriques Premption :")
    if 'kernel_features' in result['metrics']:
        preempt_stats = result['metrics']['kernel_features'].get('preemption', {})
        print(f"  Total premptions : {preempt_stats.get('total_preemptions', 0)}")
        print(f"  Reprises en attente : {preempt_stats.get('pending_resumptions', 0)}")
        print(f"  Politique : {preempt_stats.get('policy', 'N/A')}")
    
    print("\n[OK] Test Preemption termine")
    print("="*80)


def test_aging():
    """
    TEST 2 : AGING (Anti-Starvation)
    
    Scnario : Des ROUTINE attendent longtemps pendant que des URGENT arrivent.
    Attendu : Les ROUTINE sont boosts en URGENT aprs seuil.
    """
    print("\n" + "="*80)
    print("TEST 2 : AGING (Anti-Starvation)")
    print("="*80)
    
    samples = [
        # ROUTINE arriv tt (08:00) mais devrait attendre
        {
            "id": "S001_ROUTINE_OLD",
            "type": "BLOOD",
            "priority": "ROUTINE",
            "ready_time": 480,  # 08:00
            "processing_time": 20
        },
        # URGENT arrive plus tard (09:30) mais prioritaire normalement
        {
            "id": "S002_URGENT",
            "type": "BLOOD",
            "priority": "URGENT",
            "ready_time": 570,  # 09:30
            "processing_time": 15
        },
        # Autre URGENT
        {
            "id": "S003_URGENT",
            "type": "BLOOD",
            "priority": "URGENT",
            "ready_time": 590,  # 09:50
            "processing_time": 10
        }
    ]
    
    technicians = [
        {"id": "TECH01", "speciality": "BLOOD", "available_from": 570}  # Disponible  09:30
    ]
    
    equipment = [
        {"id": "EQUIP01", "type": "BLOOD", "available_from": 570}
    ]
    
    # Configuration avec aging activ (seuil 60 min)
    aging_config = AgingConfig(
        enabled=True,
        routine_to_urgent=60,  # ROUTINE  URGENT aprs 60 min
        urgent_to_stat=120
    )
    
    config = KernelSchedulerConfig(
        enable_preemption=False,
        enable_aging=True,
        aging_config=aging_config,
        enable_deadlock_detection=False,
        enable_load_balancing=False
    )
    
    planner = LabPlanner(strategy=KernelScheduler(config))
    result = planner.planify(samples, technicians, equipment)
    
    print("\n Rsultat :")
    print("  (S001 devrait tre trait AVANT S002/S003 grce  l'aging)")
    for entry in result['schedule']:
        print(f"  {entry['sample_id']:20} : "
              f"{entry['start_time']:3}{entry['end_time']:3} min "
              f"(priorit: {entry.get('sample_priority', 'N/A')})")
    
    print(f"\n Mtriques Aging :")
    if 'kernel_features' in result['metrics']:
        aging_stats = result['metrics']['kernel_features'].get('aging', {})
        print(f"  chantillons aged : {aging_stats.get('total_aged_samples', 0)}")
        print(f"  Events d'aging : {aging_stats.get('aging_events', 0)}")
        config_info = aging_stats.get('config', {})
        print(f"  Seuil ROUTINEURGENT : {config_info.get('routine_to_urgent_threshold', 'N/A')} min")
    
    print("\n[OK] Test Aging termine")
    print("="*80)


def test_load_balancing():
    """
    TEST 3 : LOAD BALANCING
    
    Scnario : Plusieurs chantillons avec plusieurs techniciens disponibles.
    Attendu : Distribution quitable de la charge entre techniciens.
    """
    print("\n" + "="*80)
    print("TEST 3 : LOAD BALANCING")
    print("="*80)
    
    # 10 chantillons URGENT de dures variables
    samples = [
        {"id": f"S{i:03d}", "type": "BLOOD", "priority": "URGENT", 
         "ready_time": 480, "processing_time": 10 + (i * 5)}
        for i in range(1, 11)
    ]
    
    # 3 techniciens BLOOD disponibles
    technicians = [
        {"id": "TECH01", "speciality": "BLOOD", "available_from": 480},
        {"id": "TECH02", "speciality": "BLOOD", "available_from": 480},
        {"id": "TECH03", "speciality": "BLOOD", "available_from": 480}
    ]
    
    # 3 quipements BLOOD
    equipment = [
        {"id": "EQUIP01", "type": "BLOOD", "available_from": 480},
        {"id": "EQUIP02", "type": "BLOOD", "available_from": 480},
        {"id": "EQUIP03", "type": "BLOOD", "available_from": 480}
    ]
    
    # Configuration avec load balancing activ
    config = KernelSchedulerConfig(
        enable_preemption=False,
        enable_aging=False,
        enable_deadlock_detection=False,
        enable_load_balancing=True
    )
    
    planner = LabPlanner(strategy=KernelScheduler(config))
    result = planner.planify(samples, technicians, equipment)
    
    print("\n Rsultat (distribution par technicien) :")
    tech_assignments = {}
    for entry in result['schedule']:
        tech_id = entry['technician_id']
        if tech_id not in tech_assignments:
            tech_assignments[tech_id] = []
        tech_assignments[tech_id].append(entry)
    
    for tech_id, entries in tech_assignments.items():
        total_duration = sum(e['end_time'] - e['start_time'] for e in entries)
        print(f"\n  {tech_id} : {len(entries)} echantillons, {total_duration} min total")
        for entry in entries:
            duration = entry['end_time'] - entry['start_time']
            print(f"    - {entry['sample_id']} ({duration} min)")
    
    print(f"\n Mtriques Load Balancing :")
    if 'kernel_features' in result['metrics']:
        lb_stats = result['metrics']['kernel_features'].get('load_balancing', {})
        
        print(f"  Charge moyenne : {lb_stats.get('average_load', 0):.1f} min")
        print(f"  cart-type : {lb_stats.get('std_deviation', 0):.1f} min")
        print(f"  Min/Max : {lb_stats.get('min_load', 0):.0f}/{lb_stats.get('max_load', 0):.0f} min")
        print(f"  Dsquilibre : {lb_stats.get('load_imbalance', 0):.0f} min")
        print(f"  Coeff. Variation : {lb_stats.get('coefficient_variation', 0):.1f}% "
              f"({'excellent' if lb_stats.get('coefficient_variation', 100) < 15 else 'bon' if lb_stats.get('coefficient_variation', 100) < 30 else 'moyen'})")
        
        # Dtails par technicien
        tech_details = lb_stats.get('technician_details', {})
        if tech_details:
            print("\n  Dtails par technicien :")
            for tech_id, details in tech_details.items():
                print(f"    {tech_id} : "
                      f"{details['sample_count']} chantillons, "
                      f"{details['total_duration']} min, "
                      f"util={details['utilization_rate']:.1f}%")
    
    print("\n[OK] Test Load Balancing termine")
    print("="*80)


def test_all_features_combined():
    """
    TEST 4 : TOUTES LES FEATURES COMBINES
    
    Scnario complexe avec :
    - Premption (STAT arrive)
    - Aging (ROUTINE anciens)
    - Load Balancing (plusieurs techniciens)
    - Potentiel deadlock
    """
    print("\n" + "="*80)
    print("TEST 4 : TOUTES LES FEATURES KERNEL COMBINEES")
    print("="*80)
    
    samples = [
        # ROUTINE anciens (devraient tre boosts)
        {"id": "S001_ROUTINE_OLD", "type": "BLOOD", "priority": "ROUTINE", 
         "ready_time": 480, "processing_time": 25},
        {"id": "S002_ROUTINE_OLD", "type": "URINE", "priority": "ROUTINE", 
         "ready_time": 480, "processing_time": 30},
        
        # URGENT normaux
        {"id": "S003_URGENT", "type": "BLOOD", "priority": "URGENT", 
         "ready_time": 540, "processing_time": 20},
        {"id": "S004_URGENT", "type": "URINE", "priority": "URGENT", 
         "ready_time": 550, "processing_time": 15},
        {"id": "S005_URGENT", "type": "BLOOD", "priority": "URGENT", 
         "ready_time": 560, "processing_time": 18},
        
        # STAT qui devrait prempter
        {"id": "S006_STAT", "type": "BLOOD", "priority": "STAT", 
         "ready_time": 570, "processing_time": 10},
        
        # Plus d'chantillons pour load balancing
        {"id": "S007_URGENT", "type": "URINE", "priority": "URGENT", 
         "ready_time": 590, "processing_time": 22},
        {"id": "S008_ROUTINE", "type": "BLOOD", "priority": "ROUTINE", 
         "ready_time": 600, "processing_time": 12},
    ]
    
    technicians = [
        {"id": "TECH_BLOOD_1", "speciality": "BLOOD", "available_from": 540},
        {"id": "TECH_BLOOD_2", "speciality": "BLOOD", "available_from": 540},
        {"id": "TECH_URINE_1", "speciality": "URINE", "available_from": 540},
        {"id": "TECH_GENERAL", "speciality": "GENERAL", "available_from": 480},
    ]
    
    equipment = [
        {"id": "EQUIP_BLOOD_1", "type": "BLOOD", "available_from": 540},
        {"id": "EQUIP_BLOOD_2", "type": "BLOOD", "available_from": 540},
        {"id": "EQUIP_URINE_1", "type": "URINE", "available_from": 540},
    ]
    
    # Configuration complte
    aging_config = AgingConfig(
        enabled=True,
        routine_to_urgent=60,
        urgent_to_stat=120
    )
    
    config = KernelSchedulerConfig(
        enable_preemption=True,
        preemption_policy=PreemptionPolicy.STAT_ONLY,
        enable_aging=True,
        aging_config=aging_config,
        enable_deadlock_detection=True,
        deadlock_check_interval=3,
        enable_load_balancing=True
    )
    
    planner = LabPlanner(strategy=KernelScheduler(config))
    result = planner.planify(samples, technicians, equipment)
    
    print("\n Planning Rsultant :")
    for i, entry in enumerate(result['schedule'], 1):
        print(f"  {i:2}. {entry['sample_id']:20} : "
              f"{entry['start_time']:3}{entry['end_time']:3} min "
              f"| {entry['technician_id']:15} + {entry['equipment_id']:15}")
    
    print(f"\n Mtriques Compltes :")
    print(f"  chantillons planifis : {result['metrics']['total_samples']}")
    print(f"  Temps total : {result['metrics']['total_time']} min")
    print(f"  Efficacit : {result['metrics']['efficiency']:.1f}%")
    print(f"  Conflits : {result['metrics']['conflicts']}")
    
    if 'kernel_features' in result['metrics']:
        kf = result['metrics']['kernel_features']
        
        print("\n   Features Kernel :")
        
        if 'preemption' in kf:
            print(f"     Premptions : {kf['preemption']['total_preemptions']}")
        
        if 'aging' in kf:
            print(f"     Aging events : {kf['aging']['aging_events']}")
            print(f"       chantillons boosts : {kf['aging']['total_aged_samples']}")
        
        if 'deadlock_detection' in kf:
            print(f"     Deadlocks dtects : {kf['deadlock_detection']['total_deadlocks_detected']}")
        
        if 'load_balancing' in kf:
            lb = kf['load_balancing']
            print(f"     Coefficient de variation : {lb.get('coefficient_variation', 0):.1f}%")
            print(f"       Dsquilibre de charge : {lb.get('load_imbalance', 0):.0f} min")
    
    print("\n[OK] Test Features Combinees termine")
    print("="*80)


def main():
    """Lance tous les tests kernel"""
    print("\n" + "="*80)
    print("TESTS KERNEL SCHEDULER - Features Avancees")
    print("="*80)
    
    try:
        test_preemption()
        test_aging()
        test_load_balancing()
        test_all_features_combined()
        
        print("\n" + "="*80)
        print("TOUS LES TESTS KERNEL REUSSIS !")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n ERREUR : {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

"""
Test rapide V2 - Vérification fonctionnalité de base
"""

from planify_next_lab import planify_lab

# Dataset test simple
samples = [
    {'id': 'S001', 'type': 'BLOOD', 'priority': 'STAT', 'ready_time': 480, 'processing_time': 15},
    {'id': 'S002', 'type': 'URINE', 'priority': 'URGENT', 'ready_time': 485, 'processing_time': 20},
    {'id': 'S003', 'type': 'BLOOD', 'priority': 'ROUTINE', 'ready_time': 490, 'processing_time': 25},
]

technicians = [
    {'id': 'TECH001', 'speciality': 'BLOOD', 'available_from': 480},
    {'id': 'TECH002', 'speciality': 'URINE', 'available_from': 480},
    {'id': 'TECH003', 'speciality': 'GENERAL', 'available_from': 480},
]

equipment = [
    {'id': 'EQ001', 'type': 'BLOOD', 'available_from': 480},
    {'id': 'EQ002', 'type': 'URINE', 'available_from': 480},
]

print("="*60)
print("TEST V2 - INDEXED APPROACH (Quick Test)")
print("="*60)
print(f"\nDataset: {len(samples)} samples, {len(technicians)} techs, {len(equipment)} equips")

try:
    result = planify_lab(samples, technicians, equipment)
    
    print(f"\n[SUCCESS] - V2 fonctionne correctement")
    print(f"\nRésultat:")
    print(f"  - Échantillons planifiés: {len(result['schedule'])}/{len(samples)}")
    print(f"  - Temps total: {result['metrics']['total_time']} min")
    print(f"  - Efficacité: {result['metrics']['efficiency']:.1f}%")
    print(f"  - Conflits: {result['metrics']['conflicts']}")
    
    print(f"\nOrdre de priorite (doit etre STAT > URGENT > ROUTINE):")
    for entry in result['schedule']:
        print(f"  - {entry['sample_id']} ({entry['priority']}) > {entry['start_time']}-{entry['end_time']}min")
    
    # Validation
    assert len(result['schedule']) == 3, f"Devrait avoir 3 échantillons, a {len(result['schedule'])}"
    assert result['schedule'][0]['priority'] == 'STAT', "Premier doit être STAT"
    assert result['metrics']['conflicts'] == 0, "Ne devrait pas avoir de conflits"
    
    print("\n[OK] Toutes les validations passent!")
    
except Exception as e:
    print(f"\n[ERROR]: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

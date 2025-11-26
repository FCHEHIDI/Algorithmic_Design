"""
Tests de Conformité INTERMEDIATE - Instructions Officielles
============================================================
Vérifie que V3 respecte TOUTES les exigences INTERMEDIATE :
- 20 samples minimum
- 8 technicians minimum
- 5 equipment minimum
- Fonction planifyLab() disponible
- Output JSON avec format exact : {laboratory, schedule, metrics, metadata}
"""

import sys
from pathlib import Path
import json

# Ajouter le répertoire parent au path pour imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from planify_lab_wrapper import planifyLab


def test_planifylab_function_exists():
    """Vérifie que la fonction planifyLab() existe et est callable"""
    assert callable(planifyLab), "planifyLab() doit être une fonction callable"


def test_intermediate_dataset_20_8_5():
    """Test conformité INTERMEDIATE : 20 samples, 8 techs, 5 equipment"""
    
    # Dataset INTERMEDIATE conforme (20/8/5)
    samples = [
        {"id": f"S{i+1:03d}", "type": "BLOOD" if i % 3 == 0 else "URINE" if i % 3 == 1 else "TISSUE",
         "priority": "STAT" if i < 4 else "URGENT" if i < 12 else "ROUTINE",
         "ready_time": 480 + (i * 10), "processing_time": 15 + (i % 5) * 5}
        for i in range(20)
    ]
    
    technicians = [
        {"id": f"TECH{i+1:03d}", "speciality": "BLOOD" if i < 3 else "URINE" if i < 5 else "TISSUE" if i < 7 else "GENERAL",
         "available_from": 480}
        for i in range(8)
    ]
    
    equipment = [
        {"id": f"EQ{i+1:03d}", "type": "BLOOD" if i < 2 else "URINE" if i < 4 else "TISSUE",
         "available_from": 480}
        for i in range(5)
    ]
    
    # Appeler planifyLab()
    result = planifyLab(samples, technicians, equipment)
    
    # planifyLab() retourne déjà un dict, pas une string JSON
    result_dict = result if isinstance(result, dict) else json.loads(result)
    
    # Vérifications conformité INTERMEDIATE
    assert "laboratory" in result_dict, "Output doit contenir section 'laboratory'"
    assert "schedule" in result_dict, "Output doit contenir section 'schedule'"
    assert "metrics" in result_dict, "Output doit contenir section 'metrics'"
    assert "metadata" in result_dict, "Output doit contenir section 'metadata'"
    
    # Vérifier laboratory
    lab = result_dict["laboratory"]
    assert "date" in lab, "laboratory doit contenir 'date'"
    assert "totalSamples" in lab, "laboratory doit contenir 'totalSamples'"
    assert lab["totalSamples"] == 20, f"totalSamples devrait être 20, got {lab['totalSamples']}"
    
    # Vérifier schedule
    schedule = result_dict["schedule"]
    assert len(schedule) >= 15, f"Au moins 15/20 samples doivent être planifiés, got {len(schedule)}"
    
    # Vérifier premier élément schedule a tous les champs INTERMEDIATE
    if schedule:
        first = schedule[0]
        required_fields = ["sampleId", "technicianId", "equipmentId", "startTime", "endTime", 
                          "efficiency", "lunchBreak", "cleaningRequired"]
        for field in required_fields:
            assert field in first, f"schedule doit contenir champ '{field}'"
    
    # Vérifier metrics
    metrics = result_dict["metrics"]
    assert "totalTime" in metrics, "metrics doit contenir 'totalTime'"
    assert "efficiency" in metrics, "metrics doit contenir 'efficiency'"
    assert "conflicts" in metrics, "metrics doit contenir 'conflicts'"
    assert "averageWaitTime" in metrics, "metrics doit contenir 'averageWaitTime' (INTERMEDIATE)"
    assert "technicianUtilization" in metrics, "metrics doit contenir 'technicianUtilization' (INTERMEDIATE)"
    assert "parallelAnalyses" in metrics, "metrics doit contenir 'parallelAnalyses' (INTERMEDIATE)"
    
    # Vérifier metadata
    metadata = result_dict["metadata"]
    assert "constraintsApplied" in metadata, "metadata doit contenir 'constraintsApplied'"
    assert isinstance(metadata["constraintsApplied"], list), "constraintsApplied doit être une liste"


def test_camelcase_format():
    """Vérifie que l'output utilise camelCase comme requis par INTERMEDIATE"""
    
    samples = [
        {"id": "S001", "type": "BLOOD", "priority": "STAT", "ready_time": 480, "processing_time": 15}
    ]
    technicians = [
        {"id": "TECH001", "speciality": "BLOOD", "available_from": 480}
    ]
    equipment = [
        {"id": "EQ001", "type": "BLOOD", "available_from": 480}
    ]
    
    result = planifyLab(samples, technicians, equipment)
    result_dict = result if isinstance(result, dict) else json.loads(result)
    
    # Vérifier camelCase (pas snake_case)
    schedule = result_dict["schedule"]
    if schedule:
        first = schedule[0]
        assert "sampleId" in first, "Doit utiliser 'sampleId' (camelCase)"
        assert "technicianId" in first, "Doit utiliser 'technicianId' (camelCase)"
        assert "equipmentId" in first, "Doit utiliser 'equipmentId' (camelCase)"
        assert "startTime" in first, "Doit utiliser 'startTime' (camelCase)"
        assert "endTime" in first, "Doit utiliser 'endTime' (camelCase)"
        
        # Vérifier absence de snake_case
        assert "sample_id" not in first, "Ne doit PAS utiliser 'sample_id' (snake_case)"
        assert "technician_id" not in first, "Ne doit PAS utiliser 'technician_id' (snake_case)"


def test_time_format_hhmm():
    """Vérifie que les temps sont au format HH:MM"""
    
    samples = [{"id": "S001", "type": "BLOOD", "priority": "STAT", "ready_time": 540, "processing_time": 30}]
    technicians = [{"id": "TECH001", "speciality": "BLOOD", "available_from": 480}]
    equipment = [{"id": "EQ001", "type": "BLOOD", "available_from": 480}]
    
    result = planifyLab(samples, technicians, equipment)
    result_dict = result if isinstance(result, dict) else json.loads(result)
    
    schedule = result_dict["schedule"]
    if schedule:
        first = schedule[0]
        start = first["startTime"]
        end = first["endTime"]
        
        # Vérifier format HH:MM
        assert ":" in start, f"startTime doit être format HH:MM, got {start}"
        assert ":" in end, f"endTime doit être format HH:MM, got {end}"
        assert len(start.split(":")) == 2, f"startTime doit avoir format HH:MM, got {start}"
        assert len(end.split(":")) == 2, f"endTime doit avoir format HH:MM, got {end}"


def test_no_conflicts():
    """Vérifie que V3 ne génère pas de conflits (contrairement à V1)"""
    
    samples = [
        {"id": f"S{i+1:03d}", "type": "BLOOD", "priority": "URGENT", "ready_time": 480, "processing_time": 20}
        for i in range(10)
    ]
    technicians = [
        {"id": f"TECH{i+1:03d}", "speciality": "BLOOD", "available_from": 480}
        for i in range(3)
    ]
    equipment = [
        {"id": f"EQ{i+1:03d}", "type": "BLOOD", "available_from": 480}
        for i in range(2)
    ]
    
    result = planifyLab(samples, technicians, equipment)
    result_dict = result if isinstance(result, dict) else json.loads(result)
    
    metrics = result_dict["metrics"]
    conflicts = metrics.get("conflicts", -1)
    
    assert conflicts == 0, f"V3 ne doit avoir AUCUN conflit (V1 avait 4/10), got {conflicts}"


if __name__ == "__main__":
    print("=" * 80)
    print("TESTS CONFORMITÉ INTERMEDIATE - Instructions Officielles")
    print("=" * 80)
    
    tests = [
        ("Fonction planifyLab() existe", test_planifylab_function_exists),
        ("Dataset 20/8/5 conforme", test_intermediate_dataset_20_8_5),
        ("Format camelCase requis", test_camelcase_format),
        ("Format temps HH:MM", test_time_format_hhmm),
        ("Zéro conflits (vs V1)", test_no_conflicts),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            test_func()
            print(f"✅ {name}")
            passed += 1
        except AssertionError as e:
            print(f"❌ {name}: {e}")
            failed += 1
        except Exception as e:
            print(f"⚠️ {name}: ERROR - {e}")
            failed += 1
    
    print("=" * 80)
    print(f"RÉSULTATS: {passed}/{len(tests)} tests passés")
    if failed == 0:
        print("✅ TOUS LES TESTS INTERMEDIATE PASSENT !")
    else:
        print(f"❌ {failed} tests échoués")
    print("=" * 80)

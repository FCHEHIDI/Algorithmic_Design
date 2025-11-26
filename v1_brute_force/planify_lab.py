""" INPUT: Un objet avec
- samples[] : Liste des échantillons à analyser
- technicians[] : Liste des techniciens disponibles  
- equipment[] : Liste des équipements du labo"""

# imports

# God function version simple brute force approach
from typing import List, Dict, Any
JSON = Dict[str, Any]

def planify_lab(samples : list, technicians : list, equipment : list) -> JSON:
    """ OUTPUT: Un dictionnaire avec la planification optimale des échantillons
    {
        'schedule' : [
            {
                'sample_id' : str(sample_id),
                'technician_id' : str(technician_id),
                'equipment_id' : str(equipment_id),
                'start_time' : str(start_time),
                'end_time' : str(end_time),
                'priority' : str(priority_level)
        }
        ],
        'metrics' : {
            'total_time' : int(total_time),
            'efficiency' : float(samples_processed) / total_time,
            'conflicts' : int(number_of_conflicts)}
    }

    """

    # Valider les entrées (vide, types, champs requis etc.)

    if not samples or not technicians or not equipment:
        raise ValueError("Les listes d'échantillons, de techniciens et d'équipements ne doivent pas être vides.")
    
    # Validation des champs requis
    for sample in samples:
        required_fields = ['id', 'priority', 'type', 'ready_time', 'processing_time']
        for field in required_fields:
            if field not in sample:
                raise ValueError(f"L'échantillon {sample.get('id', 'unknown')} manque le champ '{field}'.")
    
    for tech in technicians:
        required_fields = ['id', 'speciality', 'available_from']
        for field in required_fields:
            if field not in tech:
                raise ValueError(f"Le technicien {tech.get('id', 'unknown')} manque le champ '{field}'.")
    
    for equip in equipment:
        required_fields = ['id', 'type', 'available_from']
        for field in required_fields:
            if field not in equip:
                raise ValueError(f"L'équipement {equip.get('id', 'unknown')} manque le champ '{field}'.")
    

    # Vérifier la priorité des échantillons et trier en conséquence
    # Priority mapping: STAT (3) > URGENT (2) > ROUTINE (1)
    PRIORITY_MAP = {'STAT': 3, 'URGENT': 2, 'ROUTINE': 1}
    samples.sort(key=lambda x: PRIORITY_MAP.get(x['priority'], 0), reverse=True)

    # Vérifier la disponibilité des techniciens et équipements
    technician_availability = {tech['id']: tech['available_from'] for tech in technicians}
    equipment_availability = {equip['id']: equip['available_from'] for equip in equipment}

    # Initialiser la planification
    schedule = []
    total_time = 0
    conflicts = 0
    samples_processed = 0

    # Parcourir chaque échantillon pour l'assigner
    for sample in samples:
        assigned = False
        for tech in technicians:
            # Vérifier la compatibilité technicien-échantillon
            tech_speciality = tech.get('speciality', '')
            sample_type = sample.get('type', '')
            if tech_speciality != sample_type and tech_speciality != 'GENERAL':
                continue  # Technicien incompatible, passer au suivant
            
            for equip in equipment:
                # Vérifier la compatibilité équipement-échantillon
                equip_type = equip.get('type', '')
                if equip_type != sample_type:
                    continue  # Équipement incompatible, passer au suivant
                
                # Vérifier la disponibilité
                if (technician_availability[tech['id']] <= sample['ready_time'] and
                    equipment_availability[equip['id']] <= sample['ready_time']):
                    
                    # Assigner l'échantillon
                    start_time = max(sample['ready_time'], technician_availability[tech['id']], equipment_availability[equip['id']])
                    end_time = start_time + sample['processing_time']
                    
                    schedule.append({
                        'sample_id': sample['id'],
                        'technician_id': tech['id'],
                        'equipment_id': equip['id'],
                        'start_time': start_time,
                        'end_time': end_time,
                        'priority': sample['priority']
                    })
                    
                    # Mettre à jour la disponibilité
                    technician_availability[tech['id']] = end_time
                    equipment_availability[equip['id']] = end_time
                    
                    total_time += sample['processing_time']
                    samples_processed += 1
                    assigned = True
                    break
            if assigned:
                break
        if not assigned:
            conflicts += 1

    # Calculer l'efficacité
    efficiency = samples_processed / total_time if total_time > 0 else 0

    # Construire le résultat final
    result = {
        'schedule': schedule,
        'metrics': {
            'total_time': total_time,
            'efficiency': efficiency,
            'conflicts': conflicts
        }
    }

    return result

# Example usage
if __name__ == "__main__":
    samples = [
        {'id': 'S1', 'type': 'BLOOD', 'priority': 'URGENT', 'ready_time': 0, 'processing_time': 5},
        {'id': 'S2', 'type': 'BLOOD', 'priority': 'STAT', 'ready_time': 1, 'processing_time': 3},
        {'id': 'S3', 'type': 'URINE', 'priority': 'ROUTINE', 'ready_time': 0, 'processing_time': 4},
    ]
    technicians = [
        {'id': 'T1', 'speciality': 'BLOOD', 'available_from': 0},
        {'id': 'T2', 'speciality': 'GENERAL', 'available_from': 0},
    ]
    equipment = [
        {'id': 'E1', 'type': 'BLOOD', 'available_from': 0},
        {'id': 'E2', 'type': 'URINE', 'available_from': 0},
    ]

    plan = planify_lab(samples, technicians, equipment)
    print(plan)
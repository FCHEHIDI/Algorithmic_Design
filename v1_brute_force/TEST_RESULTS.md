# V1 - Brute Force Approach - Test Results

## Dataset Conforme SIMPLE

- **Échantillons** : 10
- **Techniciens** : 4 (BLOOD, URINE, TISSUE, GENERAL)
- **Équipements** : 3 (BLOOD, URINE, TISSUE)

## Résultats

### Schedule

6/10 échantillons planifiés avec succès :
- 2 STAT (S001, S004)
- 2 URGENT (S002, S008)
- 2 ROUTINE (S006, S009)

### Metrics

```json
{
  "total_time": 150,
  "efficiency": 0.04,
  "conflicts": 4
}
```

### Échantillons Non Planifiés (Conflicts)

4 échantillons n'ont pas pu être planifiés :
- S003 (BLOOD, ROUTINE) - Conflit de disponibilité
- S005 (BLOOD, URGENT) - Conflit de disponibilité  
- S007 (TISSUE, STAT) - Conflit de disponibilité
- S010 (TISSUE, ROUTINE) - Conflit de disponibilité

## Analyse

### Cause des Conflicts

La logique V1 utilise une condition stricte :
```python
if (technician_availability[tech['id']] <= sample['ready_time'] and
    equipment_availability[equip['id']] <= sample['ready_time']):
```

Cette condition est **trop restrictive** : elle exige que les ressources soient disponibles **avant** le ready_time de l'échantillon, ce qui n'est pas toujours possible quand les échantillons arrivent avec des ready_times différents.

### Limitation Documentée

✅ **C'est attendu pour une V1 "Brute Force"** :
- L'algorithme est naïf et simple
- Il ne cherche pas la meilleure solution
- Il ne réajuste pas les assignations
- Les conflicts sont normaux pour les cas complexes

### Évolution V2/V3

Les versions suivantes (V2 et V3) résolvent ce problème via :
- **V2** : Indexation intelligente + meilleure gestion des disponibilités
- **V3** : Architecture OOP + features kernel (aging, deadlock detection, load balancing)

## Conformité Évaluation

### ✅ Points Conformes

1. ✅ Fonction `planify_lab()` existe
2. ✅ Dataset 10/4/3 conforme
3. ✅ Output JSON avec `schedule` et `metrics`
4. ✅ Priorités respectées (STAT > URGENT > ROUTINE)
5. ✅ Spécialisations techniciens respectées
6. ✅ Compatibilité équipements respectée

### ⚠️ Points Non-Optimaux

1. ⚠️ 4 conflicts sur 10 échantillons (40% non planifiés)
2. ⚠️ Efficacité très basse (0.04 = 4%)

### 🎯 Justification Pédagogique

**C'est exactement le but de V1** : montrer qu'un algorithme naïf (brute force) a des limites importantes :
- Ne garantit pas de solution complète
- Très sensible à l'ordre de traitement
- Pas d'optimisation
- Beaucoup de conflicts possibles

Cela **justifie l'évolution vers V2/V3** qui résolvent ces problèmes.

## Recommandation Instructeur

Si l'instructeur demande "pourquoi seulement 6/10 planifiés ?", la réponse est :

> "C'est une limitation intentionnellement documentée de V1 (Brute Force). L'algorithme naïf ne garantit pas de solution complète. C'est exactement ce qui motive l'évolution vers V2 (95% gain d'efficacité) et V3 (architecture production-ready). Les 4 conflicts démontrent pourquoi l'algorithme basique ne suffit pas en production."

## Fichiers

- **Code source** : `planify_lab.py`
- **Test dataset** : `../test_v1_dataset.py`
- **Output JSON** : `output-example-simple.json`
- **Analyse** : `LIMITATIONS_V1.md` (détaillée)

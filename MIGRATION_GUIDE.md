# 📚 Guide de Migration des Versions

## 🎯 Objectif

Ce document explique comment naviguer entre les différentes versions de l'algorithme et comprendre l'évolution du projet.

---

## 📂 Structure Organisée

Le projet est maintenant organisé en **4 dossiers distincts** pour une meilleure clarté :

```
Algorithmic_Design/
├── v1_brute_force/          ← Version 1 (Baseline)
├── v2_indexed/              ← Version 2 (Optimisée)
├── v3_optimized/            ← Version 3 (Production)
├── c_native_kernel/         ← C Native (Medical RT)
└── BruteForceApproach/      ← Archive (legacy)
```

### 🗂️ Ancien vs Nouveau

| Ancien (legacy) | Nouveau | Description |
|-----------------|---------|-------------|
| `BruteForceApproach/planify_lab.py` | `v1_brute_force/planify_lab.py` | V1 isolée |
| `BruteForceApproach/planify_next_lab.py` | `v2_indexed/planify_next_lab.py` | V2 isolée |
| `BruteForceApproach/LIMITATIONS_V1.md` | `v1_brute_force/LIMITATIONS_V1.md` | Docs V1 |
| `BruteForceApproach/LIMITATIONS_V2.md` | `v2_indexed/LIMITATIONS_V2.md` | Docs V2 |
| `BruteForceApproach/Docs/` | `v1_brute_force/docs/` | Docs détaillées V1 |

---

## 🚀 Parcours Recommandé

### 📍 Pour Apprendre (Débutants)

**Ordre suggéré** :

1. **V1 Brute Force** → Comprendre le problème
   ```powershell
   cd v1_brute_force
   python planify_lab.py
   # Lire LIMITATIONS_V1.md
   ```

2. **V2 Indexed** → Comprendre l'optimisation
   ```powershell
   cd ..\v2_indexed
   python planify_next_lab.py
   # Lire LIMITATIONS_V2.md
   # Comparer avec V1
   ```

3. **V3 OOP** → Comprendre l'architecture
   ```powershell
   cd ..\v3_optimized
   python main.py
   # Explorer lab_planner/ (4 couches)
   ```

4. **C Native** (Optionnel) → Comprendre la performance ultime
   ```powershell
   cd ..\c_native_kernel
   # Lire PERFORMANCE_COMPARISON.md
   # Lire DEPLOYMENT_GUIDE.md
   ```

### 📍 Pour Développer (Production)

**Utilisez directement V3** :

```powershell
cd v3_optimized

# Tests locaux
python main.py

# Docker
docker build -t lab-planner:latest .
docker run --rm lab-planner:latest
```

---

## 🔄 Migration de Code

### Migrer de V1 vers V2

#### V1 (Brute Force)
```python
from planify_lab import planify_lab

result = planify_lab(samples, technicians, equipment)
```

#### V2 (Indexed)
```python
from planify_next_lab import planify_next_lab

result = planify_next_lab(samples, technicians, equipment)
# API identique ! Aucun changement côté appelant
```

**Changements** : Aucun ! L'API est la même, seul l'algorithme interne change.

---

### Migrer de V2 vers V3

#### V2 (Procédural)
```python
from planify_next_lab import planify_next_lab

result = planify_next_lab(samples, technicians, equipment)
schedule = result['schedule']
metrics = result['metrics']
```

#### V3 (OOP)
```python
from lab_planner import LabPlanner
from lab_planner.scheduling.priority_scheduler import PriorityScheduler

# Option 1 : Avec stratégie par défaut
planner = LabPlanner()

# Option 2 : Avec stratégie personnalisée
planner = LabPlanner(strategy=PriorityScheduler(concurrent=True))

# Planification
result = planner.planify(samples, technicians, equipment)
schedule = result['schedule']
metrics = result['metrics']
```

**Changements** :
- Import change : `planify_next_lab` → `LabPlanner`
- API change : fonction → méthode de classe
- Nouvelle feature : choix de stratégie (Priority/Greedy)
- Nouvelle feature : mode concurrent

---

## 📊 Comparaison des APIs

### Structure de Retour (Identique)

Toutes les versions retournent le même format :

```python
{
    'schedule': [
        {
            'sample_id': 'S001',
            'technician_id': 'T001',
            'equipment_id': 'E001',
            'start_time': 0,
            'end_time': 30,
            'priority': 'STAT'
        },
        # ...
    ],
    'metrics': {
        'total_time': 150,
        'efficiency': 0.67,
        'conflicts': 0
    }
}
```

### Différences Clés

| Aspect | V1/V2 | V3 |
|--------|-------|-----|
| **Type** | Fonction | Classe |
| **Import** | `from module import function` | `from package import Class` |
| **Appel** | `function(args)` | `Class().method(args)` |
| **Stratégie** | Fixe (Priority) | Configurable (Priority/Greedy) |
| **Concurrence** | Non | Oui (optionnel) |
| **Configuration** | Hardcodée | Externalisable (YAML) |

---

## 🎓 Exercices Pédagogiques

### Exercice 1 : Benchmark Comparatif

```python
import time
import sys
sys.path.append('../v1_brute_force')
sys.path.append('../v2_indexed')

from planify_lab import planify_lab
from planify_next_lab import planify_next_lab

# Dataset de test
samples = [...]  # 100 échantillons
technicians = [...]
equipment = [...]

# Benchmark V1
start = time.perf_counter()
result_v1 = planify_lab(samples, technicians, equipment)
time_v1 = time.perf_counter() - start

# Benchmark V2
start = time.perf_counter()
result_v2 = planify_next_lab(samples, technicians, equipment)
time_v2 = time.perf_counter() - start

# Résultats
print(f"V1: {time_v1*1000:.2f}ms")
print(f"V2: {time_v2*1000:.2f}ms")
print(f"Speedup: {time_v1/time_v2:.1f}x")
```

### Exercice 2 : Comparaison Stratégies V3

```python
from lab_planner import LabPlanner
from lab_planner.scheduling.priority_scheduler import PriorityScheduler
from lab_planner.scheduling.greedy_scheduler import GreedyScheduler

# Test Priority
planner_priority = LabPlanner(strategy=PriorityScheduler())
result_priority = planner_priority.planify(samples, technicians, equipment)

# Test Greedy
planner_greedy = LabPlanner(strategy=GreedyScheduler())
result_greedy = planner_greedy.planify(samples, technicians, equipment)

# Comparer
print(f"Priority - Temps total: {result_priority['metrics']['total_time']}")
print(f"Greedy   - Temps total: {result_greedy['metrics']['total_time']}")
```

---

## 🐛 Troubleshooting

### Problème : Import Error

**Erreur** :
```
ModuleNotFoundError: No module named 'planify_lab'
```

**Solution** :
```powershell
# Vérifier que vous êtes dans le bon dossier
pwd  # Doit afficher .../v1_brute_force ou .../v2_indexed

# Si besoin, ajouter au PYTHONPATH
$env:PYTHONPATH += ";$(pwd)"
```

---

### Problème : Different Results

**Question** : Pourquoi V1, V2 et V3 donnent des résultats légèrement différents ?

**Réponse** :
- **V1** : Assigne au premier technicien disponible (ordre d'itération)
- **V2** : Assigne au technicien le moins chargé (load balancing)
- **V3 Priority** : Identique V2 + features kernel (aging, deadlock)
- **V3 Greedy** : Minimise temps total (algorithme différent)

Toutes les versions sont **correctes**, elles ont juste des **objectifs d'optimisation différents**.

---

### Problème : Performance V3 < V2

**Question** : V3 semble parfois plus lente que V2 sur petits datasets ?

**Réponse** : Normal ! V3 a un **overhead** (classes, validation) qui ne vaut la peine que pour :
- Datasets > 50 échantillons
- Mode concurrent activé
- Besoin de maintenabilité/extensibilité

**Solution** :
```python
# Pour petits datasets
planner = LabPlanner(strategy=PriorityScheduler(concurrent=False))
```

---

## 📝 Checklist Migration Production

### De V2 vers V3

- [ ] **Tests** : Exécuter tests V3 (`python -m pytest`)
- [ ] **Benchmark** : Comparer performances sur vos données réelles
- [ ] **Docker** : Tester build et déploiement
- [ ] **Config** : Externaliser la configuration (YAML)
- [ ] **Logs** : Vérifier les logs structurés
- [ ] **Monitoring** : Intégrer métriques (Prometheus)
- [ ] **Documentation** : Mettre à jour docs internes
- [ ] **Formation** : Former l'équipe à l'architecture OOP

---

## 🔮 Feuille de Route

### Court Terme (Maintenant)

- ✅ V1, V2, V3 isolées dans dossiers séparés
- ✅ README individuels pour chaque version
- ✅ C Native avec guide déploiement
- ⏳ Docker V3 avec volumes persistants
- ⏳ Git : Push branche `feature/optimized-modular-approach`

### Moyen Terme (1-2 semaines)

- [ ] API REST (FastAPI) pour V3
- [ ] Base de données (SQLAlchemy + SQLite/PostgreSQL)
- [ ] Tests end-to-end complets
- [ ] CI/CD (GitHub Actions)
- [ ] Monitoring (Prometheus + Grafana)

### Long Terme (1-3 mois)

- [ ] Contraintes INTERMEDIATE (pauses, maintenance)
- [ ] Machine Learning (prédiction temps)
- [ ] Interface web (React/Vue.js)
- [ ] Multi-tenancy (plusieurs laboratoires)
- [ ] Certification médicale (IEC 62304)

---

## 🙏 Aide et Support

### Documentation Complète

- **V1** : Lire `v1_brute_force/README.md`
- **V2** : Lire `v2_indexed/README.md`
- **V3** : Lire `v3_optimized/README.md`
- **C Native** : Lire `c_native_kernel/DEPLOYMENT_GUIDE.md`

### Guides Spécifiques

- **Limitations V1** : `v1_brute_force/LIMITATIONS_V1.md`
- **Limitations V2** : `v2_indexed/LIMITATIONS_V2.md`
- **Comparaison Python vs C** : `c_native_kernel/PERFORMANCE_COMPARISON.md`
- **Git Workflow** : `GUIDE_PUSH_GIT.md`

---

**Dernière mise à jour** : 26 novembre 2025  
**Version** : 1.0.0

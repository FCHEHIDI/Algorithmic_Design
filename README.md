# 🧪 Lab Planner - Évolution d'Algorithme (V1 → V2 → V3 → C)

> **Contexte Professionnel** : Projet d'évaluation stage - Démonstration de l'évolution d'un algorithme de planification depuis une implémentation naïve jusqu'à une solution de production avec kernel real-time.

## 📋 Vue d'Ensemble

Système de planification d'analyses de laboratoire médical respectant :
- ✅ **Priorités médicales** (STAT > URGENT > ROUTINE)
- ✅ **Compatibilités** technicien-échantillon-équipement
- ✅ **Disponibilités** des ressources en temps réel
- ✅ **Optimisation** du temps total et charge de travail

---

## 🗂️ Structure du Projet

```
Algorithmic_Design/
│
├── 📁 v1_brute_force/                    # Version 1 - Brute Force O(S×T×E)
│   ├── planify_lab.py                    # Fonction SIMPLE: planify_lab()
│   ├── test_v1_dataset.py                # Tests dataset 10/4/3
│   ├── output-example-simple.json        # Exemple output (6/10 planifiés)
│   ├── TEST_RESULTS.md                   # Documentation limitations
│   ├── LIMITATIONS_V1.md                 # Analyse complexité
│   └── README.md                         # Guide d'utilisation V1
│
├── 📁 v2_indexed/                        # Version 2 - Indexed O(S+T+E)
│   ├── planify_next_lab.py               # Optimisation indexation
│   ├── LIMITATIONS_V2.md                 # Analyse gains performance
│   └── README.md                         # Guide d'utilisation V2
│
├── 📁 v3_optimized/                      # Version 3 - OOP + Kernel Features
│   ├── lab_planner/                      # Package modulaire (4 couches)
│   │   ├── domain/                       # Modèles métier (Sample, Technician, etc.)
│   │   ├── resources/                    # Gestion pools ressources
│   │   ├── scheduling/                   # Stratégies (Priority, Kernel)
│   │   └── orchestration/                # Façade + validation
│   ├── planify_lab_wrapper.py            # Fonction INTERMEDIATE: planifyLab()
│   ├── tests/                            # Tests conformité INTERMEDIATE
│   │   └── test_intermediate_conformity.py  # 5 tests (20/8/5 dataset)
│   ├── test_kernel_features_clean.py     # Tests kernel (preemption, aging, etc.)
│   ├── output/
│   │   ├── output-example-intermediate.json  # Exemple output (20/20 planifiés)
│   │   └── test-results.txt              # Résultats pytest (5/5 passed)
│   ├── docs/
│   │   ├── ARCHITECTURE_DETAILED.md      # Architecture OOP complète
│   │   └── KERNEL_FEATURES_GUIDE.md      # Guide features kernel
│   ├── Dockerfile                        # Multi-stage build
│   ├── docker-compose.yml                # Orchestration services
│   ├── LIMITATIONS_V3.md                 # Analyse extensions futures
│   └── README.md                         # Guide d'utilisation V3
│
├── 📁 c_native_kernel/                   # Version C - Real-Time Medical
│   ├── kernel_scheduler.c                # Implémentation <100µs
│   ├── kernel_scheduler.h                # Header structures
│   ├── Makefile                          # Build production
│   ├── PERFORMANCE_COMPARISON.md         # Python vs C (100x faster)
│   └── DEPLOYMENT_GUIDE.md               # Guide déploiement CentOS RT
│
├── CONFORMITY_CHECKLIST.md               # Checklist évaluation (SIMPLE + INTERMEDIATE)
├── MIGRATION_GUIDE.md                    # Guide navigation versions
└── .gitignore                            # Ignore __pycache__, logs, outputs

```

---

## 🚀 Quick Start

### 🔧 Prérequis

```bash
# Python 3.11+
python --version

# Git
git --version
```

### 📥 Installation

```bash
# Cloner le repository
git clone https://github.com/FCHEHIDI/Algorithmic_Design.git
cd Algorithmic_Design

# Installer dépendances (pour V3)
pip install pytest pytest-cov
```

---

## 🎯 Exécution par Version

### 📕 V1 - Brute Force (Niveau SIMPLE)

**Dataset** : 10 samples, 4 technicians, 3 equipment

```bash
cd v1_brute_force

# Exécuter avec dataset test
python test_v1_dataset.py

# Output: 6/10 samples planifiés (4 conflits attendus)
# Voir: output-example-simple.json
```

**Résultats attendus** :
- ⚠️ 6/10 échantillons planifiés (40% conflits)
- 📊 Complexité O(S×T×E) = 800 itérations
- 📄 Limitations documentées dans `TEST_RESULTS.md`

➡️ [Documentation V1 complète](v1_brute_force/README.md)

---

### 📗 V2 - Indexed (Optimisation)

**Dataset** : 20 samples, 8 technicians, 5 equipment

```bash
cd v2_indexed

# Exécuter avec dataset
python planify_next_lab.py

# Gain: 95.8% réduction itérations (800 → 33)
```

**Résultats attendus** :
- ✅ ~95% échantillons planifiés
- 📊 Complexité O(S+T+E) = 33 itérations
- 🚀 Gain performance 95.8%

➡️ [Documentation V2 complète](v2_indexed/README.md)

---

### 📘 V3 - OOP + Kernel Features (Niveau INTERMEDIATE)

**Dataset** : 20 samples, 8 technicians, 5 equipment

#### Option 1 : Python Direct

```bash
cd v3_optimized

# Exécuter wrapper INTERMEDIATE
python planify_lab_wrapper.py

# Output: output-example-intermediate.json
# 20/20 échantillons planifiés, 0 conflits
```

#### Option 2 : Docker (Recommandé)

```bash
cd v3_optimized

# Build et run
docker-compose up --build

# Logs disponibles dans logs/
```

#### Tests

```bash
cd v3_optimized

# Tests conformité INTERMEDIATE (5 tests)
pytest tests/test_intermediate_conformity.py -v

# Tests kernel features (4 tests)
python test_kernel_features_clean.py
```

**Résultats attendus** :
- ✅ 20/20 échantillons planifiés (100%)
- ✅ 5/5 tests INTERMEDIATE passent
- ✅ Format JSON conforme (laboratory, schedule, metrics, metadata)
- ✅ Kernel features : preemption, aging, load balancing, deadlock detection

➡️ [Documentation V3 complète](v3_optimized/README.md)  
➡️ [Architecture détaillée](v3_optimized/docs/ARCHITECTURE_DETAILED.md)  
➡️ [Guide kernel features](v3_optimized/docs/KERNEL_FEATURES_GUIDE.md)

---

### 🔥 C Native - Real-Time Medical

**Prérequis** : GCC, CentOS RT kernel

```bash
cd c_native_kernel

# Compiler
make clean && make

# Exécuter
./scheduler_demo

# Performance: <100µs (vs 8-15ms Python = 100x faster)
```

➡️ [Guide déploiement](c_native_kernel/DEPLOYMENT_GUIDE.md)  
➡️ [Comparaison performance](c_native_kernel/PERFORMANCE_COMPARISON.md)

---

## 📊 Comparaison des Versions

| Critère | V1 Brute Force | V2 Indexed | V3 OOP | C Native |
|---------|----------------|------------|--------|----------|
| **Complexité** | O(S×T×E) | O(S+T+E) | O(S+T+E) | O(S+T+E) |
| **Itérations** (20/8/5) | 800 | 33 | 33 | 33 |
| **Temps exécution** | ~15ms | ~8ms | ~5ms | <0.1ms |
| **Architecture** | Monolithique | Procédurale | OOP (4 layers) | Kernel RT |
| **Concurrence** | ❌ | ❌ | ✅ ThreadPool | ✅ Native threads |
| **Échantillons planifiés** | 60% (6/10) | 95% | 100% (20/20) | 100% |
| **Features avancées** | ❌ | ❌ | ✅ Preemption, Aging, Load Balance | ✅ Toutes |
| **Production ready** | ❌ | ⚠️ Partiel | ✅ Oui | ✅ Medical grade |

---

## 🎓 Objectifs Pédagogiques

### 🔴 V1 → V2 : Comprendre l'Impact des Structures de Données

**Problème** : Boucles imbriquées créent explosion combinatoire  
**Solution** : Hash tables (dict) transforment O(n²) en O(1)  
**Gain** : 95.8% réduction itérations

### 🟢 V2 → V3 : Comprendre l'Importance de l'Architecture

**Problème** : Code procédural difficile à maintenir, tester, étendre  
**Solution** : OOP avec patterns (Strategy, Facade), SOLID principles  
**Gain** : Maintenabilité, testabilité, extensibilité

### 🔵 V3 → C : Comprendre les Contraintes Real-Time

**Problème** : Python garbage collector imprévisible pour systèmes critiques  
**Solution** : C natif avec gestion mémoire manuelle  
**Gain** : Déterminisme temporel (<100µs garanti)

---

## 📚 Documentation

### Guides d'Utilisation
- [Guide V1 (SIMPLE)](v1_brute_force/README.md)
- [Guide V2 (Optimisé)](v2_indexed/README.md)
- [Guide V3 (INTERMEDIATE)](v3_optimized/README.md)

### Analyses Techniques
- [Limitations V1](v1_brute_force/LIMITATIONS_V1.md)
- [Limitations V2](v2_indexed/LIMITATIONS_V2.md)
- [Limitations V3](v3_optimized/LIMITATIONS_V3.md)
- [Architecture OOP Détaillée](v3_optimized/docs/ARCHITECTURE_DETAILED.md)
- [Kernel Features Guide](v3_optimized/docs/KERNEL_FEATURES_GUIDE.md)

### Évaluation & Conformité
- [Conformity Checklist](CONFORMITY_CHECKLIST.md) - SIMPLE + INTERMEDIATE
- [Migration Guide](MIGRATION_GUIDE.md) - Navigation entre versions

---

## 🧪 Tests

### V1 - SIMPLE
```bash
cd v1_brute_force
python test_v1_dataset.py
# Résultat: 6/10 planifiés (limitations documentées)
```

### V3 - INTERMEDIATE
```bash
cd v3_optimized

# Tests conformité (5 tests)
pytest tests/test_intermediate_conformity.py -v
# PASSED: planifyLab exists, 20/8/5 dataset, camelCase, HH:MM format, zero conflicts

# Tests kernel features (4 tests)
python test_kernel_features_clean.py
# PASSED: preemption, aging, load balancing, features combinées
```

---

## 🌿 Branches Git

| Branche | Contenu | Status |
|---------|---------|--------|
| `main` | Documentation + liens | ✅ Stable |
| `feature/brute-force-approach` | V1 brute force | ✅ Pushed |
| `feature/optimized-modular-approach` | V2 + V3 + C native | 🚧 Ready to push |

---

## 📝 Résultats Conformité

### ✅ Niveau SIMPLE (V1)
- ✅ Fonction `planify_lab()` conforme
- ✅ Dataset 10/4/3 testé
- ✅ Output JSON structure `{schedule, metrics}`
- ✅ Limitations documentées (6/10 planifiés)

### ✅ Niveau INTERMEDIATE (V3)
- ✅ Fonction `planifyLab()` wrapper créé
- ✅ Dataset 20/8/5 testé (100% planifiés)
- ✅ Output JSON format `{laboratory, schedule, metrics, metadata}`
- ✅ Champs INTERMEDIATE : efficiency, lunchBreak, averageWaitTime, technicianUtilization
- ✅ 5/5 tests conformité passent
- ✅ Format camelCase respecté
- ✅ Temps format HH:MM respecté

---

## 👤 Auteur

**Fares Chehidi**  
Email: fareschehidi7@gmail.com  
GitHub: [@FCHEHIDI](https://github.com/FCHEHIDI)

**Contexte** : Projet d'évaluation professionnelle - Stage "incubation"

---

## 📄 Licence

Projet académique - Usage éducatif uniquement

---

## 🔗 Liens Utiles

- [Repository GitHub](https://github.com/FCHEHIDI/Algorithmic_Design)
- [Conformity Checklist](CONFORMITY_CHECKLIST.md)
- [Architecture V3 Détaillée](v3_optimized/docs/ARCHITECTURE_DETAILED.md)
- [Kernel Features Guide](v3_optimized/docs/KERNEL_FEATURES_GUIDE.md)
- [Deployment C Native](c_native_kernel/DEPLOYMENT_GUIDE.md)

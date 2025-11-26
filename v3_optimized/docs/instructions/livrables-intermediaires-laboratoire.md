# 📦 LIVRABLES INTERMÉDIAIRES - LABORATOIRE

## 🎯 Vue d'Ensemble

**Objectif** : Démontrer capacité algorithme + architecture sans sur-complexité.


## 📋 Fichiers Obligatoires

### **1. 📖 [README.md](http://README.md)**

**Contenu minimum requis** :

```markdown
# Laboratoire - Système de Planification

## Description
[Votre explication du problème résolu]

## Installation
[Instructions pour faire tourner votre code]

## Utilisation  
[Commandes pour exécuter avec vos données]

## Évolution depuis version SIMPLE
[Si applicable : quelles extensions avez-vous ajoutées]
```

### **2. 💻 Code Source Fonctionnel**

**Fonction principale obligatoire** :

```
planifyLab(inputData) → { schedule, metrics }
```

**Critères techniques** :

* ✅ **Executable** : code qui tourne sans erreur
* ✅ **Complet** : traite les 20 échantillons fournis
* ✅ **Correct** : respecte priorités + contraintes
* ✅ **Lisible** : nommage clair + commentaires utiles
* ✅ **Évolutif** : compatible structure SIMPLE

### **3. 🧪 Tests (Minimum)**

**Tests obligatoires** :

* ✅ **Happy path** : cas nominal qui fonctionne
* ✅ **Priorités** : STAT > URGENT > ROUTINE respecté
* ✅ **Spécialisations** : technicien compatible assigné
* ✅ **Contraintes** : au moins pauses déjeuner testées
* ✅ **Efficacité** : coefficient technicien appliqué

**Fichier test minimum** :

```
test-scheduler.*
├── test_basic_scheduling()
├── test_priority_respect()  
├── test_specialization_matching()
├── test_lunch_breaks()
└── test_efficiency_coefficients()
```

### **4. 📊 Exemple Sortie**

**output-example.json** avec structure CORRIGÉE :

```json
{
  "laboratory": {
    "date": "2025-03-15",
    "processingDate": "2025-03-15",
    "totalSamples": 20,
    "algorithmVersion": "v1.0"
  },
  "schedule": [
    {
      "sampleId": "S003",
      "priority": "STAT", 
      "technicianId": "TECH001",
      "equipmentId": "EQ001",
      "startTime": "09:20",
      "endTime": "09:53",
      "duration": 33,
      "analysisType": "Numération complète",
      
      // EXTENSIONS INTERMÉDIAIRES (vs SIMPLE)
      "efficiency": 1.2,
      "lunchBreak": null,
      "cleaningRequired": false
    }
    // ... autres analyses ...
  ],
  "metrics": {
    // BASE (identique SIMPLE)
    "totalTime": 420,
    "efficiency": 82.0,
    "conflicts": 0,
    
    // EXTENSIONS INTERMÉDIAIRES
    "averageWaitTime": {
      "STAT": 8,
      "URGENT": 45, 
      "ROUTINE": 120
    },
    "technicianUtilization": 78.5,
    "priorityRespectRate": 100,
    "parallelAnalyses": 6,
    "lunchInterruptions": 1
  },
  "metadata": {
    // EXTENSIONS INTERMÉDIAIRES
    "lunchBreaks": [
      {
        "technicianId": "TECH001",
        "planned": "12:00-13:00",
        "actual": "12:15-13:15",
        "reason": "adjusted for optimization"
      }
    ],
    "constraintsApplied": [
      "priority_management",
      "specialization_matching", 
      "lunch_breaks",
      "equipment_compatibility",
      "maintenance_avoidance", 
      "cleaning_delays",
      "efficiency_coefficients",
      "parallelism_optimization"
    ]
  }
}
```


---

## 🎯 Format Attendu vs Versions

### **📊 Comparatif Structures**

| **Champ** | 🟢 **SIMPLE** | 🔵 **INTERMÉDIAIRE** | 🔴 **STANDARD** |
|----|----|----|----|
| **sampleId** | ✅ Identique | ✅ Identique | ✅ Identique |
| **technicianId** | ✅ Identique | ✅ Identique | ✅ Identique |
| **startTime** | ✅ Identique | ✅ Identique | ✅ Identique |
| **endTime** | ✅ Identique | ✅ Identique | ✅ Identique |
| **duration** | ✅ Identique | ✅ Identique | ✅ Identique |
| **efficiency** | ❌ Absent | ✅ **AJOUTÉ** | ✅ Hérité |
| **lunchBreak** | ❌ Absent | ✅ **AJOUTÉ** | ✅ Hérité |
| **metadata** | ❌ Absent | ✅ **AJOUTÉ** | ✅ Étendu |

### **🔄 Évolutivité Garantie**

```json
// CODE SIMPLE peut évoluer vers INTERMÉDIAIRE en ajoutant :
{
  // BASE SIMPLE (garde tout)
  "sampleId": "S001",
  "technicianId": "TECH001", 
  "startTime": "09:00",
  "endTime": "09:30",
  "duration": 30,
  
  // EXTENSIONS INTERMÉDIAIRES (ajoute)
  "efficiency": 1.1,           // + Nouveau
  "lunchBreak": "12:00-13:00", // + Nouveau
  "cleaningTime": 10           // + Nouveau
}
```


---

## 🎁 Bonus Possibles (+15% max)

### **🧪 Tests Complets (+5%)**

* **Tests unitaires** par classe/module
* **Tests d'intégration** scénarios complexes
* **Couverture** >70% du code critique
* **Mocking** pour isolation tests
* **Tests d'évolutivité** : Simple → Intermédiaire

### **🛡️ Gestion Erreurs Avancée (+5%)**

* **Validation inputs** robuste
* **Exceptions** métier explicites
* **Récupération gracieuse** d'erreurs
* **Messages utilisateur** informatifs
* **Compatibilité** formats SIMPLE/INTERMÉDIAIRE

### **🚀 Optimisations Créatives (+5%)**

* **Algorithmes innovants** (heuristiques, algorithmes génétiques)
* **Performance** exceptionnelle
* **Fonctionnalités bonus** (export formats multiples)
* **Interface utilisateur** (CLI élégante)
* **Migration automatique** SIMPLE → INTERMÉDIAIRE


---

## 🎯 Critères d'Évaluation

### **🏗️ Architecture (30%)**

* **POO encouragé** : classes logiques, encapsulation
* **Structure cohérente** : séparation responsabilités
* **Évolutivité** : extensions sans refonte
* **Compatibilité** : structure alignée sur SIMPLE

### **⚙️ Algorithme (25%)**

* **Correctness** : priorités + contraintes respectées
* **Efficacité** : optimisations intelligentes
* **Robustesse** : gestion cas complexes
* **Parallélisme** : utilisation multi-techniciens

### **💻 Qualité Code (20%)**

* **Lisibilité** : nommage, organisation
* **Maintenabilité** : commentaires, modularité
* **Standards** : conventions langage
* **Réutilisabilité** : composants indépendants

### **🎯 Fonctionnel (15%)**

* **Complétude** : toutes contraintes implémentées
* **Précision** : métriques exactes
* **Performance** : temps exécution raisonnable
* **Output** : format JSON conforme

### **📚 Documentation (10%)**

* **README** : instructions claires
* **Code** : commentaires pertinents
* **Tests** : documentation cas couverts
* **Évolution** : changements vs SIMPLE explicités


---

## 🚀 Conseils Finaux

### **⏱️ Gestion Temps (7h)**

**Répartition suggérée** :

* **1h** : Lecture + compréhension (focus sur évolutivité)
* **1h30** : Architecture + conception
* **3h30** : Développement + tests
* **1h** : Documentation + validation

### **🎯 Priorités**

**Phase 1 (Critical)** :


1. Planning fonctionnel basique (compatible SIMPLE)
2. Respect priorités STAT/URGENT/ROUTINE
3. Spécialisations techniciens
4. Structure JSON cohérente

**Phase 2 (Important)** : 5. Extensions intermédiaires : efficiency, lunchBreak


6. Métriques correctes + nouvelles métriques
7. Tests minimum
8. Metadata avancée

**Phase 3 (Bonus)** : 9. Optimisations avancées


10. Gestion erreurs
11. Documentation détaillée
12. Tests évolutivité

### **✅ Checklist Finale**

**Avant soumission** :

- [ ] Code s'exécute sans erreur
- [ ] Planning respecte priorités
- [ ] 20 échantillons traités
- [ ] 8+ métriques calculées (base + extensions)
- [ ] README avec instructions
- [ ] Au moins 4-5 tests
- [ ] Exemple sortie JSON fourni (format correct)
- [ ] Archive ZIP/Git propre
- [ ] **CRITIQUE** : Structure compatible SIMPLE
- [ ] **CRITIQUE** : Évolutivité vers STANDARD possible

### **🔄 Test d'Évolutivité**

**Validation obligatoire** :

```bash
# Si vous aviez commencé en SIMPLE, votre code peut-il :
1. Ajouter champ "efficiency" sans refonte ? ✅
2. Ajouter "lunchBreak" sans casser l'existant ? ✅  
3. Étendre "metrics" avec nouvelles métriques ? ✅
4. Garder même format "schedule[]" ? ✅
5. Réutiliser même algorithme de base ? ✅
```


---

## 📤 Format Livraison

### **📦 Repository GitHub**

### **⏰ Délai**

**Temps maximum** : 7 heures après réception énoncé **Tolérance** : +1h (pénalité -5%) **Limite absolue** : +24h (exclusion)


---

## 🔗 Compatibilité Entre Versions

### **✅ Ce qui DOIT rester identique avec SIMPLE**

* Noms de champs : sampleId, technicianId, startTime, endTime
* Structure schedule\[\] : même format de base
* Métriques de base : totalTime, efficiency, conflicts
* Types de données : JSON, camelCase

### **✅ Ce qui peut être ÉTENDU pour INTERMÉDIAIRE**

* Nouveaux champs optionnels dans schedule
* Nouvelles métriques dans metrics
* Section metadata additionnelle
* Contraintes avancées

### **✅ Ce qui sera HÉRITÉ par STANDARD**

* Toute la structure INTERMÉDIAIRE
* Extensions supplémentaires uniquement
* Compatibilité ascendante garantie


---

**🎯 Tout est clair ? Vous avez maintenant tous les éléments pour réussir ce test technique intermédiaire avec garantie d'évolutivité ! Bon développement ! 🚀**
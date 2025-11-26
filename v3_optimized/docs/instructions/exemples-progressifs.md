# 🎮 EXEMPLES PROGRESSIFS

## 🎯 Approche Pédagogique

**3 scénarios de complexité croissante** pour comprendre l'algorithme étape par étape. 

Chaque exemple illustre des contraintes spécifiques et leurs solutions.


---

## 🟢 EXEMPLE 1 : Cas Simple (2 échantillons)

### **📊 Données d'Entrée**

```json
{
  "samples": [
    {
      "id": "S001",
      "priority": "ROUTINE", 
      "type": "CHEMISTRY",
      "analysisType": "Bilan lipidique",
      "analysisTime": 30,
      "arrivalTime": "09:00"
    },
    {
      "id": "S002", 
      "priority": "URGENT",
      "type": "BLOOD",
      "analysisType": "Numération complète",
      "analysisTime": 45,
      "arrivalTime": "09:15"
    }
  ],
  "technicians": [
    {
      "id": "TECH001",
      "specialty": ["BLOOD", "CHEMISTRY"],
      "efficiency": 1.0,
      "startTime": "08:00",
      "endTime": "17:00",
      "lunchBreak": "12:00-13:00"
    }
  ],
  "equipment": [
    {
      "id": "EQ001", 
      "type": "BLOOD",
      "capacity": 1,
      "cleaningTime": 10
    },
    {
      "id": "EQ002",
      "type": "CHEMISTRY", 
      "capacity": 1,
      "cleaningTime": 15
    }
  ]
}
```

### **🧠 Raisonnement Algorithme**

**ÉTAPE 1 : Triage par priorité**

```
Liste originale :
- S001 (ROUTINE, 09:00)
- S002 (URGENT, 09:15)

Après tri : 
- S002 (URGENT) ← traité en premier
- S001 (ROUTINE)
```

**ÉTAPE 2 : Planification S002 (URGENT)**

```
Analyse : S002 - BLOOD, 45min

1. Technicien compatible : TECH001 ✅ (spécialité BLOOD)
2. Équipement requis : EQ001 (BLOOD) ✅  
3. Premier créneau libre : 09:15 (après arrivée)
4. Durée avec efficacité : 45min / 1.0 = 45min

5. Planning : 09:15-10:00
```

**ÉTAPE 3 : Planification S001 (ROUTINE)**

```
Analyse : S001 - CHEMISTRY, 30min  
1. Technicien compatible : TECH001 ✅ (spécialité CHEMISTRY)
2. Équipement requis : EQ002 (CHEMISTRY) ✅
3. Premier créneau libre : 10:00 (après S002)
4. Durée avec efficacité : 30min / 1.0 = 30min

5. Planning : 10:00-10:30
```

### **📋 Résultat Final**

```json
{
  "schedule": [
    {
      "sampleId": "S002",
      "priority": "URGENT", 
      "technicianId": "TECH001",
      "equipmentId": "EQ001",
      "startTime": "09:15",
      "endTime": "10:00", 
      "duration": 45,
      "analysisType": "Numération complète",
      "efficiency": 1.0
    },
    {
      "sampleId": "S001",
      "priority": "ROUTINE",
      "technicianId": "TECH001", 
      "equipmentId": "EQ002",
      "startTime": "10:00", 
      "endTime": "10:30",
      "duration": 30,
      "analysisType": "Bilan lipidique",
      "efficiency": 1.0
    }
  ],
  "metrics": {
    "totalTime": 75,
    "efficiency": 85.0,
    "conflicts": 0,
    "averageWaitTime": 22.5,
    "technicianUtilization": 41.7,
    "priorityRespectRate": 100,
    "parallelEfficiency": 0
  }
}
```

### **📖 Leçons Apprises**

* ✅ **Priorité respectée** : URGENT avant ROUTINE
* ✅ **Spécialisations** : TECH001 compatible avec les 2 types
* ✅ **Séquentiel** : 1 seul technicien, analyses l'une après l'autre
* 📊 **Pas de parallélisme** possible (même technicien)


---

## 🟡 EXEMPLE 2 : Priorité STAT (3 échantillons)

### **📊 Données d'Entrée**

```json
{
  "samples": [
    {
      "id": "S001", 
      "priority": "ROUTINE",
      "type": "CHEMISTRY", 
      "analysisTime": 30,
      "arrivalTime": "09:00"
    },
    {
      "id": "S002",
      "priority": "URGENT", 
      "type": "BLOOD",
      "analysisTime": 45, 
      "arrivalTime": "09:05"
    },
    {
      "id": "S003",
      "priority": "STAT",
      "type": "CHEMISTRY",
      "analysisTime": 20,
      "arrivalTime": "09:20" 
    }
  ],
  "technicians": [
    {
      "id": "TECH001",
      "specialty": ["BLOOD", "CHEMISTRY"], 
      "efficiency": 1.1
    },
    {
      "id": "TECH002",
      "specialty": ["CHEMISTRY", "IMMUNOLOGY"],
      "efficiency": 1.0
    }
  ]
}
```

### **🧠 Raisonnement Algorithme**

**ÉTAPE 1 : Triage par priorité**

```
Liste originale (ordre d'arrivée) :
- S001 (ROUTINE, 09:00)
- S002 (URGENT, 09:05) 
- S003 (STAT, 09:20)

Après tri (priorité) :
- S003 (STAT) ← priorité absolue
- S002 (URGENT)
- S001 (ROUTINE)
```

**ÉTAPE 2 : Planification S003 (STAT)**

```
⚡ URGENCE VITALE - Traitement immédiat

Analyse : S003 - CHEMISTRY, 20min

1. Arrivée : 09:20

2. Techniciens compatibles CHEMISTRY : TECH001, TECH002

3. Premier disponible : TECH002 (pas encore occupé)
4. Équipement : EQ002 (CHEMISTRY)
5. Délai max STAT : 30min → OK (traitement immédiat)
6. Planning : 09:20-09:38 (20min / 1.0 = 20min, nettoyage inclus)
```

**ÉTAPE 3 : Planification S002 (URGENT)**

```
Analyse : S002 - BLOOD, 45min

1. Technicien compatible : TECH001 (spécialité BLOOD)  
2. Équipement requis : EQ001

3. Premier créneau libre : 09:05 (après arrivée, STAT pas encore arrivé)
4. Durée réelle : 45min / 1.1 = 41min

5. Planning : 09:05-09:46
```

**ÉTAPE 4 : Planification S001 (ROUTINE)**

```
Analyse : S001 - CHEMISTRY, 30min

1. Techniciens compatibles : TECH001 (occupé jusqu'à 09:46), TECH002 (libre après 09:38)
2. Choix optimal : TECH002 (disponible plus tôt)  
3. Premier créneau : 09:38 + 15min nettoyage = 09:53

4. Durée : 30min / 1.0 = 30min

5. Planning : 09:53-10:23
```

### **📋 Résultat Final**

```json
{
  "schedule": [
    {
      "sampleId": "S002",
      "priority": "URGENT",
      "technicianId": "TECH001", 
      "equipmentId": "EQ001",
      "startTime": "09:05",
      "endTime": "09:46",
      "duration": 41,
      "efficiency": 1.1
    },
    {
      "sampleId": "S003", 
      "priority": "STAT",
      "technicianId": "TECH002",
      "equipmentId": "EQ002",
      "startTime": "09:20", 
      "endTime": "09:38", 
      "duration": 20,
      "efficiency": 1.0
    },
    {
      "sampleId": "S001",
      "priority": "ROUTINE",
      "technicianId": "TECH002",
      "equipmentId": "EQ002",
      "startTime": "09:53",
      "endTime": "10:23", 
      "duration": 30,
      "efficiency": 1.0,
      "cleaningDelay": 15
    }
  ],
  "metrics": {
    "totalTime": 78,
    "efficiency": 88.5,
    "conflicts": 0,
    "statResponseTime": 18,
    "parallelAnalyses": 2,
    "priorityRespectRate": 100,
    "technicianUtilization": 65.4
  }
}
```

### **📖 Leçons Apprises**

* ⚡ **STAT priorité absolue** même arrivé en 3ème
* 🚀 **Parallélisme réussi** : S002 et S003 simultanés (09:20-09:38)
* 💪 **Efficacité technicien** prise en compte (TECH001 = 1.1)
* 🎯 **Optimisation ressources** : TECH002 pour S001 (plus rapide)


---

## 🔴 EXEMPLE 3 : Complexe avec Contraintes (4 échantillons)

### **📊 Données d'Entrée**

```json
{
  "samples": [
    {
      "id": "S001",
      "priority": "ROUTINE", 
      "type": "MICROBIOLOGY",
      "analysisTime": 60,
      "arrivalTime": "11:30"
    },
    {
      "id": "S002", 
      "priority": "URGENT",
      "type": "CHEMISTRY", 
      "analysisTime": 35,
      "arrivalTime": "11:45"
    },
    {
      "id": "S003",
      "priority": "STAT",
      "type": "BLOOD",
      "analysisTime": 40, 
      "arrivalTime": "12:15"
    },
    {
      "id": "S004",
      "priority": "URGENT",
      "type": "MICROBIOLOGY", 
      "analysisTime": 50,
      "arrivalTime": "12:30"
    }
  ],
  "technicians": [
    {
      "id": "TECH001", 
      "specialty": ["BLOOD", "CHEMISTRY"],
      "efficiency": 1.2,
      "lunchBreak": "12:00-13:00"
    },
    {
      "id": "TECH002",
      "specialty": ["MICROBIOLOGY", "IMMUNOLOGY"], 
      "efficiency": 1.0,
      "lunchBreak": "12:30-13:30" 
    }
  ]
}
```

### **🧠 Raisonnement Complexe**

**ÉTAPE 1 : Triage + Analyse contraintes**

```
Ordre priorité : S003 (STAT), S002 (URGENT), S004 (URGENT), S001 (ROUTINE)
Contraintes temporelles :
- TECH001 pause : 12:00-13:00  
- TECH002 pause : 12:30-13:30
- S003 STAT arrive : 12:15 (pendant pause TECH001 !)
```

**ÉTAPE 2 : Gestion conflit STAT vs Pause**

```
⚠️ PROBLÈME : S003 (STAT BLOOD) arrive 12:15, TECH001 en pause

SOLUTIONS :
A) Interrompre pause TECH001 (cas exceptionnel STAT) 
B) Différer STAT après 13:00 (NON - délai max 30min)
C) Autre technicien BLOOD (aucun disponible)

DÉCISION : Interrompre pause TECH001 pour STAT
```

**ÉTAPE 3 : Planning optimal avec contraintes**

**11:30-11:45** : S001 commence (ROUTINE MICROBIOLOGY)

```
- TECH002 + EQ003 (MICROBIOLOGY)
- Durée : 60min / 1.0 = 60min
- Fin théorique : 12:30 MAIS pause 12:30-13:30
- Solution : arrêt 12:30, reprise 13:30
- Planning réel : 11:30-12:30 (30min) + 13:30-14:00 (30min)
```

**11:45-12:15** : S002 (URGENT CHEMISTRY)

```
- TECH001 disponible + EQ002
- Durée : 35min / 1.2 = 29min
- Planning : 11:45-12:14 (terminé avant pause)
```

**12:15-12:55** : S003 (STAT BLOOD) - INTERRUPTION PAUSE

```
⚡ URGENCE : Interrompre pause TECH001
- TECH001 + EQ001  
- Durée : 40min / 1.2 = 33min
- Planning : 12:15-12:48
- Note : Pause reportée à 12:48-13:48
```

**13:30-14:20** : S004 (URGENT MICROBIOLOGY)

```  
- TECH002 disponible après pause + EQ003
- Attendre fin S001 : 14:00 + nettoyage 20min = 14:20
- Durée : 50min / 1.0 = 50min  
- Planning : 14:20-15:10
```

### **📋 Résultat Final Complexe**

```json
{
  "schedule": [
    {
      "sampleId": "S002",
      "priority": "URGENT",
      "technicianId": "TECH001",
      "equipmentId": "EQ002",
      "startTime": "11:45", 
      "endTime": "12:14",
      "duration": 29,
      "efficiency": 1.2,
      "status": "completed"
    },
    {
      "sampleId": "S003",
      "priority": "STAT",
      "technicianId": "TECH001",
      "equipmentId": "EQ001",
      "startTime": "12:15",
      "endTime": "12:48", 
      "duration": 33,
      "efficiency": 1.2,
      "status": "lunchInterrupted",
      "lunchBreakRescheduled": "12:48-13:48",
      "notes": "Pause déjeuner interrompue pour STAT"
    },
    {
      "sampleId": "S001", 
      "priority": "ROUTINE",
      "technicianId": "TECH002",
      "equipmentId": "EQ003",
      "startTime": "11:30",
      "pauseTime": "12:30-13:30",
      "resumeTime": "13:30",
      "endTime": "14:00",
      "duration": 60,
      "efficiency": 1.0,
      "status": "pausedForLunch"
    },
    {
      "sampleId": "S004",
      "priority": "URGENT", 
      "technicianId": "TECH002",
      "equipmentId": "EQ003",
      "startTime": "14:20",
      "endTime": "15:10", 
      "duration": 50,
      "efficiency": 1.0,
      "status": "delayedByCleaning",
      "cleaningTime": 20
    }
  ],
  "metadata": {
    "lunchBreaks": [
      {
        "technicianId": "TECH001",
        "planned": "12:00-13:00",
        "actual": "12:48-13:48", 
        "reason": "STAT interruption"
      },
      {
        "technicianId": "TECH002", 
        "planned": "12:30-13:30",
        "actual": "12:30-13:30",
        "reason": "normal"
      }
    ],
    "equipmentCleaning": [
      {
        "equipmentId": "EQ003",
        "between": "S001-S004", 
        "duration": 20
      }
    ]
  },
  "metrics": {
    "totalTime": 220,
    "efficiency": 78.0,
    "conflicts": 0,
    "statResponseTime": 33,
    "lunchInterruptions": 1,
    "constraintViolations": 0,
    "technicianUtilization": 72.5,
    "priorityRespectRate": 100
  }
}
```

### **📖 Leçons Complexes**

* ⚡ **Gestion STAT critique** : interruption pause justifiée
* ⏸️ **Analyses pausables** : S001 suspendu pour pause déjeuner
* 🔄 **Replanning dynamique** : pause TECH001 décalée
* 🧽 **Nettoyage équipement** : S004 retardé par contamination S001
* 📊 **Métriques réalistes** : contraintes impactent performance


---

## 🎯 Synthèse Pédagogique

### **🟢 Exemple 1 → Fondamentaux**

* Tri par priorité
* Allocation ressources
* Planning séquentiel

### **🟡 Exemple 2 → Optimisation**

* Priorité STAT absolue
* Parallélisme intelligent
* Efficacité techniciens

### **🔴 Exemple 3 → Production**

* Contraintes temporelles complexes
* Gestion exceptions (interruptions)
* Métriques avancées
* Cas d'edge réalistes

### **💡 Progression Naturelle**

```
Simple (2 échantillons) → Priorités (3 échantillons) → Contraintes (4+ échantillons)
     ↓                        ↓                           ↓
Logique de base          Optimisation            Gestion production
```

### **✅ Évolutivité Garantie**

* **Structure de base identique** à la version SIMPLE
* **Extensions progressives** : efficiency, lunchBreak, metadata
* **Cohérence ascendante** : le candidat peut faire évoluer son code
* **Compatibilité** : mêmes noms de champs, même format output
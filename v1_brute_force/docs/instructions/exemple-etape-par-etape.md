# 🎮 EXEMPLE ÉTAPE PAR ÉTAPE

## 🎯 Progression Pédagogique

3 exemples qui montent progressivement en difficulté :


1. **Ultra-simple** : 1 échantillon → comprendre les bases
2. **Priorités** : 2 échantillons → comprendre STAT vs URGENT
3. **Ressources** : 3 échantillons → comprendre les conflits de planning


---

## 📍 EXEMPLE 1 : Un Seul Échantillon

### INPUT

```json
{
  "samples": [
    {
      "id": "S001",
      "type": "BLOOD", 
      "priority": "URGENT",
      "analysisTime": 30,
      "arrivalTime": "09:00",
      "patientId": "P001"
    }
  ],
  "technicians": [
    {
      "id": "T001", 
      "name": "Alice Martin",
      "speciality": "BLOOD",
      "startTime": "08:00",
      "endTime": "17:00"
    }
  ],
  "equipment": [
    {
      "id": "E001",
      "name": "Analyseur Sang A",
      "type": "BLOOD", 
      "available": true
    }
  ]
}
```

### LOGIQUE


1. **1 échantillon URGENT BLOOD** arrive à 09:00
2. **Technicien BLOOD** disponible dès 08:00
3. **Équipement BLOOD** disponible dès le début
4. **Assignation** : échantillon peut commencer dès son arrivée (09:00)
5. **Fin** : 09:00 + 30min = 09:30

### OUTPUT ATTENDU

```json
{
  "schedule": [
    {
      "sampleId": "S001",
      "technicianId": "T001", 
      "equipmentId": "E001",
      "startTime": "09:00",
      "endTime": "09:30", 
      "priority": "URGENT"
    }
  ],
  "metrics": {
    "totalTime": 30,      // Une seule analyse de 30min
    "efficiency": 100.0,  // Ressources utilisées à 100%
    "conflicts": 0        // Aucun conflit
  }
}
```

**🎯 Ce que tu apprends :** Structure de base, calcul des créneaux


---

## 📍 EXEMPLE 2 : Priorités STAT vs URGENT

### INPUT

```json
{
  "samples": [
    {
      "id": "S001",
      "type": "BLOOD",
      "priority": "URGENT", 
      "analysisTime": 45,
      "arrivalTime": "09:00",
      "patientId": "P001"
    },
    {
      "id": "S002", 
      "type": "BLOOD",
      "priority": "STAT",
      "analysisTime": 30,
      "arrivalTime": "09:30",
      "patientId": "P002"
    }
  ],
  "technicians": [
    {
      "id": "T001",
      "speciality": "BLOOD", 
      "startTime": "08:00",
      "endTime": "17:00"
    }
  ],
  "equipment": [
    {
      "id": "E001",
      "type": "BLOOD",
      "available": true
    }
  ]
}
```

### LOGIQUE


1. **S001 URGENT** arrive à 09:00, **S002 STAT** arrive à 09:30
2. **MAIS** : STAT a priorité absolue sur URGENT
3. **Tri par priorité** : S002 (STAT) puis S001 (URGENT)
4. **Planning** :
   * S002 démarre dès son arrivée : 09:30-10:00
   * S001 attend que S002 finisse : 10:00-10:45

### OUTPUT ATTENDU

```json
{
  "schedule": [
    {
      "sampleId": "S002",     // STAT en premier ! 
      "technicianId": "T001",
      "equipmentId": "E001", 
      "startTime": "09:30",   // Dès son arrivée
      "endTime": "10:00",
      "priority": "STAT"
    },
    {
      "sampleId": "S001",     // URGENT après
      "technicianId": "T001",
      "equipmentId": "E001",
      "startTime": "10:00",   // Attend la fin du STAT
      "endTime": "10:45", 
      "priority": "URGENT"
    }
  ],
  "metrics": {
    "totalTime": 105,       // 09:30 à 10:45 = 1h15 = 75min
    "efficiency": 71.4,     // (75min d'analyses) / (105min total)
    "conflicts": 0
  }
}
```

**🎯 Ce que tu apprends :** La priorité prime sur l'ordre d'arrivée


---

## 📍 EXEMPLE 3 : Gestion des Ressources

### INPUT

```json
{
  "samples": [
    {
      "id": "S001", 
      "type": "BLOOD",
      "priority": "URGENT",
      "analysisTime": 60,
      "arrivalTime": "09:00", 
      "patientId": "P001"
    },
    {
      "id": "S002",
      "type": "URINE", 
      "priority": "URGENT",
      "analysisTime": 30,
      "arrivalTime": "09:15",
      "patientId": "P002" 
    },
    {
      "id": "S003",
      "type": "BLOOD",
      "priority": "ROUTINE", 
      "analysisTime": 45,
      "arrivalTime": "09:00",
      "patientId": "P003"
    }
  ],
  "technicians": [
    {
      "id": "T001",
      "speciality": "BLOOD",
      "startTime": "08:00", 
      "endTime": "17:00"
    },
    {
      "id": "T002", 
      "speciality": "GENERAL",
      "startTime": "08:00",
      "endTime": "17:00"
    }
  ],
  "equipment": [
    {
      "id": "E001",
      "type": "BLOOD",
      "available": true
    },
    {
      "id": "E002", 
      "type": "URINE",
      "available": true
    }
  ]
}
```

### LOGIQUE


1. **Tri par priorité** : S001 et S002 (URGENT), puis S003 (ROUTINE)
2. **Assignation S001** (URGENT BLOOD) :
   * Technicien T001 (BLOOD) + Équipement E001 (BLOOD)
   * Créneau : 09:00-10:00
3. **Assignation S002** (URGENT URINE) :
   * Technicien T002 (GENERAL peut faire URINE) + Équipement E002 (URINE)
   * Créneau : 09:15-09:45 (en parallèle de S001)
4. **Assignation S003** (ROUTINE BLOOD) :
   * Technicien T001 libre à 10:00 + Équipement E001 libre à 10:00
   * Créneau : 10:00-10:45

### OUTPUT ATTENDU

```json
{
  "schedule": [
    {
      "sampleId": "S001",
      "technicianId": "T001",
      "equipmentId": "E001", 
      "startTime": "09:00",
      "endTime": "10:00",
      "priority": "URGENT"
    },
    {
      "sampleId": "S002", 
      "technicianId": "T002",
      "equipmentId": "E002",
      "startTime": "09:15", 
      "endTime": "09:45",
      "priority": "URGENT"
    },
    {
      "sampleId": "S003",
      "technicianId": "T001", 
      "equipmentId": "E001",
      "startTime": "10:00",
      "endTime": "10:45",
      "priority": "ROUTINE"
    }
  ], 
  "metrics": {
    "totalTime": 105,       // 09:00 à 10:45 = 1h45 = 105min
    "efficiency": 78.6,     // Analyses parallèles = meilleure efficacité
    "conflicts": 0
  }
}
```

**🎯 Ce que tu apprends :** Parallélisme, optimisation des ressources


---


## 🚀 Étape Suivante

Maintenant que tu as vu les exemples, tu peux :


1. Implémenter ta fonction `planifyLab()`
2. Tester avec ces 3 cas
3. Ajouter tes propres cas de test

\n**Le plus dur est fait - tu as compris la logique !** 🎯
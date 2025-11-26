# 📊 DONNÉES MOYENNES

## 🎯 Vue d'Ensemble

**Complexité intermédiaire** : 20 échantillons, 8 techniciens, 5 équipements 

**Réalisme** : Basé sur laboratoire médical de taille moyenne


## 🧪 Échantillons (20 au total)

### **🔴 Priorité STAT (4 échantillons)**

```json
{
  "id": "S001",
  "priority": "STAT",
  "type": "BLOOD", 
  "analysisType": "Numération complète",
  "analysisTime": 45,
  "arrivalTime": "08:30",
  "patientInfo": {
    "age": 67,
    "service": "Urgences",
    "diagnosis": "Suspicion hémorragie"
  }
}

{
  "id": "S008", 
  "priority": "STAT",
  "type": "CHEMISTRY",
  "analysisType": "Troponine",
  "analysisTime": 30,
  "arrivalTime": "09:15",
  "patientInfo": {
    "age": 55,
    "service": "Cardiologie", 
    "diagnosis": "Infarctus suspecté"
  }
}

{
  "id": "S012",
  "priority": "STAT", 
  "type": "MICROBIOLOGY",
  "analysisType": "Hémoculture urgente",
  "analysisTime": 60,
  "arrivalTime": "10:45",
  "patientInfo": {
    "age": 34,
    "service": "Réanimation",
    "diagnosis": "Sepsis sévère"
  }
}

{
  "id": "S017",
  "priority": "STAT",
  "type": "IMMUNOLOGY", 
  "analysisType": "Allergènes critiques",
  "analysisTime": 40,
  "arrivalTime": "13:20",
  "patientInfo": {
    "age": 8,
    "service": "Pédiatrie",
    "diagnosis": "Choc anaphylactique"
  }
}
```

### **🟡 Priorité URGENT (8 échantillons)**

```json
{
  "id": "S002",
  "priority": "URGENT", 
  "type": "CHEMISTRY",
  "analysisType": "Bilan hépatique",
  "analysisTime": 35,
  "arrivalTime": "08:45",
  "patientInfo": {
    "age": 42,
    "service": "Gastroentérologie",
    "diagnosis": "Hépatite virale"
  }
}

{
  "id": "S005",
  "priority": "URGENT",
  "type": "BLOOD", 
  "analysisType": "Coagulation",
  "analysisTime": 25,
  "arrivalTime": "09:30",
  "patientInfo": {
    "age": 73,
    "service": "Chirurgie",
    "diagnosis": "Pré-opératoire"
  }
}

{
  "id": "S009",
  "priority": "URGENT",
  "type": "MICROBIOLOGY",
  "analysisType": "ECBU", 
  "analysisTime": 50,
  "arrivalTime": "10:15",
  "patientInfo": {
    "age": 29,
    "service": "Urologie", 
    "diagnosis": "Infection urinaire"
  }
}

{
  "id": "S011", 
  "priority": "URGENT",
  "type": "GENETICS",
  "analysisType": "Caryotype urgent",
  "analysisTime": 90,
  "arrivalTime": "11:00",
  "patientInfo": {
    "age": 32,
    "service": "Génétique médicale",
    "diagnosis": "Syndrome chromosomique"
  }
}

{
  "id": "S014",
  "priority": "URGENT",
  "type": "IMMUNOLOGY",
  "analysisType": "Sérologie HIV",
  "analysisTime": 55,
  "arrivalTime": "11:45", 
  "patientInfo": {
    "age": 26,
    "service": "Infectiologie",
    "diagnosis": "Exposition VIH"
  }
}

{
  "id": "S016",
  "priority": "URGENT", 
  "type": "BLOOD",
  "analysisType": "Frottis sanguin",
  "analysisTime": 40,
  "arrivalTime": "12:30",
  "patientInfo": {
    "age": 45,
    "service": "Hématologie",
    "diagnosis": "Leucémie suspectée"
  }
}

{
  "id": "S018",
  "priority": "URGENT",
  "type": "CHEMISTRY",
  "analysisType": "Électrolytes",
  "analysisTime": 20,
  "arrivalTime": "14:15",
  "patientInfo": {
    "age": 81,
    "service": "Gériatrie", 
    "diagnosis": "Déshydratation"
  }
}

{
  "id": "S020",
  "priority": "URGENT",
  "type": "MICROBIOLOGY",
  "analysisType": "Parasitologie",
  "analysisTime": 65,
  "arrivalTime": "15:30",
  "patientInfo": {
    "age": 12,
    "service": "Pédiatrie",
    "diagnosis": "Parasitose intestinale"
  }
}
```

### **🟢 Priorité ROUTINE (8 échantillons)**

```json
{
  "id": "S003",
  "priority": "ROUTINE",
  "type": "CHEMISTRY", 
  "analysisType": "Bilan lipidique",
  "analysisTime": 30,
  "arrivalTime": "09:00",
  "patientInfo": {
    "age": 58,
    "service": "Médecine générale",
    "diagnosis": "Contrôle cholestérol"
  }
}

{
  "id": "S004",
  "priority": "ROUTINE",
  "type": "BLOOD",
  "analysisType": "Hémogramme standard", 
  "analysisTime": 25,
  "arrivalTime": "09:15",
  "patientInfo": {
    "age": 35,
    "service": "Médecine du travail",
    "diagnosis": "Visite systématique"
  }
}

{
  "id": "S006",
  "priority": "ROUTINE", 
  "type": "IMMUNOLOGY",
  "analysisType": "Vaccination contrôle",
  "analysisTime": 35,
  "arrivalTime": "10:00",
  "patientInfo": {
    "age": 22,
    "service": "Médecine préventive",
    "diagnosis": "Titre anticorps"
  }
}

{
  "id": "S007",
  "priority": "ROUTINE",
  "type": "GENETICS",
  "analysisType": "Conseil génétique",
  "analysisTime": 120,
  "arrivalTime": "10:30", 
  "patientInfo": {
    "age": 28,
    "service": "Consultation génétique",
    "diagnosis": "Antécédents familiaux"
  }
}

{
  "id": "S010",
  "priority": "ROUTINE",
  "type": "MICROBIOLOGY",
  "analysisType": "Prélèvement gorge",
  "analysisTime": 45,
  "arrivalTime": "11:15",
  "patientInfo": {
    "age": 19,
    "service": "ORL",
    "diagnosis": "Angine récidivante" 
  }
}

{
  "id": "S013", 
  "priority": "ROUTINE",
  "type": "CHEMISTRY",
  "analysisType": "HbA1c",
  "analysisTime": 25,
  "arrivalTime": "12:00",
  "patientInfo": {
    "age": 52,
    "service": "Endocrinologie",
    "diagnosis": "Diabète type 2"
  }
}

{
  "id": "S015",
  "priority": "ROUTINE",
  "type": "BLOOD", 
  "analysisType": "Vitesse sédimentation",
  "analysisTime": 60,
  "arrivalTime": "13:00",
  "patientInfo": {
    "age": 65,
    "service": "Rhumatologie",
    "diagnosis": "Inflammation chronique"
  }
}

{
  "id": "S019",
  "priority": "ROUTINE",
  "type": "GENETICS",
  "analysisType": "Pharmacogénétique", 
  "analysisTime": 90,
  "arrivalTime": "14:45",
  "patientInfo": {
    "age": 47,
    "service": "Oncologie",
    "diagnosis": "Adaptation thérapie"
  }
}
```


---

## 👥 Techniciens (8 au total)

### **🔬 Spécialistes Seniors**

```json
{
  "id": "TECH001",
  "name": "Dr. Marie Dubois",
  "specialty": ["BLOOD", "CHEMISTRY"],
  "efficiency": 1.2,
  "startTime": "07:30",
  "endTime": "16:30",
  "lunchBreak": "12:30-13:30"
}

{
  "id": "TECH002", 
  "name": "Jean-Pierre Martin",
  "specialty": ["MICROBIOLOGY", "IMMUNOLOGY"],
  "efficiency": 1.1,
  "startTime": "08:00",
  "endTime": "17:00", 
  "lunchBreak": "13:00-14:00"
}
```

### **🔬 Spécialistes Standards**

```json
{
  "id": "TECH003",
  "name": "Sophie Bernard",
  "specialty": ["CHEMISTRY", "IMMUNOLOGY"],  
  "efficiency": 1.0,
  "startTime": "08:00",
  "endTime": "17:00",
  "lunchBreak": "12:00-13:00"
}

{
  "id": "TECH004",
  "name": "Lucas Petit",
  "specialty": ["BLOOD", "GENETICS"],
  "efficiency": 0.95,
  "startTime": "09:00", 
  "endTime": "18:00",
  "lunchBreak": "13:00-14:00"
}

{
  "id": "TECH005",
  "name": "Emma Rousseau",
  "specialty": ["MICROBIOLOGY"], 
  "efficiency": 1.0,
  "startTime": "07:00",
  "endTime": "16:00", 
  "lunchBreak": "12:30-13:30"
}

{
  "id": "TECH006",
  "name": "Thomas Moreau",
  "specialty": ["GENETICS", "IMMUNOLOGY"],
  "efficiency": 0.9,
  "startTime": "09:30",
  "endTime": "18:30",
  "lunchBreak": "13:30-14:30"
}
```

### **🔬 Techniciens Polyvalents**

```json
{
  "id": "TECH007",
  "name": "Camille Leroy",
  "specialty": ["CHEMISTRY", "BLOOD", "IMMUNOLOGY"],
  "efficiency": 1.05,
  "startTime": "08:30",
  "endTime": "17:30",
  "lunchBreak": "12:00-13:00"
}

{
  "id": "TECH008", 
  "name": "Antoine Garnier",
  "specialty": ["BLOOD", "MICROBIOLOGY"],
  "efficiency": 0.85,
  "startTime": "10:00",
  "endTime": "19:00",
  "lunchBreak": "14:00-15:00"
}
```


---

## 🔬 Équipements (5 types)

### **🧪 Analyseurs Spécialisés**

```json
{
  "id": "EQ001",
  "name": "Analyseur Hématologie XN-3000", 
  "type": "BLOOD",
  "compatibleTypes": ["Hémogramme", "Numération", "Coagulation", "Frottis"],
  "capacity": 2,
  "maintenanceWindow": "06:00-07:00",
  "cleaningTime": 10
}

{
  "id": "EQ002",
  "name": "Automate Biochimie Cobas 8000",
  "type": "CHEMISTRY", 
  "compatibleTypes": ["Bilan hépatique", "Lipides", "Électrolytes", "Troponine", "HbA1c"],
  "capacity": 3,
  "maintenanceWindow": "06:30-07:30", 
  "cleaningTime": 15
}

{
  "id": "EQ003",
  "name": "Station Microbiologie Vitek MS",
  "type": "MICROBIOLOGY",
  "compatibleTypes": ["ECBU", "Hémoculture", "Parasitologie", "Prélèvement gorge"],
  "capacity": 2, 
  "maintenanceWindow": "07:00-08:00",
  "cleaningTime": 20
}

{
  "id": "EQ004",
  "name": "Système Immunologie Liaison XL",
  "type": "IMMUNOLOGY",
  "compatibleTypes": ["Sérologie", "Allergènes", "Vaccination", "Titre anticorps"],
  "capacity": 2,
  "maintenanceWindow": "05:30-06:30",
  "cleaningTime": 12
}

{
  "id": "EQ005", 
  "name": "Séquenceur Génétique NextSeq",
  "type": "GENETICS",
  "compatibleTypes": ["Caryotype", "Conseil génétique", "Pharmacogénétique"],
  "capacity": 1,
  "maintenanceWindow": "19:00-20:00",
  "cleaningTime": 30
}
```


---

## 📋 Contraintes Techniques

### **⏰ Contraintes Temporelles**

* **Horaires laboratoire** : 07:00 - 19:00
* **Pauses déjeuner** : 1h par technicien entre 12h-15h
* **Maintenance** : équipements indisponibles selon planning
* **Nettoyage** : délai requis entre échantillons

### **🎯 Contraintes Spécialisations**

* **Analyses spécialisées** : technicien compétent obligatoire
* **Équipements dédiés** : type analyse = type équipement
* **Capacité** : plusieurs analyses simultanées selon équipement

### **🔄 Contraintes Optimisation**

* **Efficacité technicien** : coefficient appliqué sur durée
* **Parallélisme** : maximiser analyses simultanées
* **Minimisation attente** : optimiser ordre traitement


---

## 🎯 Format Données d'Entrée

```json
{
  "laboratory": {
    "name": "Laboratoire Central Médical",
    "openingHours": "07:00-19:00",
    "date": "2025-03-15"
  },
  "samples": [/* 20 échantillons */],
  "technicians": [/* 8 techniciens */],
  "equipment": [/* 5 équipements */],
  "constraints": {
    "maxProcessingTime": 720,
    "priorityRules": ["STAT", "URGENT", "ROUTINE"],
    "contaminationPrevention": true,
    "parallelProcessing": true
  }
}
```


---

**🚀 Prêt à voir les contraintes ? Direction [contraintes-moyennes.md](/doc/contraintes-moyennes-zDd4rJFgdt) !**
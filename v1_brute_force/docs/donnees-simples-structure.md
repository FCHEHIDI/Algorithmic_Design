# 📊 DONNÉES SIMPLES - STRUCTURE

## 🎯 Vue d'Ensemble

Tu reçois 3 listes : échantillons, techniciens, équipements. Tu dois produire 1 planning + 3 métriques.

## 📥 INPUT - Ce Que Tu Reçois

### Échantillon (Sample)

```
{
  id: "S001",                    // Identifiant unique
  type: "BLOOD",                 // BLOOD, URINE, ou TISSUE  
  priority: "URGENT",            // STAT, URGENT, ou ROUTINE
  analysisTime: 45,              // Durée en minutes
  arrivalTime: "09:00",          // Heure d'arrivée au labo
  patientId: "P123"              // Pour traçabilité
}
```

### Technicien (Technician)

```
{
  id: "TECH1",
  name: "Alice Martin",
  speciality: "BLOOD",           // BLOOD, URINE, TISSUE, ou GENERAL
  startTime: "08:00",            // Début de service
  endTime: "17:00"               // Fin de service  
}
```

### Équipement (Equipment)

```
{
  id: "EQ001", 
  name: "Analyseur Sang",
  type: "BLOOD",                 // BLOOD, URINE, ou TISSUE
  available: true                // Dispo au début ou pas
}
```

## 📤 OUTPUT - Ce Que Tu Dois Produire

### Planning (Schedule Entry)

```
{
  sampleId: "S001",              // Quel échantillon
  technicianId: "TECH1",         // Quel technicien  
  equipmentId: "EQ001",          // Quel équipement
  startTime: "09:30",            // Heure de début
  endTime: "10:15",              // Heure de fin
  priority: "URGENT"             // Copie pour faciliter le tri
}
```

### Métriques (Metrics)

```
{
  totalTime: 480,                // Durée totale du planning (minutes)
  efficiency: 85.5,              // % temps d'utilisation des ressources  
  conflicts: 0                   // Nombre de conflits détectés
}
```

## 🔍 Détails Importantes

### Priorités (par ordre d'importance)


1. **STAT** - Urgence vitale, résultat en < 1h
2. **URGENT** - Important, résultat dans la journée
3. **ROUTINE** - Standard, peut attendre

### Types d'Échantillons

* **BLOOD** - Analyses sanguines (hémogramme, biochimie)
* **URINE** - Analyses d'urine (ECBU, bandelette)
* **TISSUE** - Biopsies et anatomopathologie

### Spécialités Techniciens

* **BLOOD** - Spécialisé analyses sanguines
* **URINE** - Spécialisé analyses d'urine
* **TISSUE** - Spécialisé anatomopathologie
* **GENERAL** - Polyvalent (peut tout faire mais moins efficace)

## ⚡ Règles de Compatibilité

### Technicien ↔ Échantillon

* Technicien **BLOOD** → Échantillon **BLOOD** ✅
* Technicien **GENERAL** → N'importe quel échantillon ✅
* Technicien **URINE** → Échantillon **BLOOD** ❌

### Équipement ↔ Échantillon

* Équipement **BLOOD** → Échantillon **BLOOD** ✅
* Équipement **URINE** → Échantillon **BLOOD** ❌

## 🕒 Gestion du Temps

### Format Horaires

* **Heures** : Format "HH:MM" (ex: "09:30")
* **Durées** : En minutes (ex: 45 = 45 minutes)

### Calcul des Créneaux

```
Début = Prochain créneau libre pour (technicien ET équipement)
Fin = Début + analysisTime de l'échantillon
```

### Contraintes Horaires

* Techniciens travaillent selon leurs horaires (startTime → endTime)
* Équipements disponibles 24h/24 (sauf si available=false au départ)
* Pas de pause déjeuner dans la version simple

## 🎯 Exemple Concret

### INPUT

```json
samples: [
  { id: "S001", type: "BLOOD", priority: "URGENT", analysisTime: 30, arrivalTime: "09:00" }
]

technicians: [
  { id: "T1", speciality: "BLOOD", startTime: "08:00", endTime: "17:00" }
]

equipment: [
  { id: "E1", type: "BLOOD", available: true }
]
```

### OUTPUT

```json
schedule: [
  {
    sampleId: "S001", 
    technicianId: "T1", 
    equipmentId: "E1",
    startTime: "09:00",    // Dès l'arrivée  
    endTime: "09:30",      // +30min d'analyse
    priority: "URGENT"
  }
]

metrics: {
  totalTime: 30,           // 1 seule analyse de 30min
  efficiency: 100,         // Ressources utilisées à 100%
  conflicts: 0             // Aucun conflit
}
```

## 📚 Prochaine Étape

Maintenant que tu connais la structure, regarde [les règles de base](/doc/regles-de-base-zmeL5w5dSd) pour comprendre la logique métier.
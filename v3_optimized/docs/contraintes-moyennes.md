# ⚙️ CONTRAINTES MOYENNES

## 🎯 Vue d'Ensemble

**8 contraintes essentielles** à respecter pour un planning réaliste de laboratoire médical. 

**Niveau intermédiaire** : contraintes métier importantes sans sur-complexité.


---

## 🔴 CONTRAINTES CRITIQUES (Échec si non respectées)

### **1. 🚨 Priorité STAT Absolue**

```
RÈGLE D'OR : STAT > URGENT > ROUTINE
```

**Description** :

* Les échantillons **STAT** (urgence vitale) passent **TOUJOURS** en premier
* Peuvent **interrompre** une analyse URGENT/ROUTINE en cours
* Délai maximum : **30 minutes** après arrivée

**Exemples** :

* ✅ STAT arrivé à 10h → traité avant 10h30, même si URGENT en cours
* ❌ URGENT traité avant un STAT arrivé plus tôt

**Implémentation** :

```
Si nouveau STAT arrive :
1. Vérifier si analyse interruptible en cours

2. Réquisitionner technicien/équipement approprié  
3. Reprogrammer analyse interrompue

4. Démarrer STAT immédiatement
```


---

### **2. 🎯 Spécialisations Obligatoires**

```
RÈGLE : Type analyse = Spécialité technicien requise
```

**Correspondances obligatoires** :

* **Hématologie** → Technicien spécialisé Hématologie
* **Biochimie** → Technicien spécialisé Biochimie
* **Microbiologie** → Technicien spécialisé Microbiologie
* **Immunologie** → Technicien spécialisé Immunologie
* **Génétique** → Technicien spécialisé Génétique

**Exemples** :

* ✅ Échantillon "Hématologie" → TECH001 (spécialité Hématologie)
* ❌ Échantillon "Génétique" → TECH003 (pas cette spécialité)

**Cas particuliers** :

* **Techniciens polyvalents** : peuvent traiter plusieurs types
* **Urgences STAT** : priorité sur technicien le plus qualifié


---

### **3. ⏰ Pauses Déjeuner Obligatoires**

```
RÈGLE : 1h de pause entre 12h-15h pour chaque technicien
```

**Contraintes** :

* **Durée** : exactement 60 minutes
* **Fenêtre** : entre 12h00 et 15h00
* **Flexibilité** : heure de début choisie par algorithme
* **Indisponibilité** : aucune analyse pendant la pause

**Exemples planning pauses** :

* TECH001 : 12h30-13h30
* TECH002 : 13h00-14h00
* TECH007 : 12h00-13h00

**Optimisation suggérée** :

* **Étaler les pauses** pour maintenir capacité laboratoire
* **Prioriser fin de matinée** pour analyses STAT après-midi


---

## 🟡 CONTRAINTES IMPORTANTES (Points perdus si non respectées)

### **4. 🔬 Équipements Spécialisés**

```
RÈGLE : Type analyse = Type équipement obligatoire
```

**Correspondances** :

* **Analyses Hématologie** → Analyseur Hématologie (EQ001)
* **Analyses Biochimie** → Automate Biochimie (EQ002)
* **Analyses Microbiologie** → Station Microbiologie (EQ003)
* **Analyses Immunologie** → Système Immunologie (EQ004)
* **Analyses Génétique** → Séquenceur Génétique (EQ005)

**Capacités** :

* Certains équipements traitent **plusieurs échantillons simultanément**
* Vérifier `processing_capacity` de chaque équipement
* **File d'attente** si capacité dépassée


---

### **5. ⚙️ Maintenance Quotidienne**

```
RÈGLE : Chaque équipement a une maintenance quotidienne
```

**Indisponibilités** :

* EQ001 (Hématologie) : 06h00-07h00
* EQ002 (Biochimie) : 06h30-07h30
* EQ003 (Microbiologie) : 07h00-08h00
* EQ004 (Immunologie) : 05h30-06h30
* EQ005 (Génétique) : 19h00-20h00

**Impact** :

* **Aucune analyse** pendant maintenance
* **Décaler** les analyses concernées
* **Planifier** autour des créneaux indisponibles


---

### **6. 🧽 Temps de Nettoyage**

```
RÈGLE : Délai nettoyage entre échantillons (contamination)
```

**Durées par équipement** :

* Hématologie : 10 minutes
* Biochimie : 15 minutes
* Microbiologie : 20 minutes
* Immunologie : 12 minutes
* Génétique : 30 minutes

**Application** :

* **Entre chaque échantillon** sur même équipement
* **Automatique** : inclus dans planning
* **Optimisation** : grouper analyses similaires


---

## 🔵 CONTRAINTES D'OPTIMISATION (Bonus qualité)

### **7. 💪 Efficacité Technicien**

```
RÈGLE : Coefficient d'efficacité appliqué aux durées
```

**Coefficients** :

* **Expert** (>8 ans) : 1.2 (20% plus rapide)
* **Senior** (5-8 ans) : 1.0-1.1 (standard à légèrement plus rapide)
* **Standard** (3-5 ans) : 0.95-1.0 (proche standard)
* **Junior** (<3 ans) : 0.8-0.9 (plus lent)

**Calcul** :

```
Durée réelle = Durée base / Coefficient efficacité

Exemple : 
- Analyse 60min, Technicien efficacité 1.2
- Durée réelle = 60 / 1.2 = 50 minutes
```


---

### **8. 🚀 Parallélisme Intelligent**

```
RÈGLE : Maximiser analyses simultanées si ressources disponibles
```

**Conditions parallélisme** :

* **Équipements différents** disponibles
* **Techniciens différents** disponibles
* **Pas de conflit** horaire
* **Respect** autres contraintes

**Exemple optimal** :

```
09h00-09h30 : 
- TECH001 + EQ001 : Analyse Hématologie
- TECH002 + EQ003 : Analyse Microbiologie  
- TECH003 + EQ002 : Analyse Biochimie
→ 3 analyses en parallèle
```


---

## 📊 Matrice de Compatibilité

### **Techniciens → Spécialités**

| Technicien | Hématologie | Biochimie | Microbiologie | Immunologie | Génétique |
|----|----|----|----|----|----|
| TECH001 | ✅ | ✅ | ❌ | ❌ | ❌ |
| TECH002 | ❌ | ❌ | ✅ | ✅ | ❌ |
| TECH003 | ❌ | ✅ | ❌ | ✅ | ❌ |
| TECH004 | ✅ | ❌ | ❌ | ❌ | ✅ |
| TECH005 | ❌ | ❌ | ✅ | ❌ | ❌ |
| TECH006 | ❌ | ❌ | ❌ | ✅ | ✅ |
| TECH007 | ✅ | ✅ | ❌ | ✅ | ❌ |
| TECH008 | ✅ | ❌ | ✅ | ❌ | ❌ |

### **Analyses → Équipements**

| Type Analyse | EQ001 | EQ002 | EQ003 | EQ004 | EQ005 |
|----|----|----|----|----|----|
| Hématologie | ✅ | ❌ | ❌ | ❌ | ❌ |
| Biochimie | ❌ | ✅ | ❌ | ❌ | ❌ |
| Microbiologie | ❌ | ❌ | ✅ | ❌ | ❌ |
| Immunologie | ❌ | ❌ | ❌ | ✅ | ❌ |
| Génétique | ❌ | ❌ | ❌ | ❌ | ✅ |


---

## 🎯 Validation Contraintes

### **✅ Checklist Obligatoire**

**Avant de valider votre planning** :


1. **🔴 STAT traités en premier** ?
   * Tous les STAT avant tous les URGENT/ROUTINE
   * Délai <30min après arrivée respecté
2. **🎯 Spécialisations respectées** ?
   * Chaque analyse assignée à technicien qualifié
   * Aucune analyse hors spécialité
3. **⏰ Pauses déjeuner planifiées** ?
   * 1h de pause pour chaque technicien
   * Entre 12h00 et 15h00
4. **🔬 Équipements corrects** ?
   * Type analyse = type équipement
   * Capacités respectées
5. **⚙️ Maintenances évitées** ?
   * Aucune analyse pendant maintenance
   * Horaires indisponibilité respectés
6. **🧽 Nettoyages inclus** ?
   * Délai nettoyage entre échantillons
   * Temps total cohérent
7. **💪 Efficacités appliquées** ?
   * Coefficients techniciens pris en compte
   * Durées recalculées correctement
8. **🚀 Parallélisme optimisé** ?
   * Ressources multiples utilisées
   * Aucun conflit temporel


---

## 🚨 Cas d'Exception

### **Interruption STAT**

```
Situation : STAT arrive pendant analyse URGENT

Action :
1. PAUSE analyse URGENT si >50% restante

2. Libérer technicien/équipement pour STAT  
3. Reprendre URGENT après STAT terminé
4. Recalculer planning complet si nécessaire
```

### **Conflit Ressources**

```
Situation : 2 analyses simultanées même équipement

Action :
1. Priorité = priorité échantillon (STAT > URGENT > ROUTINE)
2. Si même priorité = premier arrivé servi

3. Reporter analyse moins prioritaire

4. Optimiser allocation sur autres ressources
```

### **Technicien Indisponible**

```
Situation : Technicien en pause, maladie, etc.
Action :
1. Vérifier autres techniciens même spécialité
2. Si aucun = reporter analyse après disponibilité
3. Si STAT = interrompre pause (cas exceptionnel)
4. Recalculer métriques impactées
```


---

**🚀 Contraintes maîtrisées ? Direction [exemples-progressifs.md](exemples-progressifs.md) pour voir l'application !**
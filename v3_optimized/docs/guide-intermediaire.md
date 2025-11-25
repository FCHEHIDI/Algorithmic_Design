# 🔵 GUIDE INTERMÉDIAIRE

## 🎯 Ta Mission

Développer un **système de planification** pour laboratoire médical gérant **20 échantillons** avec **8 techniciens spécialisés**.


---

## 📊 Vue d'Ensemble

### **Problématique Métier**

Un laboratoire médical reçoit des échantillons avec différentes **priorités** et **types d'analyses**. Il faut optimiser le planning pour :

* **Respecter les urgences** médicales (STAT = vie/mort)
* **Utiliser efficacement** les ressources humaines
* **Minimiser les temps d'attente** des patients

### **Données d'Entrée**

* **20 échantillons** avec priorité, type, durée
* **8 techniciens** avec spécialités et efficacité
* **5 types d'équipements** spécialisés
* **Contraintes** : pauses, maintenance, contamination

### **Sortie Attendue**

* **Planning chronologique** détaillé
* **6 métriques** de performance
* **Justification** des choix algorithmiques


---

## 🎯 Approche Technique

### **🏗️ Architecture Recommandée (POO)**

**Idéal** : Structure orientée objet avec classes métier

```
Classes suggérées :
- Sample (échantillon)
- Technician (technicien) 
- Equipment (équipement)
- Scheduler (planificateur)
- Metrics (métriques)
```

### **📦 Alternative Fonctionnelle**

**Acceptable** : Code fonctionnel bien structuré

* Légère pénalité (-10% sur architecture)
* Focus sur **clarté** et **logique**
* Séparation **données / traitement**


---

## ⚡ Algorithme en 4 Étapes

### **🔥 ÉTAPE 1 : Triage Priorités**

```
Ordre absolu : STAT > URGENT > ROUTINE

Les STAT interrompent tout le reste
```

### **🎯 ÉTAPE 2 : Allocation Ressources**

```
Pour chaque échantillon :
1. Trouver technicien compatible + disponible

2. Vérifier équipement spécialisé
3. Calculer créneaux libres

4. Assigner au meilleur slot
```

### **⚙️ ÉTAPE 3 : Gestion Contraintes**

```
- Pauses déjeuner (12h-14h)
- Spécialisations requises
- Maintenance équipements
- Temps nettoyage contamination
```

### **📈 ÉTAPE 4 : Métriques**

```
1. Temps total laboratoire

2. Temps attente moyen par priorité  
3. Utilisation techniciens (%)
4. Efficacité globale

5. Respect priorités (%)
6. Taux parallélisme (%)
```


---

## 🧠 Stratégies d'Optimisation

### **🚀 Parallélisme Intelligent**

* **Analyses simultanées** sur équipements différents
* **Techniciens multitâches** selon spécialités
* **Pipeline** : préparation pendant analyse

### **⏰ Gestion Temporelle**

* **Fenêtres optimales** : éviter pauses déjeuner
* **Batch processing** : grouper analyses similaires
* **Priorisation dynamique** : STAT peut interrompre

### **🔧 Efficacité Ressources**

* **Matching optimal** technicien/échantillon
* **Load balancing** : équilibrer charges
* **Maintenance préventive** : planifier arrêts


---

## 📋 Contraintes à Respecter

### **🔴 Contraintes Critiques**


1. **STAT priorité absolue** (interrompt tout)
2. **Spécialisations obligatoires** (pas de sang → microbio)
3. **Pauses déjeuner** (1h entre 12h-14h par technicien)

### **🟡 Contraintes Importantes**


4. **Types analyses** (équipement spécialisé requis)
5. **Temps traitement** (varie selon complexité)
6. **Maintenance quotidienne** (1 équipement/jour)

### **🔵 Contraintes d'Optimisation**


7. **Contamination** (délai nettoyage entre échantillons)
8. **Efficacité technicien** (coefficient 0.8-1.2)


---

## 🎮 Gestion des Cas Complexes

### **🚨 Urgence STAT**

```
Si échantillon STAT arrive :
1. Interrompre analyse en cours (si possible)
2. Réquisitionner technicien spécialisé
3. Décaler planning existant

4. Recalculer métriques
```

### **⚙️ Panne Équipement**

```
Si équipement en maintenance :
1. Reporter analyses concernées

2. Redistribuer sur équipements compatibles

3. Allonger planning si nécessaire

4. Informer impacts délais
```

### **👥 Technicien Indisponible**

```
Si pause déjeuner ou maladie :
1. Vérifier autres techniciens qualifiés

2. Décaler créneaux si nécessaire

3. Optimiser charge restante

4. Respecter spécialisations
```


---

## 📊 Métriques de Performance

### **⏱️ Métriques Temporelles**

* **Temps total** : durée complète laboratoire
* **Temps attente moyen** : par niveau priorité
* **Respect délais** : % échantillons dans les temps

### **📈 Métriques Efficacité**

* **Utilisation techniciens** : % temps actif
* **Taux parallélisme** : analyses simultanées
* **Efficacité globale** : score composite


---

## 🛠️ Conseils Développement

### **🎯 Commencer Simple**


1. **Version basique** : tri + allocation séquentielle
2. **Ajouter contraintes** une par une
3. **Optimiser** en dernier
4. **Tester** chaque étape

### **🏗️ Structure Code**

* **Séparation responsabilités** (SRP)
* **Classes métier** explicites
* **Gestion erreurs** robuste
* **Code lisible** et commenté

### **🧪 Tests Essentiels**

* **Happy path** : cas nominal
* **Edge cases** : urgences, pannes
* **Validation données** : inputs incorrects
* **Performance** : 20 échantillons OK


---

## 📦 Livrables Attendus

### **📋 Fichiers Obligatoires**

* **Code source** fonctionnel
* **[README.md](/doc/laboratoire-version-intermediaire-KwcG1Xbzea)** avec instructions
* **Exemple sortie** JSON avec vos données
* **Tests** (au minimum fonction principale)


---

## 🎯 Critères d'Évaluation

| Critère | Poids | Détail |
|----|----|----|
| **🏗️ Architecture** | 25% | Structure POO/fonctionnelle claire |
| **⚡ Algorithme** | 30% | Logique tri + optimisation |
| **💻 Code Quality** | 20% | Lisibilité, robustesse |
| **📊 Fonctionnel** | 20% | Planning cohérent + métriques |
| **📖 Documentation** | 5% | README + commentaires |

### **🎁 Bonus Possibles** (+15% max)

* **Tests complets** (+5%)
* **Gestion d'erreurs** avancée (+5%)
* **Optimisations** créatives (+5%)


---

## 🚨 Points d'Attention

### **✅ Réussite Assurée**

* **Priorités respectées** (STAT > URGENT > ROUTINE)
* **Spécialisations** techniciens vérifiées
* **Contraintes temporelles** intégrées
* **Code structuré** et lisible

### **❌ Écueils à Éviter**

* **Sur-ingénierie** (solution trop complexe)
* **Contraintes oubliées** (pauses, maintenance)
* **Performance** (algorithme exponentiel)
* **Tests insuffisants** (happy path seulement)


---

**🚀 Prêt pour le défi ? Direction [donnees-moyennes.md](/doc/donnees-moyennes-laboratoire-KYEqcHpj0W) pour voir les données !**
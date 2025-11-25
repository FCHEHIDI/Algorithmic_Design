# 🎯 GUIDE SIMPLE

## 🎯 Ta Mission

Créer une fonction `planifyLab(data)` qui organise les analyses de laboratoire médical.

**En gros :** Tu reçois des échantillons à analyser, tu les assignes aux bons techniciens sur les bons équipements, sans conflit d'horaire.

## 🏥 Le Contexte

Tu travailles pour un laboratoire médical. Des échantillons arrivent (sang, urine, etc.) avec différents niveaux d'urgence. Tu dois les planifier intelligemment :

* **STAT** = Urgence vitale (résultat en 1h max)
* **URGENT** = Important mais pas vital (résultat dans la journée)
* **ROUTINE** = Analyse standard (peut attendre)

## 📊 Ce Que Tu Reçois

```
INPUT: Un objet avec
- samples[] : Liste des échantillons à analyser
- technicians[] : Liste des techniciens disponibles  
- equipment[] : Liste des équipements du labo
```

## 🎯 Ce Que Tu Dois Produire

```
OUTPUT: Un objet avec
- schedule[] : Planning chronologique des analyses
- metrics{} : 3 métriques de base (temps total, efficacité, conflits)
```

## 🔥 L'Algorithme en 4 Étapes

### Étape 1 : Trier Par Urgence (30min)

Les échantillons STAT passent TOUJOURS en premier. Puis URGENT. Puis ROUTINE.

### Étape 2 : Assigner les Ressources (2h)

Pour chaque échantillon (dans l'ordre de priorité) :

* Trouve un technicien compatible (spécialité + disponibilité)
* Trouve un équipement compatible (type + disponibilité)

### Étape 3 : Planifier les Créneaux (2h)

* Calcule le prochain créneau libre pour le technicien ET l'équipement
* Bloque le créneau (durée = temps d'analyse de l'échantillon)
* Ajoute au planning

### Étape 4 : Calculer les Métriques (1h)

* **Temps total** : Durée du planning complet
* **Efficacité** : % du temps où les ressources sont utilisées
* **Conflits** : Nombre de conflits détectés (doit être 0)

## ⚡ Les Règles Essentielles


1. **PRIORITÉ ABSOLUE** : STAT > URGENT > ROUTINE (jamais d'exception)
2. **COMPATIBILITÉ** : Technicien BLOOD avec échantillon BLOOD, etc.
3. **DISPONIBILITÉ** : Pas de double booking des ressources
4. **CHRONOLOGIE** : Le planning doit être ordonné dans le temps

## 🎮 Stratégie de Développement

### Phase 1 : Version Basique (2h)

* Trier les échantillons
* Assigner naïvement (premier technicien + équipement disponible)
* Planning simple sans optimisation

### Phase 2 : Gestion des Conflits (2h)

* Vérifier disponibilité des ressources
* Gérer les créneaux occupés
* Calculer les métriques

### Phase 3 : Peaufinage (1h30)

* Optimiser l'ordre d'assignation
* Améliorer les métriques
* Tests et validation

## 🚨 Pièges à Éviter

* **Ne pas** essayer d'optimiser dès le départ
* **Ne pas** oublier que STAT est TOUJOURS prioritaire
* **Ne pas** assigner un technicien à 2 endroits en même temps
* **Ne pas** compliquer : version simple = logique directe

## 📈 Comment Savoir si c'est Bon ?

✅ **Ton planning respecte les priorités** (tous les STAT en premier)\n✅ **Aucun conflit de ressources** (metrics.conflicts = 0)\n✅ **Planning chronologique** (ordonné par heure de début)\n✅ **Métriques cohérentes** (temps total > 0, efficacité entre 0-100%)

## 🎯 Exemple Ultra-Simple

```
INPUT:
- 1 échantillon URGENT BLOOD
- 1 technicien spécialisé BLOOD  
- 1 équipement BLOOD

OUTPUT:
- 1 ligne dans le planning
- Métriques basiques
```

**C'est tout !** Pas de complexité cachée dans la version simple.


---

## 📚 Prochaine Étape

Regarde [les données détaillées](/doc/donnees-simples-structure-XbRODnmjcM) pour comprendre la structure exacte des objets.
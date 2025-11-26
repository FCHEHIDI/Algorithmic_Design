# 🔴 Version 1 : Brute Force Approach

## 📋 Description

**Première implémentation** de l'algorithme de planification de laboratoire médical.

Approche naïve utilisant une stratégie de force brute pour assigner les échantillons aux ressources disponibles.

## 📂 Contenu

- **`planify_lab.py`** : Implémentation principale (fonction God)
- **`LIMITATIONS_V1.md`** : Analyse détaillée des limitations
- **`docs/`** : Documentation technique complète

## ⚙️ Caractéristiques

### Algorithme
- **Complexité** : O(S × T × E) - Très inefficace
- **Stratégie** : Itération séquentielle sur tous les échantillons
- **Tri** : Par priorité (STAT > URGENT > ROUTINE)
- **Assignment** : Premier technicien/équipement disponible

### Architecture
- ❌ Fonction monolithique (God function)
- ❌ Pas de séparation des responsabilités
- ❌ Gestion d'erreurs minimale
- ❌ Pas d'indexation

## 📊 Performances

| Métrique | Valeur |
|----------|--------|
| **Complexité temporelle** | O(S × T × E) |
| **Complexité spatiale** | O(S + T + E) |
| **Temps moyen (100 samples)** | ~5-10 ms |
| **Maintenabilité** | ⭐ (1/5) |

## 🚫 Limitations Principales

1. **Performance** : Complexité cubique inacceptable pour >1000 échantillons
2. **Maintenabilité** : Code monolithique difficile à modifier
3. **Scalabilité** : Pas d'optimisation pour charges élevées
4. **Robustesse** : Gestion d'erreurs basique

## ➡️ Évolution vers V2

La V2 introduit :
- ✅ Indexation à deux niveaux (Priority → Type)
- ✅ Pools de ressources par spécialité
- ✅ Complexité réduite à O(S + T + E)
- ✅ Architecture modulaire

---

**Status** : ⚠️ Proof of Concept - Ne pas utiliser en production

**Branche Git** : `feature/brute-force-approach`

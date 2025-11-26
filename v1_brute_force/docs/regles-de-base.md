# 🔥 RÈGLES DE BASE

## ⚡ LA RÈGLE D'OR

```
STAT > URGENT > ROUTINE

TOUJOURS. SANS EXCEPTION. MÊME SI ÇA COMPLIQUE TOUT.
```

Un échantillon STAT qui arrive à 16h55 passe AVANT un ROUTINE qui attend depuis 8h00.

## 📋 Les 4 Règles Essentielles

### 1. 🚨 PRIORITÉ ABSOLUE

**STAT** = Urgence vitale (patient en danger)

* Passe devant TOUT le monde
* Résultat attendu en moins d'1 heure
* Dans le planning final, TOUJOURS traité avant tout URGENT ou ROUTINE

**URGENT** = Important pour la prise en charge

* Passe devant ROUTINE
* Résultat attendu dans la journée
* Peut attendre si STAT arrive

**ROUTINE** = Analyse standard

* Passe en dernier
* Peut attendre plusieurs heures si nécessaire

### 2. 🎯 COMPATIBILITÉ TECHNICIEN

| Technicien | Peut analyser |
|----|----|
| BLOOD | Échantillons BLOOD uniquement |
| URINE | Échantillons URINE uniquement |
| TISSUE | Échantillons TISSUE uniquement |
| GENERAL | TOUS les types (mais moins efficace) |

**Pourquoi ?** Chaque type d'analyse nécessite des compétences spécifiques.

### 3. 🔧 COMPATIBILITÉ ÉQUIPEMENT

| Équipement | Peut traiter |
|----|----|
| BLOOD | Échantillons BLOOD uniquement |
| URINE | Échantillons URINE uniquement |
| TISSUE | Échantillons TISSUE uniquement |

**Pas d'équipement GENERAL** - chaque machine est spécialisée.

### 4. 📅 DISPONIBILITÉ TEMPORELLE

**Techniciens**

* Travaillent selon leurs horaires (startTime → endTime)
* Ne peuvent traiter qu'1 échantillon à la fois
* Pas de chevauchement d'analyses

**Équipements**

* Disponibles 24h/24 (sauf si available=false)
* Ne peuvent traiter qu'1 échantillon à la fois
* Pas de maintenance dans la version simple

## 🧠 Logique de Planification

### Étape 1 : Tri par Priorité

```
1. Tous les STAT (par heure d'arrivée)
2. Tous les URGENT (par heure d'arrivée)  
3. Tous les ROUTINE (par heure d'arrivée)
```

### Étape 2 : Assignation Séquentielle

Pour chaque échantillon (dans l'ordre de priorité) :


1. **Trouve technicien compatible ET disponible**
2. **Trouve équipement compatible ET disponible**
3. **Calcule prochain créneau libre** (max des 2 disponibilités)
4. **Bloque les ressources** pendant analysisTime
5. **Ajoute au planning**

### Étape 3 : Gestion des Indisponibilités

**Si technicien occupé** → Attendre qu'il se libère **Si équipement occupé** → Attendre qu'il se libère\n**Si les deux occupés** → Attendre le max des deux

## 🚨 CLARIFICATION IMPORTANTE : PLANNING STATIQUE

**Dans les versions SIMPLE et INTERMÉDIAIRE :**

✅ **Tous les échantillons sont donnés EN UNE FOIS**\n✅ **Tu calcules UN PLANNING COMPLET**\n✅ **Pas d'interruption, pas d'ajout dynamique**\n✅ **Approche : Input unique → Planning complet → Output**

❌ **PAS de gestion temps réel**\n❌ **PAS d'échantillons qui arrivent pendant l'exécution**\n❌ **PAS d'interruption d'analyses en cours**

## 🚨 Situations Critiques

### Conflit de Ressources

```
Échantillon A : 09:00-09:30 sur Technicien T1
Échantillon B : Veut T1 à 09:15

Solution : B commence à 09:30 (après A)
```

### Technicien Pas Compatible

```
Échantillon BLOOD + Technicien URINE = IMPOSSIBLE

Solutions :
1. Chercher technicien BLOOD libre

2. Utiliser technicien GENERAL si disponible

3. Attendre qu'un technicien BLOOD se libère
```

### Priorité vs Chronologie

```
09:00 - Échantillon ROUTINE arrive

09:30 - Échantillon STAT arrive  

Résultat : STAT passe EN PREMIER même s'il arrive après
```

## ✅ Validation du Planning

### Ton planning est BON si :


1. **Priorités respectées** : Tous les STAT avant tous les URGENT, etc.
2. **Compatibilités OK** : Chaque (technicien, équipement, échantillon) est compatible
3. **Pas de conflits** : Aucune ressource à 2 endroits en même temps
4. **Chronologique** : Planning trié par heure de début
5. **Horaires cohérents** : startTime < endTime, dans les horaires de travail

### Ton planning est MAUVAIS si :

❌ Un URGENT passe avant un STAT 

❌ Technicien BLOOD traite échantillon URINE\n❌ 2 échantillons sur même équipement en même temps 

❌ Technicien travaille en dehors de ses horaires 

❌ Analyse se termine avant qu'elle commence (bug de calcul)

## 🎯 Métriques de Qualité

### Temps Total

```
Durée entre première analyse et dernière analyse
```

### Efficacité

```
% de temps où les ressources sont utilisées
(temps actif) / (temps total) * 100
```

### Conflits

```
Nombre de violations des règles détectées

DOIT être 0 dans un bon planning
```

## 💡 Conseils de Développement


1. **Commence simple** : 1 échantillon, 1 technicien, 1 équipement
2. **Vérifie à chaque étape** : ajoute des logs pour voir ce qui se passe
3. **Teste les cas limites** : STAT qui arrive tard, ressources occupées
4. **Valide les règles** : écris des fonctions de vérification

## 📚 Prochaine Étape

Regarde l'exemple progressif pour voir ces règles en action !
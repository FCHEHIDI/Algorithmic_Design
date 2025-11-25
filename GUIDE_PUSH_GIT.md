# 🚀 Guide de Push Git - Planificateur de Laboratoire

## 📊 État Actuel du Dépôt

Vous avez maintenant **2 branches** prêtes à être poussées vers un dépôt distant :

```
📦 Algorithmic_Design (dépôt local)
├── 🌿 feature/brute-force-approach
│   ├── ✅ Commit: ba73f66 "feat: Implémentation V1 et V2..."
│   ├── 📂 BruteForceApproach/
│   │   ├── planify_lab.py (V1 - Brute Force)
│   │   ├── planify_next_lab.py (V2 - Indexée)
│   │   ├── LIMITATIONS_V1.md
│   │   ├── LIMITATIONS_V2.md
│   │   └── README.md
│   └── 📄 .gitignore
│
└── 🌿 feature/optimized-modular-approach
    ├── ✅ Commit: 7e0ec42 "feat: V3 Architecture OOP modulaire..."
    └── 📂 v3_optimized/
        ├── lab_planner/ (package modulaire)
        ├── Dockerfile
        ├── docker-compose.yml
        └── README.md (documentation complète)
```

---

## 🎯 Étapes pour Pusher vers GitHub/GitLab

### Étape 1 : Créer un Dépôt Distant

#### Option A : GitHub

1. Aller sur https://github.com/new
2. Nom du dépôt : `algorithmic-design-lab-planner`
3. Description : `Lab planning system with brute force (V1/V2) and OOP optimized (V3) implementations`
4. Visibilité : **Private** (recommandé pour projet académique)
5. **NE PAS** initialiser avec README/license/.gitignore (déjà présents localement)
6. Cliquer **Create repository**

#### Option B : GitLab

1. Aller sur https://gitlab.com/projects/new
2. Même configuration que ci-dessus
3. Cliquer **Create project**

---

### Étape 2 : Lier le Dépôt Local au Distant

```powershell
# Copier l'URL fournie par GitHub/GitLab
# Exemple GitHub: https://github.com/VOTRE_USERNAME/algorithmic-design-lab-planner.git
# Exemple GitLab: https://gitlab.com/VOTRE_USERNAME/algorithmic-design-lab-planner.git

# Ajouter le remote (remplacer URL_DU_DEPOT par votre URL)
git remote add origin URL_DU_DEPOT

# Vérifier que le remote est ajouté
git remote -v
# Devrait afficher :
# origin  https://github.com/VOTRE_USERNAME/algorithmic-design-lab-planner.git (fetch)
# origin  https://github.com/VOTRE_USERNAME/algorithmic-design-lab-planner.git (push)
```

---

### Étape 3 : Pusher la Branche Brute Force

```powershell
# Basculer sur la branche brute-force
git checkout feature/brute-force-approach

# Pusher vers le remote (première fois)
git push -u origin feature/brute-force-approach

# Le flag -u (--set-upstream) lie la branche locale à la branche distante
# Les prochains push pourront être simplement : git push
```

**🎓 Explication du flag `-u`**

```powershell
# Première fois (avec -u)
git push -u origin feature/brute-force-approach
# → Crée la branche distante ET lie les deux branches

# Les fois suivantes (sans -u)
git push  # Suffisant ! Git sait où pusher
```

---

### Étape 4 : Pusher la Branche Optimisée

```powershell
# Basculer sur la branche optimisée
git checkout feature/optimized-modular-approach

# Pusher vers le remote
git push -u origin feature/optimized-modular-approach
```

---

### Étape 5 : Créer une Branche Main/Master (Optionnel)

Si vous voulez une branche principale stable :

```powershell
# Créer une branche main depuis brute-force (point de départ)
git checkout -b main

# Pusher la branche main
git push -u origin main

# Définir main comme branche par défaut sur GitHub :
# Settings → Branches → Default branch → main → Update
```

---

## 📋 Vérifications Post-Push

### 1. Vérifier les Branches Distantes

```powershell
# Lister toutes les branches (locales et distantes)
git branch -a

# Devrait afficher :
#   main (si créée)
#   feature/brute-force-approach
#   feature/optimized-modular-approach
#   remotes/origin/feature/brute-force-approach
#   remotes/origin/feature/optimized-modular-approach
```

### 2. Vérifier sur le Web

Aller sur votre dépôt GitHub/GitLab :
- ✅ Vous devriez voir **2 branches** (ou 3 avec main)
- ✅ Chaque branche contient ses fichiers spécifiques
- ✅ Les commits sont visibles avec leurs messages

---

## 🔄 Workflow de Développement Recommandé

### Scénario 1 : Corriger un Bug dans V1

```powershell
# 1. Basculer sur la branche
git checkout feature/brute-force-approach

# 2. Faire les modifications
# ... éditer BruteForceApproach/planify_lab.py ...

# 3. Commiter
git add BruteForceApproach/planify_lab.py
git commit -m "fix: Correction bug validation V1"

# 4. Pusher
git push  # Pas besoin de -u, déjà configuré
```

### Scénario 2 : Ajouter une Feature à V3

```powershell
# 1. Basculer sur la branche
git checkout feature/optimized-modular-approach

# 2. Créer une sous-branche pour la feature
git checkout -b feature/v3-add-lunch-breaks

# 3. Développer la feature
# ... éditer lab_planner/scheduling/constraints.py ...

# 4. Commiter
git add v3_optimized/lab_planner/
git commit -m "feat: Ajout contrainte pauses déjeuner"

# 5. Pusher la nouvelle branche
git push -u origin feature/v3-add-lunch-breaks

# 6. Créer une Pull Request sur GitHub pour merger dans feature/optimized-modular-approach
```

### Scénario 3 : Synchroniser avec le Remote

```powershell
# Récupérer les dernières modifications du remote
git fetch origin

# Voir les différences
git log HEAD..origin/feature/brute-force-approach

# Fusionner les changements distants
git pull origin feature/brute-force-approach
```

---

## 🛡️ Bonnes Pratiques Git

### 1. Messages de Commit Conventionnels

Utilisez le format **Conventional Commits** :

```
<type>(<scope>): <description>

[corps optionnel]

[footer optionnel]
```

**Types** :
- `feat`: Nouvelle fonctionnalité
- `fix`: Correction de bug
- `docs`: Documentation uniquement
- `style`: Formatage, point-virgules manquants, etc.
- `refactor`: Refactoring sans changer le comportement
- `test`: Ajout de tests
- `chore`: Maintenance (dépendances, config)

**Exemples** :

```powershell
git commit -m "feat(v3): Ajout stratégie ShortestJobFirst"
git commit -m "fix(v1): Correction validation priorité STAT"
git commit -m "docs(readme): Ajout section Docker"
git commit -m "refactor(v2): Simplification build_index"
git commit -m "test(v3): Ajout tests unitaires ResourcePool"
```

### 2. Branches Descriptives

```powershell
# ✅ BON : Descriptif et namespaced
feature/v3-add-lunch-breaks
bugfix/v1-priority-sorting
docs/update-readme-docker

# ❌ MAUVAIS : Vague
fix-bug
update
test
```

### 3. Commits Atomiques

**Principe** : Un commit = **une seule modification logique**.

```powershell
# ❌ MAUVAIS : Trop de choses dans un commit
git add .
git commit -m "Fix bugs and add feature and update docs"

# ✅ BON : Commits séparés
git add BruteForceApproach/planify_lab.py
git commit -m "fix(v1): Correction bug validation"

git add v3_optimized/lab_planner/scheduling/
git commit -m "feat(v3): Nouvelle stratégie d'ordonnancement"

git add README.md
git commit -m "docs: Mise à jour section installation Docker"
```

### 4. .gitignore Complet

Votre `.gitignore` actuel est bon, mais vérifiez régulièrement :

```powershell
# Voir ce qui serait ignoré
git status --ignored

# Ajouter de nouvelles règles si nécessaire
echo "*.bak" >> .gitignore
git add .gitignore
git commit -m "chore: Ajout fichiers .bak au gitignore"
```

---

## 🚨 Commandes de Secours

### Annuler le Dernier Commit (avant push)

```powershell
# Annuler le commit mais garder les modifications
git reset --soft HEAD~1

# Annuler le commit ET les modifications (DANGER)
git reset --hard HEAD~1
```

### Récupérer un Fichier Supprimé

```powershell
# Récupérer depuis le dernier commit
git checkout HEAD -- chemin/vers/fichier.py

# Récupérer depuis un commit spécifique
git checkout abc1234 -- chemin/vers/fichier.py
```

### Résoudre un Conflit de Merge

```powershell
# Si un pull crée un conflit
git pull origin feature/brute-force-approach

# Git marque les fichiers en conflit
# Éditer les fichiers, chercher les marqueurs :
# <<<<<<< HEAD
# Votre version
# =======
# Version distante
# >>>>>>> origin/feature/brute-force-approach

# Après résolution
git add fichier_resolu.py
git commit -m "merge: Résolution conflit validation"
```

### Voir l'Historique

```powershell
# Historique complet
git log

# Historique condensé
git log --oneline

# Historique graphique
git log --oneline --graph --all

# Historique d'un fichier spécifique
git log -- BruteForceApproach/planify_lab.py
```

---

## 📊 Commandes Git Utiles

### Statut et Différences

```powershell
# Statut actuel
git status

# Différences non staged
git diff

# Différences staged (dans l'index)
git diff --cached

# Différences entre branches
git diff feature/brute-force-approach..feature/optimized-modular-approach

# Statistiques de différences
git diff --stat
```

### Branches

```powershell
# Lister branches locales
git branch

# Lister toutes les branches (locales + distantes)
git branch -a

# Créer nouvelle branche
git checkout -b nouvelle-branche

# Supprimer branche locale
git branch -d nom-branche

# Supprimer branche distante
git push origin --delete nom-branche

# Renommer branche
git branch -m ancien-nom nouveau-nom
```

### Tags

```powershell
# Créer un tag (version)
git tag -a v1.0.0 -m "Version 1.0.0 - Brute Force Baseline"

# Pusher tags
git push --tags

# Lister tags
git tag
```

---

## 🎓 Ressources Git

### Documentation Officielle

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com/)
- [GitLab Documentation](https://docs.gitlab.com/)

### Outils Visuels

- **Git Graph** (VS Code Extension) : Visualiser l'historique
- **GitKraken** : Client Git graphique
- **SourceTree** : Client Git gratuit

### Cheatsheets

- [GitHub Git Cheatsheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [Atlassian Git Cheatsheet](https://www.atlassian.com/git/tutorials/atlassian-git-cheatsheet)

---

## ✅ Checklist Avant de Pusher

Avant chaque `git push`, vérifiez :

- [ ] **Tests passent** : `python main.py` (pour V3)
- [ ] **Pas de fichiers sensibles** : Pas de mots de passe, clés API
- [ ] **.gitignore à jour** : Fichiers temporaires exclus
- [ ] **Message de commit clair** : Format Conventional Commits
- [ ] **Branche correcte** : `git branch` pour vérifier
- [ ] **Remote correct** : `git remote -v` pour vérifier

---

## 🎯 Prochaines Étapes

1. **Pusher les deux branches** (suivre les étapes ci-dessus)
2. **Créer un README.md racine** avec vue d'ensemble du projet
3. **Ajouter GitHub Actions** (CI/CD) pour tests automatiques
4. **Créer des Issues** sur GitHub pour tracker les TODOs
5. **Mettre en place un Project Board** pour la gestion

---

## 📝 Template README Racine (Optionnel)

Créer `README.md` à la racine pour la page d'accueil du dépôt :

```markdown
# 🧪 Algorithmic Design - Lab Planner

Système de planification de laboratoire avec 3 versions évolutives.

## 📚 Branches

- **feature/brute-force-approach** : V1 (brute force) et V2 (indexée)
- **feature/optimized-modular-approach** : V3 (OOP modulaire + Docker)

## 🚀 Quick Start

Voir le README de chaque branche pour les détails.

## 📊 Comparaison

| Version | Complexité | Architecture | Docker | Tests |
|---------|-----------|--------------|--------|-------|
| V1 | O(S×T×E) | Monolithique | ❌ | ❌ |
| V2 | O(S+T+E) | Procédurale | ❌ | ❌ |
| V3 | O(S+T+E) | OOP Modulaire | ✅ | ✅ |
```

---

**Bonne chance pour le push ! 🚀**

---

**Dernière mise à jour** : 25 novembre 2025

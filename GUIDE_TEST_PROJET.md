# 🧪 Guide de Test Complet du Projet

## 📋 Vue d'Ensemble

Ce guide vous permet de tester systématiquement toutes les fonctionnalités de l'application avant la soumission sur Kaggle.

**Temps estimé :** 2-3 heures pour un test complet

---

## 🔧 Phase 1 : Préparation de l'Environnement

### 1.1 Vérifier les Prérequis

- [ ] Python 3.8+ installé
- [ ] Toutes les dépendances installées (`pip install -r requirements.txt`)
- [ ] Clé API Gemini obtenue et valide
- [ ] Fichier `.env` créé avec `GEMINI_API_KEY`

### 1.2 Configuration Initiale

```bash
# 1. Aller dans le dossier du projet
cd gemini_math_stats

# 2. Vérifier que les dépendances sont installées
pip install -r requirements.txt

# 3. Vérifier le fichier .env
# Le fichier .env doit contenir :
# GEMINI_API_KEY=votre_cle_api
# EMAIL_SENDER=votre_email@example.com (optionnel)
# EMAIL_PASSWORD=votre_mot_de_passe (optionnel)
```

### 1.3 Lancer l'Application

```bash
# Lancer Streamlit
streamlit run app.py
```

**Vérification :**
- [ ] L'application démarre sans erreur
- [ ] L'interface s'affiche correctement
- [ ] Pas d'erreurs dans la console

---

## 🎯 Phase 2 : Tests des Fonctionnalités Core

### 2.1 Configuration Gemini

**Test :** Initialisation du client Gemini

**Étapes :**
1. Ouvrir l'application dans le navigateur
2. Dans la sidebar, entrer la clé API Gemini
3. Vérifier que le message "✅ Gemini 3 Pro connecté" apparaît

**Résultat attendu :**
- [ ] Message de succès affiché
- [ ] Pas d'erreur dans la console
- [ ] Les options de génération d'exercices sont disponibles

**Si erreur :**
- Vérifier que la clé API est valide
- Vérifier la connexion internet
- Vérifier les logs dans la console

---

### 2.2 Génération d'Exercices

#### Test 2.2.1 : Génération - Tableau d'Effectifs

**Étapes :**
1. Sélectionner "Tableau d'effectifs" dans le type d'exercice
2. Choisir une difficulté (facile, moyen, difficile)
3. Cliquer sur "🎲 Générer un nouvel exercice"
4. Attendre la génération (peut prendre 10-30 secondes)

**Résultat attendu :**
- [ ] Un exercice apparaît avec :
  - Type d'exercice clairement indiqué
  - Énoncé clair et compréhensible
  - Données nécessaires (liste de valeurs)
  - Instructions claires
- [ ] L'exercice est adapté au niveau 3ème
- [ ] L'exercice est varié (différent à chaque génération)

**Vérifications :**
- [ ] L'énoncé est en français
- [ ] Les données sont cohérentes
- [ ] L'exercice est faisable pour un élève de 3ème

#### Test 2.2.2 : Génération - Calcul de Fréquences

**Étapes :** Identiques au test 2.2.1, mais sélectionner "Calcul de fréquences"

**Résultat attendu :**
- [ ] Exercice sur les fréquences (décimal, fraction, ou pourcentage)
- [ ] Données nécessaires fournies
- [ ] Instructions claires

#### Test 2.2.3 : Génération - Moyenne Pondérée

**Étapes :** Identiques, sélectionner "Moyenne pondérée"

**Résultat attendu :**
- [ ] Exercice avec série statistique
- [ ] Données avec effectifs/coefficients
- [ ] Instructions pour calculer la moyenne pondérée

#### Test 2.2.4 : Génération - Problème Textuel

**Étapes :** Identiques, sélectionner "Problème textuel"

**Résultat attendu :**
- [ ] Problème contextualisé (situation réelle)
- [ ] Données intégrées dans le problème
- [ ] Questions claires

**Tests de Robustesse :**
- [ ] Générer 3-5 exercices de chaque type
- [ ] Vérifier que chaque exercice est différent
- [ ] Vérifier qu'il n'y a pas d'erreurs de génération

---

### 2.3 Upload et Analyse de Copies Manuscrites

#### Test 2.3.1 : Upload d'Image

**Préparation :**
- Préparer une photo de copie manuscrite (ou utiliser un exemple)

**Étapes :**
1. Générer un exercice (ex: Tableau d'effectifs)
2. Résoudre l'exercice sur papier (ou utiliser une copie existante)
3. Prendre une photo de la copie (ou utiliser une image existante)
4. Cliquer sur "📸 Télécharger une photo de ta copie"
5. Sélectionner l'image
6. Vérifier que l'image s'affiche

**Résultat attendu :**
- [ ] L'image s'affiche correctement
- [ ] L'image est lisible
- [ ] Le bouton "🔍 Analyser ma copie" est disponible

**Tests de Robustesse :**
- [ ] Tester avec différentes tailles d'images
- [ ] Tester avec différentes qualités (haute, moyenne, basse)
- [ ] Tester avec différents formats (JPG, PNG)
- [ ] Tester avec une image très grande (> 5MB)
- [ ] Tester avec une image très petite

#### Test 2.3.2 : Analyse de Copie Manuscrite

**Étapes :**
1. Après avoir uploadé une image, cliquer sur "🔍 Analyser ma copie"
2. Attendre l'analyse (peut prendre 20-60 secondes)
3. Vérifier le feedback affiché

**Résultat attendu :**
- [ ] Un feedback complet apparaît avec :
  - [ ] Commentaire général
  - [ ] Analyse de la démarche (étapes)
  - [ ] Points positifs
  - [ ] Erreurs identifiées
  - [ ] Correction détaillée
  - [ ] Conseils personnalisés
  - [ ] Score (ex: 15/20)
- [ ] Le feedback est en français
- [ ] Le feedback est constructif et bienveillant
- [ ] Les erreurs sont expliquées clairement

**Tests de Robustesse :**
- [ ] Tester avec une copie correcte
- [ ] Tester avec une copie avec erreurs
- [ ] Tester avec une copie partiellement correcte
- [ ] Tester avec une copie illisible (vérifier la gestion d'erreur)
- [ ] Tester avec une copie d'un autre exercice (vérifier la détection)

---

### 2.4 Personnalisation Adaptative

#### Test 2.4.1 : Activation de la Personnalisation

**Étapes :**
1. Dans la sidebar, cocher "Activer la personnalisation adaptative"
2. Compléter quelques exercices avec feedback
3. Vérifier que le profil se met à jour

**Résultat attendu :**
- [ ] Le profil s'affiche après quelques exercices
- [ ] Les métriques sont correctes :
  - [ ] Nombre d'exercices complétés
  - [ ] Score moyen
  - [ ] Difficulté recommandée
  - [ ] Domaines à travailler
  - [ ] Points forts

#### Test 2.4.2 : Recommandations Personnalisées

**Étapes :**
1. Compléter 3-5 exercices avec des résultats variés
2. Vérifier les recommandations :
   - Type d'exercice recommandé
   - Difficulté recommandée

**Résultat attendu :**
- [ ] Les recommandations sont cohérentes avec les performances
- [ ] Si l'élève a des difficultés, la difficulté recommandée est "facile"
- [ ] Si l'élève réussit bien, la difficulté recommandée est "moyen" ou "difficile"

#### Test 2.4.3 : Adaptation de la Difficulté

**Étapes :**
1. Compléter plusieurs exercices du même type
2. Vérifier que la difficulté recommandée change selon les performances

**Résultat attendu :**
- [ ] La difficulté s'adapte aux performances
- [ ] Les recommandations sont pertinentes

---

### 2.5 Analyse d'Exemples d'Exercices (Optionnel)

#### Test 2.5.1 : Upload d'Exemples

**Préparation :**
- Préparer 3-10 photos d'exercices de statistiques (ou utiliser des exemples)

**Étapes :**
1. Dans la sidebar, section "Exemples d'exercices (optionnel)"
2. Uploader 3-10 images d'exercices
3. Cliquer sur "Analyser les exemples"
4. Attendre l'analyse (peut prendre 30-60 secondes)

**Résultat attendu :**
- [ ] Message de validation si les exemples sont valides
- [ ] Message d'erreur si les exemples ne sont pas valides
- [ ] Si valides, un badge "✨ Inspiré de tes exemples" apparaît lors de la génération

#### Test 2.5.2 : Génération Inspirée d'Exemples

**Étapes :**
1. Après avoir analysé des exemples valides
2. Générer un nouvel exercice
3. Vérifier que l'exercice est inspiré des exemples

**Résultat attendu :**
- [ ] Badge "✨ Inspiré de tes exemples" visible
- [ ] L'exercice est similaire en style/format aux exemples
- [ ] L'exercice reste original (pas une copie exacte)

**Tests de Robustesse :**
- [ ] Tester avec 3 exemples (minimum)
- [ ] Tester avec 10 exemples (maximum)
- [ ] Tester avec des exemples non valides (vérifier la gestion d'erreur)
- [ ] Tester avec des exemples d'un autre chapitre (vérifier la détection)

---

### 2.6 Notification Email Parent

#### Test 2.6.1 : Configuration Email

**Préparation :**
- Avoir un compte email avec SMTP (Gmail recommandé)
- Créer un "App Password" pour Gmail si nécessaire

**Étapes :**
1. Dans la sidebar, section "📧 Notification Parent"
2. Entrer le prénom de l'élève
3. Entrer l'email du parent
4. Cocher "Activer les notifications email"
5. Entrer l'email expéditeur (SMTP)
6. Entrer le mot de passe SMTP (ou App Password pour Gmail)

**Résultat attendu :**
- [ ] Message "✅ Configuration email validée"
- [ ] Pas d'erreur

**Si erreur :**
- Vérifier les credentials SMTP
- Pour Gmail, utiliser un "App Password" (pas le mot de passe normal)
- Vérifier que la validation en 2 étapes est activée pour Gmail

#### Test 2.6.2 : Envoi d'Email

**Étapes :**
1. Compléter quelques exercices avec feedback
2. Après le dernier exercice, cliquer sur "📧 Envoyer rapport parent"
3. Vérifier l'envoi

**Résultat attendu :**
- [ ] Message "✅ Rapport envoyé à [email]"
- [ ] Email reçu dans la boîte mail du parent
- [ ] Email contient :
  - [ ] Prénom de l'élève
  - [ ] Chapitre travaillé
  - [ ] Nombre d'exercices
  - [ ] Taux de réussite
  - [ ] Points forts
  - [ ] Axes de progression
- [ ] Email est bien formaté (HTML)
- [ ] Email est lisible sur mobile et desktop

**Tests de Robustesse :**
- [ ] Tester avec 0 exercice (vérifier que le bouton n'apparaît pas)
- [ ] Tester avec plusieurs exercices
- [ ] Tester avec différents taux de réussite
- [ ] Vérifier le rendu sur mobile

---

## 🔄 Phase 3 : Tests d'Intégration

### 3.1 Workflow Complet

**Test :** Parcours utilisateur complet

**Étapes :**
1. Démarrer l'application
2. Configurer Gemini
3. Activer la personnalisation
4. Générer un exercice (Tableau d'effectifs)
5. Résoudre l'exercice sur papier
6. Uploader la photo
7. Analyser la copie
8. Vérifier le feedback
9. Générer un autre exercice (Calcul de fréquences)
10. Répéter le processus
11. Vérifier que le profil se met à jour
12. Envoyer le rapport parent

**Résultat attendu :**
- [ ] Toutes les étapes fonctionnent sans erreur
- [ ] Le workflow est fluide
- [ ] Les données sont cohérentes entre les étapes

---

### 3.2 Gestion des Erreurs

#### Test 3.2.1 : Erreurs de Génération

**Étapes :**
1. Simuler une erreur (déconnecter internet, clé API invalide)
2. Essayer de générer un exercice
3. Vérifier la gestion d'erreur

**Résultat attendu :**
- [ ] Message d'erreur clair affiché
- [ ] L'application ne plante pas
- [ ] Possibilité de réessayer

#### Test 3.2.2 : Erreurs d'Analyse

**Étapes :**
1. Uploader une image non valide (pas une copie, image corrompue)
2. Essayer d'analyser
3. Vérifier la gestion d'erreur

**Résultat attendu :**
- [ ] Message d'erreur clair
- [ ] Suggestion de réessayer avec une meilleure image
- [ ] L'application ne plante pas

#### Test 3.2.3 : Erreurs d'Email

**Étapes :**
1. Configurer un email invalide
2. Essayer d'envoyer un rapport
3. Vérifier la gestion d'erreur

**Résultat attendu :**
- [ ] Message d'erreur clair
- [ ] Suggestion de vérifier la configuration
- [ ] L'application ne plante pas

---

## 📊 Phase 4 : Tests de Performance

### 4.1 Temps de Réponse

**Tests :**
- [ ] Génération d'exercice : < 30 secondes
- [ ] Analyse de copie : < 60 secondes
- [ ] Analyse d'exemples : < 60 secondes
- [ ] Envoi d'email : < 10 secondes

**Si trop lent :**
- Vérifier la connexion internet
- Vérifier les quotas API Gemini
- Optimiser les images (réduire la taille)

---

### 4.2 Utilisation Mémoire

**Tests :**
- [ ] L'application ne consomme pas trop de mémoire
- [ ] Pas de fuites mémoire après plusieurs utilisations
- [ ] Les images sont bien libérées après analyse

---

## ✅ Checklist Complète de Test

### Configuration
- [ ] Application démarre sans erreur
- [ ] Clé API Gemini fonctionne
- [ ] Interface s'affiche correctement

### Génération d'Exercices
- [ ] Tableau d'effectifs : Génération fonctionne
- [ ] Calcul de fréquences : Génération fonctionne
- [ ] Moyenne pondérée : Génération fonctionne
- [ ] Problème textuel : Génération fonctionne
- [ ] Exercices variés à chaque génération
- [ ] Exercices adaptés au niveau 3ème

### Analyse de Copies
- [ ] Upload d'image fonctionne
- [ ] Analyse de copie fonctionne
- [ ] Feedback complet affiché
- [ ] Analyse de démarche étape par étape
- [ ] Points positifs identifiés
- [ ] Erreurs identifiées
- [ ] Correction détaillée fournie
- [ ] Score affiché

### Personnalisation
- [ ] Profil se met à jour
- [ ] Recommandations personnalisées
- [ ] Adaptation de la difficulté
- [ ] Statistiques correctes

### Exemples d'Exercices (Optionnel)
- [ ] Upload de 3-10 exemples fonctionne
- [ ] Analyse d'exemples fonctionne
- [ ] Validation des exemples
- [ ] Génération inspirée fonctionne

### Notification Email
- [ ] Configuration email fonctionne
- [ ] Envoi d'email fonctionne
- [ ] Email reçu et bien formaté
- [ ] Contenu de l'email correct

### Robustesse
- [ ] Gestion d'erreurs appropriée
- [ ] Pas de plantage
- [ ] Messages d'erreur clairs
- [ ] Performance acceptable

### Workflow Complet
- [ ] Parcours utilisateur complet fonctionne
- [ ] Toutes les fonctionnalités s'intègrent bien
- [ ] Données cohérentes

---

## 🐛 Problèmes Courants et Solutions

### Problème 1 : Erreur "API Key not found"
**Solution :**
- Vérifier que le fichier `.env` existe
- Vérifier que `GEMINI_API_KEY` est bien défini
- Vérifier qu'il n'y a pas d'espaces dans la clé

### Problème 2 : Génération d'exercice échoue
**Solution :**
- Vérifier la connexion internet
- Vérifier les quotas API Gemini
- Vérifier les logs dans la console
- Réessayer (peut être temporaire)

### Problème 3 : Analyse de copie échoue
**Solution :**
- Vérifier que l'image est valide
- Vérifier que l'image contient bien une copie manuscrite
- Vérifier la taille de l'image (pas trop grande)
- Réessayer avec une meilleure qualité d'image

### Problème 4 : Email non envoyé
**Solution :**
- Vérifier les credentials SMTP
- Pour Gmail, utiliser un "App Password"
- Vérifier que la validation en 2 étapes est activée
- Vérifier les logs dans la console

### Problème 5 : Application lente
**Solution :**
- Vérifier la connexion internet
- Réduire la taille des images
- Vérifier les quotas API Gemini
- Optimiser les requêtes

---

## 📝 Rapport de Test

Après avoir complété tous les tests, remplir ce rapport :

**Date de test :** _______________

**Résultats :**
- Fonctionnalités testées : ___ / ___
- Fonctionnalités fonctionnelles : ___ / ___
- Bugs trouvés : ___
- Bugs critiques : ___

**Bugs trouvés :**
1. _______________________________
2. _______________________________
3. _______________________________

**Commentaires :**
_________________________________
_________________________________

---

## 🎯 Prochaines Étapes

Après les tests :
1. [ ] Corriger les bugs trouvés
2. [ ] Retester les fonctionnalités corrigées
3. [ ] Préparer une démo pour la vidéo
4. [ ] Déployer sur AI Studio
5. [ ] Tester en production

---

*Guide de test créé le : [Date]*
*Dernière mise à jour : [Date]*


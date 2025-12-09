# 📊 Application d'Exercices de Statistiques - Niveau 3ème

Application pédagogique développée pour la compétition Kaggle **"Vibe Code with Gemini 3 Pro"**.

Cette application permet aux élèves de 3ème de s'entraîner aux statistiques avec un feedback intelligent basé sur l'analyse de copies manuscrites par Gemini 3 Pro.

> **💡 Vision du Projet** : Ce MVP (Minimum Viable Product) couvre actuellement **1 chapitre (Statistiques) × 1 niveau (3ème)**, mais l'architecture modulaire permet une expansion massive vers **tous les chapitres de mathématiques** et **tous les niveaux de la 6ème à la Terminale**, avec un potentiel d'impact sur des millions d'élèves.

## 🎯 Fonctionnalités

### Types d'exercices (générés par Gemini 3 Pro)

1. **📋 Tableaux d'effectifs**
   - À partir d'une liste de valeurs, l'élève doit remplir un tableau d'effectifs
   - Vérification de la présentation et des calculs
   - Exercices variés générés dynamiquement

2. **📈 Calcul de fréquences**
   - Calcul de fréquences sous différentes formes (décimal, fraction, pourcentage)
   - Utilisation de la formule ou du produit en croix
   - Contextes variés et réalistes

3. **🎯 Moyenne pondérée**
   - Calcul de la moyenne pondérée d'une série statistique
   - Vérification de la méthode et des calculs
   - Exercices adaptés au niveau

4. **📝 Problèmes textuels**
   - Résolution de problèmes concrets impliquant des statistiques
   - Interprétation des résultats
   - Situations variées et engageantes

### Analyse intelligente avec Gemini 3 Pro

- **Vision par ordinateur** : Analyse précise des copies manuscrites
- **Raisonnement multi-étapes** : 
  - Analyse de la démarche étape par étape
  - Identification des erreurs de raisonnement (pas seulement de calcul)
  - Compréhension de la méthode utilisée par l'élève
- **Feedback pédagogique avancé** : 
  - Identification précise des erreurs avec contexte
  - Mise en avant des bons points détaillés
  - Correction détaillée étape par étape
  - Conseils personnalisés basés sur les erreurs
  - Recommandations pour progresser
  - Évaluation qualitative ou quantitative

### Personnalisation adaptative

- **Profil de l'élève** : Suivi automatique des performances
- **Adaptation de la difficulté** : Recommandations basées sur les résultats
- **Exercices personnalisés** : Génération adaptée aux difficultés identifiées
- **Indices contextuels** : Aide ciblée selon les erreurs communes
- **Suivi de progression** : Statistiques et tendances d'évolution

### Génération basée sur des exemples

- **Upload d'exemples** : L'élève peut télécharger 3-10 photos d'exercices de son chapitre
- **Validation automatique** : Gemini vérifie que les exemples sont complets et en lien avec le chapitre
- **Analyse intelligente** : Extraction des caractéristiques communes (styles, contextes, formats)
- **Génération inspirée** : Création d'exercices similaires mais originaux basés sur les exemples
- **Adaptation pédagogique** : Les exercices générés respectent le style et le format des exemples fournis

## 🚀 Installation

### Prérequis

- Python 3.8+
- Clé API Google Gemini (obtenez-la sur [Google AI Studio](https://makersuite.google.com/app/apikey))

### Installation des dépendances

```bash
pip install -r requirements.txt
```

### Configuration

1. Créez un fichier `.env` à la racine du projet :

```env
GEMINI_API_KEY=votre_cle_api_ici
```

Ou configurez la clé directement dans l'interface de l'application.

## 💻 Utilisation

### Lancer l'application

```bash
streamlit run app.py
```

L'application s'ouvrira dans votre navigateur à l'adresse `http://localhost:8501`.

### Workflow

#### Workflow standard

1. **Choisir un exercice** : Sélectionnez le type d'exercice et le niveau de difficulté dans la barre latérale
2. **Générer** : Cliquez sur "Générer un nouvel exercice"
3. **Résoudre** : L'élève résout l'exercice sur sa feuille
4. **Photographier** : Prendre une photo de la copie
5. **Télécharger** : Uploader la photo dans l'application
6. **Analyser** : Cliquer sur "Analyser ma copie"
7. **Feedback** : Consulter le feedback détaillé avec erreurs, bons points et correction

#### Workflow avec exemples (optionnel)

1. **Télécharger des exemples** : Dans la barre latérale, téléchargez 3-10 photos d'exercices de votre chapitre
2. **Analyser les exemples** : Cliquez sur "Analyser les exemples" - Gemini vérifie leur validité
3. **Générer un exercice inspiré** : Les nouveaux exercices générés s'inspireront du style et du format de vos exemples
4. **Continuer le workflow standard** : Résoudre, photographier, analyser, obtenir le feedback

## 🏗️ Architecture

```
gemini_math_stats/
├── app.py                 # Application Streamlit principale avec personnalisation
├── gemini_client.py       # Client Gemini 3 Pro (vision + raisonnement multi-étapes)
├── exercise_generator.py  # Générateur d'exercices utilisant Gemini
├── student_profile.py     # Gestion du profil et personnalisation adaptative
├── requirements.txt       # Dépendances Python
├── test_app.py           # Script de test
└── README.md             # Documentation
```

### Modules

- **`gemini_client.py`** : 
  - Gère l'interaction avec Gemini 3 Pro
  - Analyse d'images avec vision par ordinateur
  - Raisonnement multi-étapes pour analyser la démarche
  - Génération d'exercices variés et originaux
  - Analyse et validation d'exemples d'exercices
  - Génération d'exercices inspirés des exemples
  
- **`exercise_generator.py`** : 
  - Génère les 4 types d'exercices avec Gemini 3 Pro
  - Personnalisation selon le profil de l'élève
  - Fallback vers exercices prédéfinis si nécessaire
  
- **`student_profile.py`** : 
  - Gestion du profil de l'élève
  - Analyse des performances et erreurs
  - Recommandations de difficulté et types d'exercices
  - Suivi de progression
  
- **`app.py`** : 
  - Interface utilisateur Streamlit complète
  - Intégration de la personnalisation
  - Affichage du feedback détaillé avec analyse de démarche
  - Tableau de bord de progression

## 🎓 Pédagogie

L'application suit une approche pédagogique progressive :

- **Feedback constructif** : Mise en avant des réussites avant les erreurs
- **Correction détaillée** : Explications étape par étape pour comprendre les erreurs
- **Adaptation** : Niveaux de difficulté ajustables
- **Autonomie** : L'élève peut s'entraîner seul avec un feedback immédiat

## 🔧 Technologies utilisées

- **Streamlit** : Interface utilisateur web
- **Google Gemini 3 Pro** : Vision par ordinateur et raisonnement mathématique
- **Pillow (PIL)** : Traitement d'images
- **Python** : Langage de développement

## 📝 Compétition Kaggle

Ce projet participe à la compétition **"Vibe Code with Gemini 3 Pro"** et exploite pleinement les capacités du modèle :

### Utilisation avancée de Gemini 3 Pro

- ✅ **Vision par ordinateur** : Analyse précise de copies manuscrites mathématiques
- ✅ **Raisonnement multi-étapes** : Analyse de la démarche étape par étape
- ✅ **Génération de contenu** : Création d'exercices variés et originaux
- ✅ **Raisonnement mathématique** : Correction intelligente avec compréhension du contexte
- ✅ **Personnalisation** : Adaptation du contenu selon le profil de l'élève
- ✅ **Feedback constructif** : Conseils personnalisés et recommandations

### Innovation technique

- **Raisonnement en chaîne** : Analyse en deux étapes (extraction de démarche puis feedback détaillé)
- **Personnalisation adaptative** : Système de profil qui s'améliore avec l'usage
- **Génération dynamique** : Exercices toujours variés grâce à Gemini
- **Analyse contextuelle** : Compréhension de la méthode de l'élève, pas seulement du résultat

## ✨ Fonctionnalités implémentées

- [x] Génération d'exercices avec Gemini 3 Pro
- [x] Analyse de copies manuscrites avec vision par ordinateur
- [x] Raisonnement multi-étapes pour analyser la démarche
- [x] Personnalisation adaptative basée sur les performances
- [x] Suivi de progression et statistiques
- [x] Recommandations de difficulté et types d'exercices
- [x] Feedback détaillé avec conseils personnalisés
- [x] Interface utilisateur complète avec tableau de bord

## 🚀 Roadmap et Potentiel d'Expansion

### Phase Actuelle (MVP)
- ✅ Statistiques - Niveau 3ème
- ✅ Architecture modulaire prête pour l'expansion

### Phase 2 - Expansion Collège (6ème à 3ème)
- [ ] Tous les chapitres de mathématiques du collège
- [ ] Algèbre, Géométrie, Fonctions, Probabilités
- [ ] Adaptation automatique par niveau

### Phase 3 - Expansion Lycée (2nde à Terminale)
- [ ] Mathématiques générales (2nde, 1ère, Terminale)
- [ ] Spécialités mathématiques (Terminale)
- [ ] Préparation au Baccalauréat

### Phase 4 - Fonctionnalités Avancées
- [ ] Sauvegarde persistante des profils (base de données)
- [ ] Export des résultats en PDF
- [ ] Support de plusieurs langues
- [ ] Mode hors ligne avec modèle local
- [ ] Intégration avec systèmes de gestion d'apprentissage (LMS)
- [ ] Tableau de bord pour enseignants
- [ ] Statistiques de classe

### Impact Potentiel
- **Millions d'élèves** : Tous les élèves de 6ème à Terminale en France et pays francophones
- **Tous les chapitres** : Couverture complète du programme de mathématiques
- **Accessibilité** : Disponible 24/7, sans limite géographique
- **Personnalisation** : Adaptation à chaque élève et chaque niveau

## 📄 Licence

Ce projet est développé dans le cadre de la compétition Kaggle "Vibe Code with Gemini 3 Pro".

## 👨‍💻 Auteur

Développé pour la compétition Kaggle Gemini 3 Pro - 2025


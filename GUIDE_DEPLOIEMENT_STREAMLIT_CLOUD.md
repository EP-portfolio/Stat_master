# 🚀 Guide de Déploiement sur Streamlit Cloud

## 📋 Vue d'Ensemble

Ce guide vous permet de déployer votre application sur Streamlit Cloud pour la compétition Kaggle. C'est **rapide, gratuit et parfaitement adapté** pour Streamlit.

---

## ✅ Prérequis

- [ ] Compte GitHub
- [ ] Compte Streamlit Cloud (gratuit, se connecte avec GitHub)
- [ ] Code de l'application prêt dans un repo GitHub
- [ ] Clé API Gemini obtenue

---

## 🚀 Étapes de Déploiement

### Étape 1 : Préparer le Repo GitHub

1. **Créer un repo GitHub** (ou utiliser celui existant : `https://github.com/EP-portfolio/Stat_master`)

2. **Vérifier les fichiers nécessaires** :
   ```
   Stat_master/
   ├── app.py                    # ✅ Application principale
   ├── gemini_client.py          # ✅ Client Gemini
   ├── exercise_generator.py     # ✅ Générateur d'exercices
   ├── student_profile.py        # ✅ Profil élève
   ├── email_notifier.py         # ✅ Notifications email
   ├── requirements.txt          # ✅ Dépendances
   └── README.md                 # ✅ Documentation (optionnel)
   ```

3. **Vérifier `requirements.txt`** :
   ```txt
   streamlit>=1.28.0
   google-generativeai>=0.3.0
   Pillow>=10.0.0
   python-dotenv>=1.0.0
   pandas>=2.0.0
   numpy>=1.24.0
   ```

4. **Pousser le code sur GitHub** :
   ```bash
   git add .
   git commit -m "Application prête pour Streamlit Cloud"
   git push origin main
   ```

---

### Étape 2 : Créer un Compte Streamlit Cloud

1. Aller sur **https://share.streamlit.io**
2. Cliquer sur **"Sign in"** ou **"Se connecter"**
3. Se connecter avec votre compte **GitHub**
4. Autoriser Streamlit Cloud à accéder à vos repos GitHub

---

### Étape 3 : Déployer l'Application

1. **Dans Streamlit Cloud**, cliquer sur **"New app"** ou **"Nouvelle app"**

2. **Configurer le déploiement** :
   - **Repository** : Sélectionner `EP-portfolio/Stat_master`
   - **Branch** : `main` (ou la branche principale)
   - **Main file path** : `app.py`
   - **App URL** : Choisir un nom (ex: `stat-master-3eme`)

3. **Cliquer sur "Deploy"** ou **"Déployer"**

4. **Attendre le déploiement** (2-3 minutes)

---

### Étape 4 : Configurer les Variables d'Environnement

1. **Dans Streamlit Cloud**, aller dans **"Settings"** (⚙️) de votre app

2. **Aller dans "Secrets"**

3. **Ajouter les secrets** (format TOML) :
   ```toml
   GEMINI_API_KEY = "votre_cle_api_gemini"
   EMAIL_SENDER = "votre_email@gmail.com"  # Optionnel
   EMAIL_PASSWORD = "votre_app_password"    # Optionnel
   ```

4. **Sauvegarder** - L'app redémarre automatiquement

---

### Étape 5 : Vérifier le Déploiement

1. **Ouvrir l'URL de l'app** (ex: `https://stat-master-3eme.streamlit.app`)

2. **Tester les fonctionnalités** :
   - [ ] L'app se charge correctement
   - [ ] La clé API Gemini fonctionne
   - [ ] Génération d'exercices fonctionne
   - [ ] Upload de photos fonctionne
   - [ ] Analyse avec Gemini fonctionne
   - [ ] Feedback s'affiche correctement

3. **Vérifier l'accessibilité publique** :
   - [ ] Ouvrir l'URL en navigation privée
   - [ ] Vérifier qu'aucun login n'est requis
   - [ ] L'app fonctionne sans authentification

---

## 🔗 Obtenir le Lien Public

Une fois déployé, votre app aura une URL du type :
```
https://stat-master-3eme.streamlit.app
```

**Ce lien est public et accessible à tous** - parfait pour Kaggle !

---

## ⚙️ Configuration Avancée

### Personnaliser l'URL

Dans les **Settings** de Streamlit Cloud :
- **App URL** : Vous pouvez changer le nom de l'URL
- **Custom domain** : Optionnel (nécessite un domaine personnalisé)

### Gérer les Versions

- **Branch** : Vous pouvez changer la branche à déployer
- **Auto-redeploy** : Activez pour redéployer automatiquement à chaque push

### Monitoring

- **Logs** : Consultez les logs dans Streamlit Cloud
- **Metrics** : Voir les statistiques d'utilisation

---

## 🐛 Résolution de Problèmes

### Problème 1 : L'app ne démarre pas

**Solutions :**
- Vérifier les logs dans Streamlit Cloud
- Vérifier que `app.py` est bien le point d'entrée
- Vérifier que toutes les dépendances sont dans `requirements.txt`

### Problème 2 : Erreur "GEMINI_API_KEY not found"

**Solutions :**
- Vérifier que les secrets sont bien configurés dans Streamlit Cloud
- Vérifier le format TOML des secrets
- Redémarrer l'app après avoir ajouté les secrets

### Problème 3 : Erreur d'import de modules

**Solutions :**
- Vérifier que tous les fichiers Python sont dans le repo
- Vérifier que les imports sont corrects
- Vérifier que `requirements.txt` contient toutes les dépendances

### Problème 4 : L'app est lente

**Solutions :**
- Vérifier les logs pour identifier les goulots d'étranglement
- Optimiser les appels à Gemini (cache si possible)
- Réduire la taille des images uploadées

---

## ✅ Checklist Finale

Avant de soumettre à Kaggle :

- [ ] App déployée sur Streamlit Cloud
- [ ] URL publique obtenue
- [ ] App accessible sans login
- [ ] Toutes les fonctionnalités testées
- [ ] Clé API Gemini configurée
- [ ] App fonctionne correctement
- [ ] Lien prêt pour le Writeup Kaggle

---

## 📝 Pour le Writeup Kaggle

Dans votre Writeup, mentionnez :

```
**Application Interactive :** [Lien Streamlit Cloud]

L'application est déployée sur Streamlit Cloud et accessible publiquement.
Lien : https://stat-master-3eme.streamlit.app
```

---

## 🎯 Avantages de Streamlit Cloud

- ✅ **Gratuit** : Déploiement gratuit pour les projets publics
- ✅ **Rapide** : Déploiement en 2-3 minutes
- ✅ **Automatique** : Redéploiement automatique à chaque push
- ✅ **Public** : Lien public sans authentification
- ✅ **Fiable** : Infrastructure gérée par Streamlit
- ✅ **Parfait pour Kaggle** : Répond à toutes les exigences

---

**Bonne chance pour la compétition ! 🚀**


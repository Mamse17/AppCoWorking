# Espace de Co-Working d’Île de France

Une application Streamlit interactive pour découvrir et rechercher les espaces de coworking en Île-de-France.

---

## 🚀 Fonctionnalités principales

1. **Scraping & géocodage**  
   - Récupération automatique des informations (nom, adresse, téléphone, accès, liens) depuis la page LePortageSalarial  
   - Nettoyage du texte et des numéros de téléphone  
   - Géocodage des adresses (latitude / longitude) via l’API OpenCage  

2. **Recherche en direct**  
   - Barre de recherche en haut de la page  
   - Filtre instantané par nom, adresse, ligne de transport ou téléphone  

3. **Visualisation**  
   - **Liste** des espaces (6 premières colonnes du CSV) dans une section extensible  
   - **Carte interactive** Folium centrée sur Paris avec marqueurs pour chaque espace  
   - **Diagramme en barres** matplotlib du nombre d’espaces accessibles par ligne de métro (1–14) et RER (A–H)  

4. **Téléchargement du code**  
   - Bouton pour télécharger le script Python complet  

---

## 📦 Prérequis

- Python ≥ 3.8  
- Clé API OpenCage (ici codée en dur : `1a641532f42e4521ab7a948d109443bb`)  
- Connexion Internet (scraping + géocodage)

---

## 🔧 Installation

1. **Cloner le dépôt**  
   ```bash
   git clone https://github.com/tonPseudo/ton-repo.git
   cd ton-repo

2. **Créer et activer l’environnement virtuel**
   python -m venv librairie
   # Windows
   librairie\Scripts\activate
   # macOS / Linux
   source librairie/bin/activate

3. **Installer les dépendances**
   pip install -r requirements.txt

4. **Ajouter (ou modifier) votre clé OpenCage**
   Ici l'exposition de la clé API n'est pas sensible du fait qu'elle soit lié à un compte non critique et free

   - Si vous préférez ne pas garder la clé en dur, exportez-la en variable d’environnement, puis dans le code remplacez : 
      locator = OpenCage(api_key="VOTRE_CLE_ICI")

   par : 
      import os
      locator = OpenCage(api_key=os.getenv("OPENCAGE_API_KEY"))

   et exportez avant de lancer : 
      export OPENCAGE_API_KEY="1a641532f42e4521ab7a948d109443bb"

## ▶️ Lancer l’application

   - streamlit run app_streamlit.py

## 📁 Structure du projet

   - .
      ├── app_streamlit.py       # Script principal Streamlit
      ├── requirements.txt       # Dépendances Python
      ├── .gitignore             # Exclusions Git (env, caches, csv…)
      └── README.md              # Documentation (ce fichier)





<p align="center"> Made with ❤️ by Kondian Traoré </p> ```






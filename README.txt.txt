Espace de Co-Working d’Île de France
===================================

Description
-----------
Ce script Streamlit permet de :
1. Récupérer les données des espaces de co-working en Île-de-France via scraping du site https://www.leportagesalarial.com/coworking/
2. Nettoyer et normaliser les textes (adresses, téléphones, etc.).
3. Géocoder chaque adresse pour obtenir latitude et longitude.
4. Afficher dans l’application Streamlit :
   - Une liste des espaces (6 premières colonnes du CSV).
   - Une carte interactive Folium centrée sur Paris, avec marqueurs pour chaque espace.
   - Un diagramme en barres (matplotlib) montrant le nombre d’espaces accessibles par ligne de métro et RER.

Fichiers générés
----------------
- coworking_data_pandas.csv  
- fichier_nettoye.csv  
- fichier_nettoye_geocoded.csv  
- fichier2_nettoye.csv  

Prérequis
---------
- Python 3.7 ou supérieur  
- Accès internet pour le scraping et le géocodage  

Installation
------------
1. Créez et activez un environnement virtuel (par exemple env_streamlit) :  
python -m venv env_streamlit
env_streamlit\Scripts\activate

2. Installez les dépendances :  
pip install -r Requirements.txt

Utilisation
-----------
Lancez l’application Streamlit :  
streamlit run app.py
(Remplacez app.py par le nom de votre script si besoin.)
# Documentation technique – Application **“Espace de Co-Working d’Île-de-France”**

---

## 1. Vue d’ensemble
Cette application **Streamlit** :

1. **Scrape** la page *LePortageSalarial.com/coworking/* pour récupérer les espaces de coworking en Île-de-France ;  
2. **Nettoie** et normalise les données (texte ASCII, numéros de téléphone) ;  
3. **Géocode** chaque adresse via l’API **OpenCage** (lat / lon) ;  
4. Met les résultats en **cache** grâce à `@st.cache_data`, afin de ne pas refaire les étapes lourdes à chaque interaction ;  
5. Propose à l’utilisateur :  
   * une **barre de recherche** temps réel ;  
   * un **tableau** synthétique des espaces ;  
   * une **carte interactive** Folium ;  
   * un **diagramme en barres** des lignes de métro / RER ;  
   * un **bouton** pour télécharger le script complet.  

---

## 2. Dépendances

| Bibliothèque                    | Rôle                                   | Fonctions / objets utilisés |
|---------------------------------|----------------------------------------|------------------------------|
| `pandas`                        | Manipulation tabulaire                 | `DataFrame`, filtrage        |
| `pyquery`                       | Scraping HTML façon jQuery             | Sélecteurs CSS (`.find()`)   |
| `requests`                      | Requêtes HTTP                          | `get()`                      |
| `re`, `unicodedata`             | Nettoyage texte                        | Regex, normalisation ASCII   |
| `streamlit`                     | Interface web réactive                | Widgets, `@st.cache_data`    |
| `folium`, `streamlit-folium`    | Cartographie                           | `folium.Map`, `Marker`, `folium_static` |
| `geopy`                         | Géocodage                              | `OpenCage`, `RateLimiter`    |
| `matplotlib`                    | Visualisation                          | `plt.subplots`, `ax.bar`     |

---

## 3. Parcours détaillé du code

### 3.1  En-tête Streamlit
```python
st.title("Espace de Co-Working d'Île de France")
st.subheader('~ by Kondian Traore ~')
Affiche le titre et le sous-titre de l’application.

3.2 Fonction load_and_prepare_data() (mise en cache)
python
Copier
Modifier
@st.cache_data(show_spinner=True)
def load_and_prepare_data():
    ...
    return df2, df_map, labels, values
L’annotation @st.cache_data garantit que l’ensemble du pipeline lourd (scraping → nettoyage → géocodage → statistiques) n’est exécuté qu’au premier run ou lors d’un changement du code ; les appels suivants récupèrent directement les objets mis en mémoire/disque.

Étape	Détails	Choix / justification
1. Scraping	- Requête HTTP sur la page principale.
- Sélection du bloc <ul> suivant le <h3> cible.
- Récupération des liens puis parsing de chaque page pour extraire nom / adresse / téléphone / accès / liens.	PyQuery permet des sélecteurs CSS concis, proches de jQuery.
2. Nettoyage initial	- Conversion DataFrame → chaînes.
- net_txt : normalise en ASCII, supprime les espaces multiples.
- net_tel : standardise les numéros FR (regex + regroupement “XX XX …”).	Uniformiser les données avant géocodage.
3. Géocodage	```python	
locator = OpenCage(api_key="...")		
geocode = RateLimiter(locator.geocode, min_delay_seconds=1)		
df['loc'] = df['adresse'].apply(lambda a: geocode(a, language="fr"))		

markdown
Copier
Modifier
Extraction `latitude` / `longitude`, puis suppression de la colonne temporaire. | - OpenCage = service fiable + clé API.<br>- `RateLimiter` : respecte 1 req/s → pas de blocage. |
| 4. **Nettoyage secondaire** | Re-application de `net_txt` & `net_tel` sur le DF géocodé. | Supprime les artefacts ajoutés lors du géocodage. |
| 5. **Statistiques transport** | Compte, pour chaque ligne *Accès* :<br>• chiffres `1-14` → métro ;<br>• lettres isolées `A-H` → RER.<br>Met en forme `labels` & `values` pour le graphique. | Prépare la visualisation “desserte transport”. |
```
---

### 3.3  Chargement des données

```python
df_search, df2, labels, values = load_and_prepare_data()
df_search : version complète (recherche + tableau)

df2 : lignes avec coordonnées valides (carte)

labels, values : données du diagramme.
```
### 3.4 Recherche temps réel
python
Copier
Modifier
query = st.text_input("🔎 Rechercher un espace de co-working")
mask = (
    df_search['nom'].str.contains(query, case=False, na=False) |
    df_search['adresse'].str.contains(query, case=False, na=False) |
    df_search['Accès'].str.contains(query, case=False, na=False) |
    df_search['téléphone'].str.contains(query, case=False, na=False)
)
Filtre sur quatre colonnes ; résultat affiché en markdown (nom, adresse, etc.).

### .5 Sections dépliables (st.expander)
Expander	Contenu	Code résumé
📋 Liste	Affiche les 6 premières colonnes du DataFrame.	st.write(df_search.iloc[:, :6])
🗺️ Carte	Folium centrée sur Paris, marqueurs sur chaque (lat, lon).	folium.Map, boucle Marker
📊 Diagramme	Histogramme du nombre d’espaces par ligne métro / RER.	ax.bar(labels, values)
⬇️ Script	Bouton pour télécharger le fichier Python courant.	st.download_button

### 4. Choix techniques & bonnes pratiques
Cache Streamlit : évite de refaire le scraping et le géocodage (longs).

RateLimiter : protège l’API OpenCage et respecte le quota.

Normalisation ASCII : empêche les soucis d’encodage CSV / affichage.

Expander : interface épurée, chaque section se charge à la demande.

Téléchargement du script : favorise la transparence et la réutilisation.

### 5. Pistes d’amélioration
Ajouter ttl=86400 au cache pour rafraîchir les données une fois par jour.

Sauvegarder le CSV issu du scraping pour disposer d’un fallback hors-ligne.

Externaliser la clé OpenCage dans une variable d’environnement.

Mettre en place une CI/CD : GitHub → Streamlit Cloud auto-deploy.

Ajouter des filtres (département, prix, services) pour affiner la recherche.

### 6. Schéma global
mermaid
Copier
Modifier
flowchart LR
    A[Scraping] --> B[Nettoyage 1]
    B --> C[Géocodage OpenCage]
    C --> D[Nettoyage 2]
    D --> E[DataFrame final]
    E --> F[Recherche]
    E --> T[Tableau 📋]
    E --> M[Carte 🗺️]
    E --> G[Diagramme 📊]




<p align="center">Made with ❤️ by Kondian Traoré</p> ```
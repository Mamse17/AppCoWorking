import pandas as pd
from pyquery import PyQuery as pq
import requests
import re
import unicodedata
import streamlit as st
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import matplotlib.pyplot as plt

st.title("Espace de Co-Working d'Île de France")
st.subheader('~ by Kondian Traore ~')

@st.cache_data(show_spinner=True)
def load_and_prepare_data():
    # 1. Scraping
    website_response = requests.get("https://www.leportagesalarial.com/coworking/")
    urls = []
    data_list = []
    if website_response.status_code == 200:
        html = pq(website_response.text)
        ul = html('h3:contains("Coworking Paris – Île de France :") + ul')
        for li in ul.find('li').items():
            a = li.find('a')
            if a:
                urls.append(a.attr('href'))
    for url in urls:
        resp = requests.get(url)
        entry = {}
        if resp.status_code == 200:
            page = pq(resp.text)
            name = page('h2:contains("Contacter")').text().replace("Contacter", "").strip()
            entry['nom'] = name
            for li in page('h2:contains("Contacter") + ul').find('li').items():
                txt = li.text()
                a = li.find('a')
                if "Adresse :" in txt:
                    entry['adresse'] = txt.replace("Adresse :", "").strip()
                elif "Téléphone :" in txt:
                    entry['téléphone'] = txt.replace("Téléphone :", "").strip()
                elif "Accès :" in txt:
                    entry['Accès'] = txt.replace("Accès :", "").strip()
                elif "Site :" in txt and a:
                    entry['Site'] = a.attr('href')
                elif "Instagram :" in txt and a:
                    entry['Instagram'] = a.attr('href')
        data_list.append(entry)

    # 2. Nettoyage initial
    df = pd.DataFrame(data_list).fillna("NULL").astype(str)
    def net_txt(t):
        t = unicodedata.normalize('NFKD', t).encode('ascii','ignore').decode('ascii')
        return re.sub(r'\s+',' ', t.strip())
    for col in df.columns:
        df[col] = df[col].apply(net_txt)
    def net_tel(t):
        t = t.split(',')[0].strip()
        m = re.search(r'\b(0[1-9](?:[ .-]?\d{2}){4}|0[1-9]\d{8})\b', t)
        if m:
            num = re.sub(r'\D','', m.group(0))
            return ' '.join(num[i:i+2] for i in range(0,len(num),2))
        return "NULL"
    if "téléphone" in df.columns:
        df["téléphone"] = df["téléphone"].apply(net_tel)

    # 3. Géocodage
    from geopy.geocoders import OpenCage

# Initialisation du géocodeur OpenCage
    locator = OpenCage(api_key="1a641532f42e4521ab7a948d109443bb")
# On limite à 1 requête/sec pour ne pas dépasser le quota
    geocode = RateLimiter(locator.geocode, min_delay_seconds=1)

# Géocodage avec OpenCage
    df['loc'] = df['adresse'].apply(lambda a: geocode(a, language="fr"))
    df['latitude'] = df['loc'].apply(lambda x: x.latitude if x else None)
    df['longitude'] = df['loc'].apply(lambda x: x.longitude if x else None)
    df.drop(columns=['loc'], inplace=True)


    # 4. Nettoyage secondaire
    df2 = df.fillna("NULL").astype(str)
    for col in df2.columns:
        df2[col] = df2[col].apply(net_txt)
    if "téléphone" in df2.columns:
        df2["téléphone"] = df2["téléphone"].apply(net_tel)

    # 5. Préparation diagramme
    df_map = df2.dropna(subset=['latitude','longitude'])
    metro = [f"ligne {i}" for i in range(1,15)]
    rer   = [f"RER {c}"  for c in list("ABCDEFGH")]
    keys  = metro + rer
    cnts  = {k:0 for k in keys}
    for a in df_map['Accès'].fillna(""):
        low = a.lower()
        for n in re.findall(r'\b([1-9]|1[0-4])\b', low):
            cnts[f"ligne {n}"] += 1
        for l in re.findall(r'\b([a-h])\b', low):
            cnts[f"RER {l.upper()}"] += 1
    labels = [f"ligne {lbl.split()[1]}" if lbl in ["RER F","RER G","RER H"] else lbl for lbl in keys]
    values = [cnts[k] for k in keys]

    return df2, df_map, labels, values

# Chargement mis en cache
df_search, df2, labels, values = load_and_prepare_data()

# Barre de recherche
query = st.text_input("🔎 Rechercher un espace de co-working")
if query:
    mask = (
        df_search['nom'].str.contains(query, case=False, na=False) |
        df_search['adresse'].str.contains(query, case=False, na=False) |
        df_search['Accès'].str.contains(query, case=False, na=False) |
        df_search['téléphone'].str.contains(query, case=False, na=False)
    )
    filt = df_search[mask]

    if not filt.empty:
        st.markdown("### Résultats de la recherche")
        for _, row in filt.iterrows():
            st.write(f"**Nom** : {row['nom']}")
            st.write(f"**Adresse** : {row['adresse']}")
            st.write(f"**Téléphone** : {row['téléphone']}")
            st.write(f"**Accès** : {row['Accès']}")
            st.write(f"**Site** : {row.get('Site','')}")
            st.write(f"**Instagram** : {row.get('Instagram','')}")
            st.markdown("---")
    else:
        st.info("Aucun espace trouvé pour votre recherche.")


# Sections dépliables
with st.expander("📋 Liste des espaces de Co-working"):
    st.write(df_search.iloc[:, :6])

with st.expander("🗺️ Carte des espaces de Co-working"):
    m = folium.Map(location=[48.8566, 2.3522], zoom_start=12)
    for _, row in df2.iterrows():
        try:
            lat = float(row['latitude'])
            lon = float(row['longitude'])
            folium.Marker([lat, lon], popup=row.get('nom', '')).add_to(m)
        except (ValueError, TypeError):
            continue  # Ignore les lignes avec coordonnées invalides
    folium_static(m)


with st.expander("📊 Diagramme d'accès par ligne"):
    fig, ax = plt.subplots(figsize=(12,6))
    ax.bar(labels, values)
    ax.set_xlabel("Lignes de métro / RER")
    ax.set_ylabel("Nombre d'espaces de co-working")
    ax.set_title("Nombre d'espaces de co-working accessibles par ligne")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)

with st.expander("⬇️ Télécharger le script complet"):
    with open(__file__, 'r', encoding='utf-8') as f:
        script = f.read()
    st.download_button("Télécharger le code Python", script, "app_streamlit.py", "text/plain")

````md
# 🇸🇳 Observatoire du Sénégal — Suivi collaboratif des prix des denrées(BETA)

Une plateforme **open-source** de **crowdsourcing** pour collecter, vérifier et visualiser les prix des denrées alimentaires au Sénégal (🍚 riz, 🛢️ huile, 🧅 oignon, etc.).

---

## ❗ Problème
Les prix varient fortement selon les zones et les périodes, mais l'information est souvent :
- **dispersée** (bouche-à-oreille, réseaux sociaux)
- **peu fiable** (absence de source/horodatage)
- **difficile à comparer** (formats différents, manque d'historique)

---

## ✅ Solution
**Observatoire du Sénégal** centralise des prix remontés par la communauté, pour permettre :
- 🧾 **Collecte simple** des prix par marché et produit
- 🕒 **Historique** et suivi des tendances
- 📊 **Visualisation** claire (tableaux, courbes)
- 🧠 **Décisions informées** pour citoyens, journalistes, ONG et décideurs

---

## 🧱 Stack Technique
- ⚡ **API** : FastAPI
- 🗄️ **Base de données** : PostgreSQL
- 📈 **Dashboard** : Streamlit

---

## ✅ Prérequis
- 🐍 **Python 3.10+**
- 🗄️ **PostgreSQL** (local ou remote)
- 🌿 **git**

---

## 🚀 Démarrage rapide (Installation)

### 1) Cloner le projet
```bash
git clone https://github.com/flowerpower584/Premiere-projet.git
cd Premiere-projet
````

### 2) Créer et activer un environnement virtuel (venv)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Installer les dépendances

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4) Configurer les variables d'environnement (.env)

Crée un fichier `.env` à la racine du projet :

```env
DATABASE_URL=postgresql+psycopg2://USER:PASSWORD@HOST:PORT/DBNAME
```

Exemple (PostgreSQL local) :

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/observatoire
```

---

## ⚡ Lancer l’API (FastAPI)

Démarrage en mode développement (auto-reload) :

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Accès :

* **API** : `http://localhost:8000`
* **Docs Swagger** : `http://localhost:8000/docs`
* **Docs ReDoc** : `http://localhost:8000/redoc`

---

## 📈 Lancer le dashboard (Streamlit)

Depuis la racine du projet :

```bash
streamlit run dashboard/app.py
```

Accès :

* **Dashboard** : `http://localhost:8501`

---

## 🗂️ Structure (proposée)

```txt
.
├── api/                 # FastAPI (routes, services, models)
├── dashboard/           # Streamlit (visualisations)
├── db/                  # migrations / seeds / scripts
├── main.py
├── database.py
├── models.py
├── requirements.txt
├── README.md
└── schema_db.md
```

---

## 🤝 Contribuer

Les contributions sont les bienvenues :

* 🐛 signaler un bug (Issues)
* ✨ proposer une feature (Discussions / PR)
* 🧪 ajouter des tests
* 🧱 améliorer le schéma DB et la qualité des données

---

## 📜 Licence

À définir (MIT recommandé pour l’open-source).

---

**Conçu avec ❤️ au Sénégal par un développeur de 17 ans.**

```
```

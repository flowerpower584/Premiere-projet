# 🇸🇳 Observatoire du Sénégal — Suivi collaboratif des prix des denrées

Une plateforme **open-source** de **crowdsourcing** pour collecter, vérifier et visualiser les prix des denrées alimentaires au Sénégal (🍚 riz, 🛢️ huile, 🧅 oignon, etc.).

---

## ❗ Problème
Les prix varient fortement selon les zones et les périodes, mais l’information est souvent :
- **dispersée** (bouche-à-oreille, réseaux sociaux)
- **peu fiable** (absence de source/horodatage)
- **difficile à comparer** (formats différents, manque d’historique)

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
- 🐳 **Infra** : Docker / Docker Compose
- 📈 **Dashboard** : Streamlit

---

## 🚀 Démarrage rapide (Installation)
### Prérequis
- Docker + Docker Compose

### Lancer le projet
```bash
git clone https://github.com/flowerpower584/Premiere-projet.git
cd Premiere-projet
docker compose up --build

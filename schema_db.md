# Schéma Base de Données — Observatoire du Sénégal

Ce document décrit le schéma minimal de la base PostgreSQL pour stocker :
- les **produits** (denrées),
- les **marchés** (lieux de vente),
- les **prix** collectés dans le temps.

---

## Table: Produits

| Colonne      | Type     | Contraintes                  | Description |
|-------------|----------|------------------------------|-------------|
| id          | Integer  | PK, Auto-incrément           | Identifiant unique du produit |
| nom         | String   | NOT NULL, UNIQUE             | Nom du produit (ex: riz, huile, oignon) |
| unite       | String   | NOT NULL                     | Unité (ex: kg, litre, sac) |
| categorie   | String   | NULL                         | Catégorie (ex: céréales, huiles, légumes) |
| created_at  | DateTime | NOT NULL                     | Date de création |
| updated_at  | DateTime | NOT NULL                     | Date de mise à jour |

---

## Table: Marches

| Colonne      | Type     | Contraintes                  | Description |
|-------------|----------|------------------------------|-------------|
| id          | Integer  | PK, Auto-incrément           | Identifiant unique du marché |
| nom         | String   | NOT NULL                     | Nom du marché (ex: Sandaga, Tilène) |
| ville       | String   | NOT NULL                     | Ville (ex: Dakar, Thiès) |
| region      | String   | NOT NULL                     | Région (ex: Dakar, Thiès, Saint-Louis) |
| latitude    | Float    | NULL                         | Latitude (optionnel) |
| longitude   | Float    | NULL                         | Longitude (optionnel) |
| created_at  | DateTime | NOT NULL                     | Date de création |
| updated_at  | DateTime | NOT NULL                     | Date de mise à jour |

---

## Table: Prix

| Colonne        | Type     | Contraintes                                | Description |
|---------------|----------|--------------------------------------------|-------------|
| id            | Integer  | PK, Auto-incrément                         | Identifiant unique du prix |
| produit_id    | Integer  | NOT NULL, FK → Produits(id)                | Référence du produit |
| marche_id     | Integer  | NOT NULL, FK → Marches(id)                 | Référence du marché |
| valeur        | Float    | NOT NULL                                   | Prix observé (ex: 500.0) |
| devise        | String   | NOT NULL                                   | Devise (ex: XOF) |
| qualite       | String   | NULL                                       | Qualité/variant (ex: riz brisé, huile 5L) |
| source        | String   | NULL                                       | Source (ex: utilisateur, enquête, commerçant) |
| collecte_at   | DateTime | NOT NULL                                   | Date/heure de collecte |
| created_at    | DateTime | NOT NULL                                   | Date d’insertion |
| updated_at    | DateTime | NOT NULL                                   | Date de mise à jour |

### Relations
- **Prix.produit_id** → **Produits.id** (Many-to-One)
- **Prix.marche_id** → **Marches.id** (Many-to-One)

### Index recommandés
- Index sur `Prix(produit_id, marche_id, collecte_at)`
- Index sur `Marches(ville, region)`
- Index sur `Produits(nom)`

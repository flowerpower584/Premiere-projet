from __future__ import annotations

from typing import List, Optional
from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import engine, get_db
from models import Base, Produit, Marche, Prix

app = FastAPI(title="Observatoire du Sénégal API", version="1.0.0")


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


# --- Pydantic Models ---

# Produit
class ProduitCreate(BaseModel):
    nom: str = Field(..., min_length=1, max_length=120)
    unite: str = Field(..., min_length=1)
    categorie: Optional[str] = None

class ProduitRead(BaseModel):
    id: int
    nom: str
    unite: str
    categorie: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Marche
class MarcheCreate(BaseModel):
    nom: str = Field(..., min_length=1)
    ville: str = Field(..., min_length=1)
    region: str = Field(..., min_length=1)
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class MarcheRead(BaseModel):
    id: int
    nom: str
    ville: str
    region: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Prix
class PrixCreate(BaseModel):
    produit_id: int
    marche_id: int
    valeur: float = Field(..., gt=0)
    devise: str = Field("XOF", min_length=1)
    qualite: Optional[str] = None
    source: Optional[str] = None
    collecte_at: datetime

class PrixRead(BaseModel):
    id: int
    produit_id: int
    marche_id: int
    valeur: float
    devise: str
    qualite: Optional[str] = None
    source: Optional[str] = None
    collecte_at: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


@app.get("/")
def root() -> dict:
    return {"message": "Bienvenue sur l'API Observatoire du Sénégal 🇸🇳"}


# --- Endpoints Produits ---

@app.post("/produits/", response_model=ProduitRead, status_code=status.HTTP_201_CREATED)
def create_produit(payload: ProduitCreate, db: Session = Depends(get_db)) -> Produit:
    produit = Produit(**payload.model_dump())
    db.add(produit)
    try:
        db.commit()
        db.refresh(produit)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Un produit avec ce nom existe déjà.",
        )
    return produit

@app.get("/produits/", response_model=List[ProduitRead])
def list_produits(db: Session = Depends(get_db)) -> List[Produit]:
    return db.query(Produit).order_by(Produit.nom.asc()).all()


# --- Endpoints Marches ---

@app.post("/marches/", response_model=MarcheRead, status_code=status.HTTP_201_CREATED)
def create_marche(payload: MarcheCreate, db: Session = Depends(get_db)) -> Marche:
    marche = Marche(**payload.model_dump())
    db.add(marche)
    db.commit()
    db.refresh(marche)
    return marche

@app.get("/marches/", response_model=List[MarcheRead])
def list_marches(db: Session = Depends(get_db)) -> List[Marche]:
    return db.query(Marche).order_by(Marche.nom.asc()).all()


# --- Endpoints Prix ---

@app.post("/prix/", response_model=PrixRead, status_code=status.HTTP_201_CREATED)
def create_prix(payload: PrixCreate, db: Session = Depends(get_db)) -> Prix:
    # Check if product and market exist
    if not db.query(Produit).filter(Produit.id == payload.produit_id).first():
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    if not db.query(Marche).filter(Marche.id == payload.marche_id).first():
        raise HTTPException(status_code=404, detail="Marché non trouvé")

    prix = Prix(**payload.model_dump())
    db.add(prix)
    db.commit()
    db.refresh(prix)
    return prix

@app.get("/prix/", response_model=List[PrixRead])
def list_prix(db: Session = Depends(get_db)) -> List[Prix]:
    return db.query(Prix).order_by(Prix.collecte_at.desc()).all()

from __future__ import annotations

from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import engine, get_db
from models import Base, Produit

app = FastAPI(title="Observatoire du Sénégal API", version="1.0.0")


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


class ProduitCreate(BaseModel):
    nom: str = Field(..., min_length=1, max_length=120)
    description: Optional[str] = Field(None, max_length=10_000)


class ProduitRead(BaseModel):
    id: int
    nom: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


@app.get("/")
def root() -> dict:
    return {"message": "Bienvenue sur l'API Observatoire du Sénégal 🇸🇳"}


@app.post("/produits/", response_model=ProduitRead, status_code=status.HTTP_201_CREATED)
def create_produit(payload: ProduitCreate, db: Session = Depends(get_db)) -> Produit:
    produit = Produit(nom=payload.nom, description=payload.description)
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
    return db.query(Produit).order_by(Produit.id.asc()).all()

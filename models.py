from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Produit(Base):
    __tablename__ = "produits"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, unique=True, index=True, nullable=False)
    unite = Column(String, nullable=False)
    categorie = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    prix = relationship("Prix", back_populates="produit")


class Marche(Base):
    __tablename__ = "marches"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    ville = Column(String, nullable=False)
    region = Column(String, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    prix = relationship("Prix", back_populates="marche")


class Prix(Base):
    __tablename__ = "prix"

    id = Column(Integer, primary_key=True, index=True)
    produit_id = Column(Integer, ForeignKey("produits.id"), nullable=False)
    marche_id = Column(Integer, ForeignKey("marches.id"), nullable=False)
    valeur = Column(Float, nullable=False)
    devise = Column(String, nullable=False)
    qualite = Column(String, nullable=True)
    source = Column(String, nullable=True)
    collecte_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    produit = relationship("Produit", back_populates="prix")
    marche = relationship("Marche", back_populates="prix")

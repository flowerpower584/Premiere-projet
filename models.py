from __future__ import annotations

from datetime import datetime
from typing import Optional, List

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    CheckConstraint,
    UniqueConstraint,
    Index,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, validates


class Base(DeclarativeBase):
    pass


class Produit(Base):
    __tablename__ = "produits"
    __table_args__ = (
        UniqueConstraint("nom", name="uq_produits_nom"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nom: Mapped[str] = mapped_column(String(120), nullable=False, unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    prix: Mapped[List["Prix"]] = relationship(
        "Prix",
        back_populates="produit",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    @validates("nom")
    def validate_nom(self, key: str, value: str) -> str:
        v = (value or "").strip()
        if not v:
            raise ValueError("Le nom du produit est requis.")
        if len(v) > 120:
            raise ValueError("Le nom du produit est trop long (max 120).")
        return v

    @validates("description")
    def validate_description(self, key: str, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        v = value.strip()
        return v if v else None


class Marche(Base):
    __tablename__ = "marches"
    __table_args__ = (
        CheckConstraint(
            "(latitude IS NULL) OR (latitude >= -90 AND latitude <= 90)",
            name="ck_marches_latitude_range",
        ),
        CheckConstraint(
            "(longitude IS NULL) OR (longitude >= -180 AND longitude <= 180)",
            name="ck_marches_longitude_range",
        ),
        Index("ix_marches_ville", "ville"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nom: Mapped[str] = mapped_column(String(160), nullable=False, index=True)
    ville: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    prix: Mapped[List["Prix"]] = relationship(
        "Prix",
        back_populates="marche",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    @validates("nom")
    def validate_nom(self, key: str, value: str) -> str:
        v = (value or "").strip()
        if not v:
            raise ValueError("Le nom du marché est requis.")
        if len(v) > 160:
            raise ValueError("Le nom du marché est trop long (max 160).")
        return v

    @validates("ville")
    def validate_ville(self, key: str, value: str) -> str:
        v = (value or "").strip()
        if not v:
            raise ValueError("La ville est requise.")
        if len(v) > 120:
            raise ValueError("La ville est trop longue (max 120).")
        return v

    @validates("latitude")
    def validate_latitude(self, key: str, value: Optional[float]) -> Optional[float]:
        if value is None:
            return None
        if value < -90 or value > 90:
            raise ValueError("Latitude invalide (doit être entre -90 et 90).")
        return float(value)

    @validates("longitude")
    def validate_longitude(self, key: str, value: Optional[float]) -> Optional[float]:
        if value is None:
            return None
        if value < -180 or value > 180:
            raise ValueError("Longitude invalide (doit être entre -180 et 180).")
        return float(value)


class Prix(Base):
    __tablename__ = "prix"
    __table_args__ = (
        CheckConstraint("prix > 0", name="ck_prix_positive"),
        CheckConstraint(
            "(devise IS NULL) OR (length(devise) >= 3 AND length(devise) <= 8)",
            name="ck_prix_devise_len",
        ),
        Index("ix_prix_produit_marche_date", "produit_id", "marche_id", "date"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    produit_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("produits.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    marche_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("marches.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    prix: Mapped[float] = mapped_column(Float, nullable=False)
    devise: Mapped[str] = mapped_column(String(8), nullable=False, default="XOF")

    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)

    user_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True)
    qualite: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)

    produit: Mapped["Produit"] = relationship("Produit", back_populates="prix")
    marche: Mapped["Marche"] = relationship("Marche", back_populates="prix")

    @validates("prix")
    def validate_prix(self, key: str, value: float) -> float:
        if value is None:
            raise ValueError("Le prix est requis.")
        v = float(value)
        if v <= 0:
            raise ValueError("Le prix doit être strictement supérieur à 0.")
        return v

    @validates("devise")
    def validate_devise(self, key: str, value: str) -> str:
        v = (value or "").strip().upper()
        if not v:
            raise ValueError("La devise est requise.")
        if len(v) < 3 or len(v) > 8:
            raise ValueError("Devise invalide (3 à 8 caractères).")
        return v

    @validates("date")
    def validate_date(self, key: str, value: datetime) -> datetime:
        if value is None:
            raise ValueError("La date est requise.")
        if not isinstance(value, datetime):
            raise ValueError("La date doit être un datetime.")
        return value

    @validates("user_id")
    def validate_user_id(self, key: str, value: Optional[int]) -> Optional[int]:
        if value is None:
            return None
        v = int(value)
        if v <= 0:
            raise ValueError("user_id doit être un entier positif.")
        return v

    @validates("qualite")
    def validate_qualite(self, key: str, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        v = value.strip()
        if not v:
            return None
        if len(v) > 120:
            raise ValueError("qualite est trop long (max 120).")
        return v

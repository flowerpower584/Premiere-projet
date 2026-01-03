from sqlalchemy import Column, Integer, String
from database import Base


class Produit(Base):
    __tablename__ = "produits"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    prix = Column(Integer, nullable=False)

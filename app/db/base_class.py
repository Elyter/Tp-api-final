from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declared_attr

class CustomBase:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    # Pour permettre l'utilisation des colonnes non mappées
    __allow_unmapped__ = True

# Création de la classe Base
Base = declarative_base(cls=CustomBase)
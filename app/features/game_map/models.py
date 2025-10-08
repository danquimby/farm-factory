from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.features.building.models import Building
from app.features.storage.models import Storage


class GameMap(Base):
    __tablename__ = "game_maps"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    # имя карты
    name = Column(String, nullable=False)
    deleted = Column(Boolean, nullable=True, default=False)

    buildings = relationship(
        Building, back_populates="game_map"
    )
    storages = relationship(
        Storage, back_populates="game_map"
    )
    user = relationship("User", back_populates="game_map")

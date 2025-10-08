from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class Resource(Base):
    __tablename__ = "resources"

    # тип ресурса, игровые, промо
    type = Column(String, nullable=True, server_default="game")
    name = Column(String, nullable=False, unique=True)
    icon = Column(String, nullable=True, server_default="not presents")

    storages = relationship("Storage", back_populates="resource")

class Storage(Base):
    __tablename__ = "storages"

    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)
    value = Column(Integer, nullable=True, server_default="0")
    game_map_id = Column(Integer, ForeignKey("game_maps.id"), nullable=False)

    resource = relationship("Resource", back_populates="storages")
    game_map = relationship("GameMap", back_populates="storages")

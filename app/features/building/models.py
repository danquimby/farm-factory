from sqlalchemy import (
    Column,
    Integer,
    UniqueConstraint,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.features.structure.models import Structure


class Building(Base):
    __tablename__ = "buildings"
    __table_args__ = (  # гарантия что не будет одного и тоже обьекта в 1 точке
        UniqueConstraint("x", "y", "game_map_id", name="uq_building_x_y"),
    )
    x = Column(Integer, index=True, nullable=False)
    y = Column(Integer, index=True, nullable=False)
    level = Column(Integer, nullable=False)

    game_map_id = Column(Integer, ForeignKey("game_maps.id"), nullable=False)
    structure_id = Column(Integer, ForeignKey("structures.id"), nullable=False)

    game_map = relationship("GameMap", back_populates="buildings")
    structure = relationship(Structure, back_populates="buildings")

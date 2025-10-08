from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint

from app.core.database import Base


class BuildingResource(Base):
    __tablename__ = "building_resources"

    __table_args__ = (
        UniqueConstraint("structure_id", "resource_id", "level", name="uq_building_resource"),
    )

    structure_id = Column(Integer, ForeignKey("structures.id"), nullable=False)
    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)

    # уровень постройки
    level = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)

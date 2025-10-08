from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.core.database import Base


class Structure(Base):
    __tablename__ = "structures"

    icon = Column(String, nullable=False)
    name = Column(String, nullable=False)
    # путь до картинки на с3
    image = Column(String, nullable=False)
    w = Column(Integer, nullable=True, server_default="1")
    h = Column(Integer, nullable=True, server_default="1")
    max_level = Column(Integer, nullable=False)
    enable = Column(Boolean, nullable=False, server_default="True")


    buildings = relationship("Building", back_populates="structure")

from sqlalchemy import (
    Column,
    Integer,
    UniqueConstraint,
    String,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


# предполагаю что это будут ресурсы, или спец айтемы мб так и назвать? )
class GameItem(Base):
    __tablename__ = "game_items"

from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from app.db.database import Base

class Keyword(Base):
    __tablename__ = "keywords"

    id = Column(Integer, primary_key=True, index=True)
    term = Column(String(100), unique=True, nullable=False, index=True)
    is_active = Column(Boolean, default=True)
    last_discovered_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

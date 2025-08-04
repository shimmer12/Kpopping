from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import datetime

class Group(Base):
    __tablename__ = "groups"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    company = Column(String(100))
    debut_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
    image_url = Column(String(500))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    idols = relationship("Idol", back_populates="group")

class Idol(Base):
    __tablename__ = "idols"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    stage_name = Column(String(100))
    real_name = Column(String(100))
    group_id = Column(Integer, ForeignKey("groups.id"))
    company = Column(String(100))
    gender = Column(String(10))  # male, female, co-ed
    position = Column(String(100))  # main vocal, lead dancer, etc.
    birth_date = Column(DateTime)
    nationality = Column(String(50))
    is_soloist = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    image_url = Column(String(500))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    group = relationship("Group", back_populates="idols")
    rankings = relationship("Ranking", back_populates="idol")
    metrics = relationship("Metric", back_populates="idol")
    trends = relationship("Trend", back_populates="idol")
    trend_data = relationship("TrendData", back_populates="idol")

class Ranking(Base):
    __tablename__ = "rankings"
    
    id = Column(Integer, primary_key=True, index=True)
    idol_id = Column(Integer, ForeignKey("idols.id"), nullable=False)
    category = Column(String(50), nullable=False)  # overall, music, social, brand, etc.
    rank = Column(Integer, nullable=False)
    score = Column(Float, nullable=False)
    total_score = Column(Float)
    music_score = Column(Float)
    social_score = Column(Float)
    brand_score = Column(Float)
    search_score = Column(Float)
    award_score = Column(Float)
    date = Column(DateTime, default=func.now(), nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    idol = relationship("Idol", back_populates="rankings")

class TrendData(Base):
    __tablename__ = "trend_data"
    
    id = Column(Integer, primary_key=True, index=True)
    idol_id = Column(Integer, ForeignKey("idols.id"), nullable=False)
    category = Column(String(50), nullable=False)  # music, social, streaming, etc.
    score = Column(Float, nullable=False)
    rank = Column(Integer)
    date = Column(DateTime, default=func.now(), nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    idol = relationship("Idol", back_populates="trend_data")

class Metric(Base):
    __tablename__ = "metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    idol_id = Column(Integer, ForeignKey("idols.id"), nullable=False)
    metric_type = Column(String(50), nullable=False)  # spotify_streams, youtube_views, instagram_followers, etc.
    value = Column(Float, nullable=False)
    date = Column(DateTime, default=func.now(), nullable=False)
    source = Column(String(100))  # api, scraping, manual
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    idol = relationship("Idol", back_populates="metrics")

class Trend(Base):
    __tablename__ = "trends"
    
    id = Column(Integer, primary_key=True, index=True)
    idol_id = Column(Integer, ForeignKey("idols.id"), nullable=False)
    trend_type = Column(String(50), nullable=False)  # ranking, followers, streams, etc.
    value = Column(Float, nullable=False)
    change = Column(Float)  # change from previous period
    date = Column(DateTime, default=func.now(), nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    idol = relationship("Idol", back_populates="trends")

class DataSource(Base):
    __tablename__ = "data_sources"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)  # api, scraping, manual
    url = Column(String(500))
    api_key = Column(String(200))
    is_active = Column(Boolean, default=True)
    last_updated = Column(DateTime)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class PlatformConfig(Base):
    __tablename__ = "platform_config"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, nullable=False)
    value = Column(Text)
    description = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now()) 
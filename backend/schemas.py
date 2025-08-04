from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# Group schemas
class GroupBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    company: Optional[str] = Field(None, max_length=100)
    debut_date: Optional[datetime] = None
    is_active: bool = True
    image_url: Optional[str] = Field(None, max_length=500)

class GroupCreate(GroupBase):
    pass

class GroupUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    company: Optional[str] = Field(None, max_length=100)
    debut_date: Optional[datetime] = None
    is_active: Optional[bool] = None
    image_url: Optional[str] = Field(None, max_length=500)

class GroupResponse(GroupBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
class GroupNested(BaseModel):
    id: int
    name: str
    company: Optional[str]
    debut_date: Optional[datetime]
    is_active: bool
    image_url: Optional[str]

    class Config:
        from_attributes = True

# Base schemas
class IdolBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    stage_name: Optional[str] = Field(None, max_length=100)
    real_name: Optional[str] = Field(None, max_length=100)
    group_id: Optional[int] = None
    company: Optional[str] = Field(None, max_length=100)
    gender: Optional[str] = Field(None, max_length=10)
    position: Optional[str] = Field(None, max_length=100)
    birth_date: Optional[datetime] = None
    nationality: Optional[str] = Field(None, max_length=50)
    is_soloist: bool = False
    is_active: bool = True
    image_url: Optional[str] = Field(None, max_length=500)

class IdolCreate(IdolBase):
    pass

class IdolUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    stage_name: Optional[str] = Field(None, max_length=100)
    real_name: Optional[str] = Field(None, max_length=100)
    group_id: Optional[int] = None
    company: Optional[str] = Field(None, max_length=100)
    gender: Optional[str] = Field(None, max_length=10)
    position: Optional[str] = Field(None, max_length=100)
    birth_date: Optional[datetime] = None
    nationality: Optional[str] = Field(None, max_length=50)
    is_soloist: Optional[bool] = None
    is_active: Optional[bool] = None
    image_url: Optional[str] = Field(None, max_length=500)

class IdolResponse(IdolBase):
    id: int
    group: Optional[GroupNested] = None  # ✅ use nested version here
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Ranking schemas
class RankingBase(BaseModel):
    category: str = Field(..., max_length=50)
    rank: int = Field(..., ge=1)
    score: float = Field(..., ge=0, le=100)
    total_score: Optional[float] = Field(None, ge=0, le=100)
    music_score: Optional[float] = Field(None, ge=0, le=100)
    social_score: Optional[float] = Field(None, ge=0, le=100)
    brand_score: Optional[float] = Field(None, ge=0, le=100)
    search_score: Optional[float] = Field(None, ge=0, le=100)
    award_score: Optional[float] = Field(None, ge=0, le=100)

class RankingCreate(RankingBase):
    idol_id: int

class RankingResponse(RankingBase):
    id: int
    idol_id: int
    date: datetime
    created_at: datetime
    idol: IdolResponse
    
    class Config:
        from_attributes = True

# TrendData schemas
class TrendDataBase(BaseModel):
    category: str = Field(..., max_length=50)
    score: float = Field(..., ge=0, le=100)
    rank: Optional[int] = Field(None, ge=1)

class TrendDataCreate(TrendDataBase):
    idol_id: int

class TrendDataResponse(TrendDataBase):
    id: int
    idol_id: int
    date: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True

# Metric schemas
class MetricBase(BaseModel):
    metric_type: str = Field(..., max_length=50)
    value: float = Field(..., ge=0)
    source: Optional[str] = Field(None, max_length=100)

class MetricCreate(MetricBase):
    idol_id: int

class MetricResponse(MetricBase):
    id: int
    idol_id: int
    date: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True

# Trend schemas
class TrendBase(BaseModel):
    trend_type: str = Field(..., max_length=50)
    value: float = Field(..., ge=0)
    change: Optional[float] = None

class TrendCreate(TrendBase):
    idol_id: int

class TrendResponse(TrendBase):
    id: int
    idol_id: int
    date: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True

# Comparison schemas
class ComparisonResponse(BaseModel):
    idol1: IdolResponse
    idol2: IdolResponse
    comparison_data: Dict[str, Any]
    
    class Config:
        from_attributes = True

# Platform stats schemas
class PlatformStats(BaseModel):
    total_idols: int
    total_groups: int
    total_soloists: int
    last_updated: datetime
    data_sources_count: int
    active_rankings_count: int

# Data source schemas
class DataSourceBase(BaseModel):
    name: str = Field(..., max_length=100)
    type: str = Field(..., max_length=50)
    url: Optional[str] = Field(None, max_length=500)
    is_active: bool = True

class DataSourceCreate(DataSourceBase):
    api_key: Optional[str] = Field(None, max_length=200)

class DataSourceResponse(DataSourceBase):
    id: int
    last_updated: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Configuration schemas
class ConfigBase(BaseModel):
    key: str = Field(..., max_length=100)
    value: Optional[str] = None
    description: Optional[str] = None

class ConfigCreate(ConfigBase):
    pass

class ConfigResponse(ConfigBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True 
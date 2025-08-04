from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn

from database import get_db, engine
from models import Base
from schemas import IdolResponse, RankingResponse, ComparisonResponse
from services.ranking_service import RankingService
from services.data_collector import DataCollectorService

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="K-Pop Ranking Platform API",
    description="Unified platform for K-Pop idol and group rankings",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
ranking_service = RankingService()
data_collector = DataCollectorService()

@app.get("/")
async def root():
    return {"message": "K-Pop Ranking Platform API", "version": "1.0.0"}

@app.get("/api/rankings", response_model=List[RankingResponse])
async def get_rankings(
    category: Optional[str] = None,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get current rankings with optional filtering"""
    try:
        rankings = ranking_service.get_current_rankings(db, category=category, limit=limit)
        return rankings
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/idols", response_model=List[IdolResponse])
async def get_idols(
    group: Optional[str] = None,
    gender: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all idols with optional filtering"""
    try:
        idols = ranking_service.get_idols(db, group=group, gender=gender)
        return idols
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/idols/{idol_id}", response_model=IdolResponse)
async def get_idol(idol_id: int, db: Session = Depends(get_db)):
    """Get specific idol details"""
    try:
        idol = ranking_service.get_idol_by_id(db, idol_id)
        if not idol:
            raise HTTPException(status_code=404, detail="Idol not found")
        return idol
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/compare/{idol1_id}/{idol2_id}", response_model=ComparisonResponse)
async def compare_idols(idol1_id: int, idol2_id: int, db: Session = Depends(get_db)):
    """Compare two idols side by side"""
    try:
        comparison = ranking_service.compare_idols(db, idol1_id, idol2_id)
        if not comparison:
            raise HTTPException(status_code=404, detail="One or both idols not found")
        return comparison
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/trends/{idol_id}")
async def get_idol_trends(idol_id: int, days: int = 30, db: Session = Depends(get_db)):
    """Get trend data for a specific idol"""
    try:
        trends = ranking_service.get_idol_trends(db, idol_id, days)
        if not trends:
            raise HTTPException(status_code=404, detail="Trend data not found")
        return trends
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/refresh-data")
async def refresh_data(db: Session = Depends(get_db)):
    """Manually trigger data refresh from all sources"""
    try:
        result = await data_collector.refresh_all_data(db)
        return {"message": "Data refresh completed", "updated_count": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
async def get_platform_stats(db: Session = Depends(get_db)):
    """Get platform statistics"""
    try:
        stats = ranking_service.get_platform_stats(db)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 
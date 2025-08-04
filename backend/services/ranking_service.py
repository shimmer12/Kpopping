from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import pandas as pd

from models import Idol, Group, Ranking, TrendData


class RankingService:
    """Service class for handling ranking-related operations"""
    
    def get_current_rankings(self, db: Session, category: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get current rankings with optional filtering"""
        query = db.query(Ranking).order_by(Ranking.rank)
        
        if category:
            query = query.filter(Ranking.category == category)
        
        if limit:
            query = query.limit(limit)
        
        rankings = query.all()
        
        result = []
        for ranking in rankings:
            idol = db.query(Idol).filter(Idol.id == ranking.idol_id).first()
            group = db.query(Group).filter(Group.id == idol.group_id).first() if idol else None
            
            result.append({
                "id": ranking.id,
                "rank": ranking.rank,
                "category": ranking.category,
                "score": ranking.score,
                "date": ranking.date.isoformat() if ranking.date else None,
                "idol": {
                    "id": idol.id,
                    "name": idol.name,
                    "stage_name": idol.stage_name,
                    "birth_date": idol.birth_date.isoformat() if idol.birth_date else None,
                    "gender": idol.gender,
                    "nationality": idol.nationality,
                    "group": {
                        "id": group.id,
                        "name": group.name,
                        "company": group.company,
                        "debut_date": group.debut_date.isoformat() if group.debut_date else None
                    } if group else None
                } if idol else None
            })
        
        return result
    
    def get_idols(self, db: Session, group: Optional[str] = None, gender: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all idols with optional filtering"""
        query = db.query(Idol)
        
        if group:
            query = query.join(Group).filter(Group.name == group)
        
        if gender:
            query = query.filter(Idol.gender == gender)
        
        idols = query.all()
        
        result = []
        for idol in idols:
            group = db.query(Group).filter(Group.id == idol.group_id).first()
            
            result.append({
                "id": idol.id,
                "name": idol.name,
                "stage_name": idol.stage_name,
                "birth_date": idol.birth_date.isoformat() if idol.birth_date else None,
                "gender": idol.gender,
                "nationality": idol.nationality,
                "group": {
                    "id": group.id,
                    "name": group.name,
                    "company": group.company,
                    "debut_date": group.debut_date.isoformat() if group.debut_date else None
                } if group else None
            })
        
        return result
    
    def get_idol_by_id(self, db: Session, idol_id: int) -> Optional[Dict[str, Any]]:
        """Get specific idol details"""
        idol = db.query(Idol).filter(Idol.id == idol_id).first()
        
        if not idol:
            return None
        
        group = db.query(Group).filter(Group.id == idol.group_id).first()
        
        return {
            "id": idol.id,
            "name": idol.name,
            "stage_name": idol.stage_name,
            "birth_date": idol.birth_date.isoformat() if idol.birth_date else None,
            "gender": idol.gender,
            "nationality": idol.nationality,
            "group": {
                "id": group.id,
                "name": group.name,
                "company": group.company,
                "debut_date": group.debut_date.isoformat() if group.debut_date else None
            } if group else None
        }
    
    def compare_idols(self, db: Session, idol1_id: int, idol2_id: int) -> Optional[Dict[str, Any]]:
        """Compare two idols side by side"""
        idol1 = db.query(Idol).filter(Idol.id == idol1_id).first()
        idol2 = db.query(Idol).filter(Idol.id == idol2_id).first()
        
        if not idol1 or not idol2:
            return None
        
        group1 = db.query(Group).filter(Group.id == idol1.group_id).first()
        group2 = db.query(Group).filter(Group.id == idol2.group_id).first()
        
        # Get current rankings for both idols
        ranking1 = db.query(Ranking).filter(Ranking.idol_id == idol1_id).order_by(desc(Ranking.date)).first()
        ranking2 = db.query(Ranking).filter(Ranking.idol_id == idol2_id).order_by(desc(Ranking.date)).first()
        
        return {
            "idol1": {
                "id": idol1.id,
                "name": idol1.name,
                "stage_name": idol1.stage_name,
                "birth_date": idol1.birth_date.isoformat() if idol1.birth_date else None,
                "gender": idol1.gender,
                "nationality": idol1.nationality,
                "group": {
                    "id": group1.id,
                    "name": group1.name,
                    "company": group1.company,
                    "debut_date": group1.debut_date.isoformat() if group1.debut_date else None
                } if group1 else None,
                "current_ranking": {
                    "rank": ranking1.rank,
                    "score": ranking1.score,
                    "category": ranking1.category,
                    "date": ranking1.date.isoformat() if ranking1.date else None
                } if ranking1 else None
            },
            "idol2": {
                "id": idol2.id,
                "name": idol2.name,
                "stage_name": idol2.stage_name,
                "birth_date": idol2.birth_date.isoformat() if idol2.birth_date else None,
                "gender": idol2.gender,
                "nationality": idol2.nationality,
                "group": {
                    "id": group2.id,
                    "name": group2.name,
                    "company": group2.company,
                    "debut_date": group2.debut_date.isoformat() if group2.debut_date else None
                } if group2 else None,
                "current_ranking": {
                    "rank": ranking2.rank,
                    "score": ranking2.score,
                    "category": ranking2.category,
                    "date": ranking2.date.isoformat() if ranking2.date else None
                } if ranking2 else None
            }
        }
    
    def get_idol_trends(self, db: Session, idol_id: int, days: int = 30) -> Optional[Dict[str, Any]]:
        """Get trend data for a specific idol"""
        idol = db.query(Idol).filter(Idol.id == idol_id).first()
        
        if not idol:
            return None
        
        # Get trend data for the specified period
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        trends = db.query(TrendData).filter(
            TrendData.idol_id == idol_id,
            TrendData.date >= start_date,
            TrendData.date <= end_date
        ).order_by(TrendData.date).all()
        
        if not trends:
            return None
        
        trend_data = []
        for trend in trends:
            trend_data.append({
                "date": trend.date.isoformat(),
                "score": trend.score,
                "rank": trend.rank,
                "category": trend.category
            })
        
        return {
            "idol_id": idol_id,
            "idol_name": idol.name,
            "period_days": days,
            "trends": trend_data
        } 
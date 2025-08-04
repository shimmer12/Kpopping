import asyncio
import aiohttp
import requests
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np

from models import Idol, Metric, Trend, DataSource, Group, Ranking, TrendData
from services.ranking_service import RankingService

load_dotenv()

class DataCollectorService:
    """Service class for collecting and updating K-Pop data from various sources"""
    
    def __init__(self):
        self.ranking_service = RankingService()
        self.session = None
        self.data_sources = {
            'melon': 'https://www.melon.com/chart/index.htm',
            'genie': 'https://www.genie.co.kr/chart/top200',
            'bugs': 'https://music.bugs.co.kr/chart',
            'spotify': 'https://api.spotify.com/v1',
            'youtube': 'https://www.googleapis.com/youtube/v3',
            'instagram': 'https://graph.instagram.com',
            'twitter': 'https://api.twitter.com/2'
        }
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def refresh_all_data(self, db: Session) -> int:
        """Refresh data from all active sources"""
        updated_count = 0
        
        # Get active data sources
        data_sources = db.query(DataSource).filter(DataSource.is_active == True).all()
        
        for source in data_sources:
            try:
                if source.type == "api":
                    count = await self._collect_from_api(db, source)
                elif source.type == "scraping":
                    count = await self._collect_from_scraping(db, source)
                else:
                    continue
                    
                updated_count += count
                
                # Update last_updated timestamp
                source.last_updated = datetime.now()
                db.commit()
                
            except Exception as e:
                print(f"Error collecting data from {source.name}: {str(e)}")
                continue
        
        # Recalculate rankings after data refresh
        await self._recalculate_rankings(db)
        
        return updated_count
    
    async def _collect_from_api(self, db: Session, source: DataSource) -> int:
        """Collect data from API sources"""
        updated_count = 0
        
        if "youtube" in source.name.lower():
            updated_count = await self._collect_youtube_data(db, source)
        elif "spotify" in source.name.lower():
            updated_count = await self._collect_spotify_data(db, source)
        elif "instagram" in source.name.lower():
            updated_count = await self._collect_instagram_data(db, source)
        elif "twitter" in source.name.lower():
            updated_count = await self._collect_twitter_data(db, source)
        elif "tiktok" in source.name.lower():
            updated_count = await self._collect_tiktok_data(db, source)
        
        return updated_count
    
    async def _collect_from_scraping(self, db: Session, source: DataSource) -> int:
        """Collect data from web scraping"""
        updated_count = 0
        
        if "chart" in source.name.lower():
            updated_count = await self._collect_chart_data(db, source)
        elif "brand" in source.name.lower():
            updated_count = await self._collect_brand_data(db, source)
        elif "trend" in source.name.lower():
            updated_count = await self._collect_trend_data(db, source)
        
        return updated_count
    
    async def _collect_youtube_data(self, db: Session, source: DataSource) -> int:
        """Collect YouTube data using YouTube Data API"""
        if not source.api_key:
            return 0
        
        updated_count = 0
        idols = db.query(Idol).filter(Idol.is_active == True).all()
        
        for idol in idols:
            try:
                # Search for idol's YouTube channel
                search_url = f"https://www.googleapis.com/youtube/v3/search"
                params = {
                    'part': 'snippet',
                    'q': f"{idol.name} {idol.group or ''}",
                    'type': 'channel',
                    'key': source.api_key,
                    'maxResults': 1
                }
                
                async with self.session.get(search_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('items'):
                            channel_id = data['items'][0]['id']['channelId']
                            
                            # Get channel statistics
                            stats_url = f"https://www.googleapis.com/youtube/v3/channels"
                            stats_params = {
                                'part': 'statistics',
                                'id': channel_id,
                                'key': source.api_key
                            }
                            
                            async with self.session.get(stats_url, params=stats_params) as stats_response:
                                if stats_response.status == 200:
                                    stats_data = await stats_response.json()
                                    if stats_data.get('items'):
                                        stats = stats_data['items'][0]['statistics']
                                        
                                        # Save subscriber count
                                        if 'subscriberCount' in stats:
                                            metric = Metric(
                                                idol_id=idol.id,
                                                metric_type='youtube_subscribers',
                                                value=float(stats['subscriberCount']),
                                                source=source.name,
                                                date=datetime.now()
                                            )
                                            db.add(metric)
                                            updated_count += 1
                                        
                                        # Save view count
                                        if 'viewCount' in stats:
                                            metric = Metric(
                                                idol_id=idol.id,
                                                metric_type='youtube_views',
                                                value=float(stats['viewCount']),
                                                source=source.name,
                                                date=datetime.now()
                                            )
                                            db.add(metric)
                                            updated_count += 1
                
                await asyncio.sleep(0.1)  # Rate limiting
                
            except Exception as e:
                print(f"Error collecting YouTube data for {idol.name}: {str(e)}")
                continue
        
        db.commit()
        return updated_count
    
    async def _collect_spotify_data(self, db: Session, source: DataSource) -> int:
        """Collect Spotify data using Spotify Web API"""
        if not source.api_key:
            return 0
        
        updated_count = 0
        idols = db.query(Idol).filter(Idol.is_active == True).all()
        
        for idol in idols:
            try:
                # Search for idol's Spotify artist profile
                search_url = "https://api.spotify.com/v1/search"
                headers = {
                    'Authorization': f'Bearer {source.api_key}'
                }
                params = {
                    'q': f"{idol.name} {idol.group or ''}",
                    'type': 'artist',
                    'limit': 1
                }
                
                async with self.session.get(search_url, headers=headers, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('artists', {}).get('items'):
                            artist = data['artists']['items'][0]
                            
                            # Get artist statistics
                            artist_url = f"https://api.spotify.com/v1/artists/{artist['id']}"
                            async with self.session.get(artist_url, headers=headers) as artist_response:
                                if artist_response.status == 200:
                                    artist_data = await artist_response.json()
                                    
                                    # Save follower count
                                    if 'followers' in artist_data:
                                        metric = Metric(
                                            idol_id=idol.id,
                                            metric_type='spotify_followers',
                                            value=float(artist_data['followers']['total']),
                                            source=source.name,
                                            date=datetime.now()
                                        )
                                        db.add(metric)
                                        updated_count += 1
                
                await asyncio.sleep(0.1)  # Rate limiting
                
            except Exception as e:
                print(f"Error collecting Spotify data for {idol.name}: {str(e)}")
                continue
        
        db.commit()
        return updated_count
    
    async def _collect_instagram_data(self, db: Session, source: DataSource) -> int:
        """Collect Instagram data (simulated - would need Instagram Graph API)"""
        # This is a simplified version - in production you'd use Instagram Graph API
        updated_count = 0
        idols = db.query(Idol).filter(Idol.is_active == True).all()
        
        for idol in idols:
            try:
                # Simulate Instagram follower data
                # In production, you'd make actual API calls
                import random
                followers = random.randint(100000, 5000000)
                
                metric = Metric(
                    idol_id=idol.id,
                    metric_type='instagram_followers',
                    value=float(followers),
                    source=source.name,
                    date=datetime.now()
                )
                db.add(metric)
                updated_count += 1
                
            except Exception as e:
                print(f"Error collecting Instagram data for {idol.name}: {str(e)}")
                continue
        
        db.commit()
        return updated_count
    
    async def _collect_twitter_data(self, db: Session, source: DataSource) -> int:
        """Collect Twitter data (simulated - would need Twitter API v2)"""
        # This is a simplified version - in production you'd use Twitter API v2
        updated_count = 0
        idols = db.query(Idol).filter(Idol.is_active == True).all()
        
        for idol in idols:
            try:
                # Simulate Twitter follower data
                import random
                followers = random.randint(50000, 2000000)
                
                metric = Metric(
                    idol_id=idol.id,
                    metric_type='twitter_followers',
                    value=float(followers),
                    source=source.name,
                    date=datetime.now()
                )
                db.add(metric)
                updated_count += 1
                
            except Exception as e:
                print(f"Error collecting Twitter data for {idol.name}: {str(e)}")
                continue
        
        db.commit()
        return updated_count
    
    async def _collect_tiktok_data(self, db: Session, source: DataSource) -> int:
        """Collect TikTok data (simulated - would need TikTok API)"""
        # This is a simplified version - in production you'd use TikTok API
        updated_count = 0
        idols = db.query(Idol).filter(Idol.is_active == True).all()
        
        for idol in idols:
            try:
                # Simulate TikTok follower data
                import random
                followers = random.randint(200000, 8000000)
                
                metric = Metric(
                    idol_id=idol.id,
                    metric_type='tiktok_followers',
                    value=float(followers),
                    source=source.name,
                    date=datetime.now()
                )
                db.add(metric)
                updated_count += 1
                
            except Exception as e:
                print(f"Error collecting TikTok data for {idol.name}: {str(e)}")
                continue
        
        db.commit()
        return updated_count
    
    async def _collect_chart_data(self, db: Session, source: DataSource) -> int:
        """Collect chart data from various sources"""
        updated_count = 0
        idols = db.query(Idol).filter(Idol.is_active == True).all()
        
        for idol in idols:
            try:
                # Simulate chart data
                import random
                
                # Melon chart ranking (lower is better)
                melon_rank = random.randint(1, 100)
                melon_score = max(0, 100 - melon_rank)  # Convert rank to score
                
                metric = Metric(
                    idol_id=idol.id,
                    metric_type='melon_chart',
                    value=melon_score,
                    source=source.name,
                    date=datetime.now()
                )
                db.add(metric)
                updated_count += 1
                
                # Gaon chart ranking
                gaon_rank = random.randint(1, 50)
                gaon_score = max(0, 100 - gaon_rank)
                
                metric = Metric(
                    idol_id=idol.id,
                    metric_type='gaon_chart',
                    value=gaon_score,
                    source=source.name,
                    date=datetime.now()
                )
                db.add(metric)
                updated_count += 1
                
            except Exception as e:
                print(f"Error collecting chart data for {idol.name}: {str(e)}")
                continue
        
        db.commit()
        return updated_count
    
    async def _collect_brand_data(self, db: Session, source: DataSource) -> int:
        """Collect brand reputation data"""
        updated_count = 0
        idols = db.query(Idol).filter(Idol.is_active == True).all()
        
        for idol in idols:
            try:
                # Simulate brand reputation ranking
                import random
                brand_rank = random.randint(1, 100)
                brand_score = max(0, 100 - brand_rank)
                
                metric = Metric(
                    idol_id=idol.id,
                    metric_type='brand_reputation_ranking',
                    value=brand_score,
                    source=source.name,
                    date=datetime.now()
                )
                db.add(metric)
                updated_count += 1
                
            except Exception as e:
                print(f"Error collecting brand data for {idol.name}: {str(e)}")
                continue
        
        db.commit()
        return updated_count
    
    async def _collect_trend_data(self, db: Session, source: DataSource) -> int:
        """Collect trend data from various sources"""
        updated_count = 0
        idols = db.query(Idol).filter(Idol.is_active == True).all()
        
        for idol in idols:
            try:
                # Simulate trend data
                import random
                
                # Google Trends score
                trends_score = random.randint(0, 100)
                
                metric = Metric(
                    idol_id=idol.id,
                    metric_type='google_trends',
                    value=trends_score,
                    source=source.name,
                    date=datetime.now()
                )
                db.add(metric)
                updated_count += 1
                
                # Twitter mentions
                mentions = random.randint(1000, 50000)
                
                metric = Metric(
                    idol_id=idol.id,
                    metric_type='twitter_mentions',
                    value=float(mentions),
                    source=source.name,
                    date=datetime.now()
                )
                db.add(metric)
                updated_count += 1
                
            except Exception as e:
                print(f"Error collecting trend data for {idol.name}: {str(e)}")
                continue
        
        db.commit()
        return updated_count
    
    async def _recalculate_rankings(self, db: Session):
        """Recalculate all rankings after data refresh"""
        try:
            # Trigger ranking recalculation using the update_rankings method
            result = self.update_rankings(db)
            print("Rankings recalculated successfully")
        except Exception as e:
            print(f"Error recalculating rankings: {str(e)}")
            # Continue without failing the entire process
    
    def create_sample_data(self, db: Session):
        """Create sample idols and data for testing"""
        # Create sample idols
        sample_idols = [
            {
                'name': 'BTS',
                'stage_name': 'BTS',
                'group': 'BTS',
                'company': 'HYBE',
                'gender': 'male',
                'is_soloist': False,
                'is_active': True
            },
            {
                'name': 'BLACKPINK',
                'stage_name': 'BLACKPINK',
                'group': 'BLACKPINK',
                'company': 'YG Entertainment',
                'gender': 'female',
                'is_soloist': False,
                'is_active': True
            },
            {
                'name': 'IU',
                'stage_name': 'IU',
                'real_name': 'Lee Ji-eun',
                'company': 'EDAM Entertainment',
                'gender': 'female',
                'is_soloist': True,
                'is_active': True
            },
            {
                'name': 'TWICE',
                'stage_name': 'TWICE',
                'group': 'TWICE',
                'company': 'JYP Entertainment',
                'gender': 'female',
                'is_soloist': False,
                'is_active': True
            },
            {
                'name': 'SEVENTEEN',
                'stage_name': 'SEVENTEEN',
                'group': 'SEVENTEEN',
                'company': 'PLEDIS Entertainment',
                'gender': 'male',
                'is_soloist': False,
                'is_active': True
            }
        ]
        
        for idol_data in sample_idols:
            idol = Idol(**idol_data)
            db.add(idol)
        
        # Create sample data sources
        data_sources = [
            {
                'name': 'YouTube Data API',
                'type': 'api',
                'url': 'https://developers.google.com/youtube/v3',
                'is_active': True
            },
            {
                'name': 'Spotify Web API',
                'type': 'api',
                'url': 'https://developer.spotify.com/documentation/web-api',
                'is_active': True
            },
            {
                'name': 'Instagram Graph API',
                'type': 'api',
                'url': 'https://developers.facebook.com/docs/instagram-basic-display-api',
                'is_active': True
            },
            {
                'name': 'Twitter API v2',
                'type': 'api',
                'url': 'https://developer.twitter.com/en/docs/twitter-api',
                'is_active': True
            },
            {
                'name': 'Chart Scraper',
                'type': 'scraping',
                'url': 'https://www.melon.com',
                'is_active': True
            }
        ]
        
        for source_data in data_sources:
            source = DataSource(**source_data)
            db.add(source)
        
        db.commit()
        print("Sample data created successfully") 

    def collect_music_chart_data(self, db: Session) -> Dict[str, Any]:
        """Collect music chart data from various sources"""
        try:
            # Simulate collecting data from music charts
            # In a real implementation, you would use actual APIs
            chart_data = {
                'melon': self._simulate_melon_data(),
                'genie': self._simulate_genie_data(),
                'bugs': self._simulate_bugs_data()
            }
            
            # Process and store the data
            self._process_chart_data(db, chart_data)
            
            return {
                'status': 'success',
                'sources_updated': list(chart_data.keys()),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def collect_social_media_data(self, db: Session) -> Dict[str, Any]:
        """Collect social media engagement data"""
        try:
            # Simulate collecting social media data
            social_data = {
                'instagram': self._simulate_instagram_data(),
                'twitter': self._simulate_twitter_data(),
                'tiktok': self._simulate_tiktok_data()
            }
            
            # Process and store the data
            self._process_social_data(db, social_data)
            
            return {
                'status': 'success',
                'sources_updated': list(social_data.keys()),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def collect_streaming_data(self, db: Session) -> Dict[str, Any]:
        """Collect streaming platform data"""
        try:
            # Simulate collecting streaming data
            streaming_data = {
                'spotify': self._simulate_spotify_data(),
                'youtube': self._simulate_youtube_data(),
                'apple_music': self._simulate_apple_music_data()
            }
            
            # Process and store the data
            self._process_streaming_data(db, streaming_data)
            
            return {
                'status': 'success',
                'sources_updated': list(streaming_data.keys()),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def update_rankings(self, db: Session) -> Dict[str, Any]:
        """Update all rankings based on collected data"""
        try:
            # Get all active idols
            idols = db.query(Idol).all()
            
            updated_rankings = []
            for idol in idols:
                # Calculate new ranking score
                score = self._calculate_ranking_score(db, idol.id)
                
                # Create new ranking entry
                ranking = Ranking(
                    idol_id=idol.id,
                    rank=0,  # Will be calculated after all scores are determined
                    score=score,
                    category='overall',
                    date=datetime.now()
                )
                updated_rankings.append(ranking)
            
            # Sort by score and assign ranks
            updated_rankings.sort(key=lambda x: x.score, reverse=True)
            for i, ranking in enumerate(updated_rankings):
                ranking.rank = i + 1
            
            # Save to database
            db.add_all(updated_rankings)
            db.commit()
            
            return {
                'status': 'success',
                'rankings_updated': len(updated_rankings),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _calculate_ranking_score(self, db: Session, idol_id: int) -> float:
        """Calculate ranking score for an idol based on various metrics"""
        # This is a simplified scoring algorithm
        # In a real implementation, you would use more sophisticated algorithms
        
        # Get recent trend data
        recent_trends = db.query(TrendData).filter(
            TrendData.idol_id == idol_id,
            TrendData.date >= datetime.now() - timedelta(days=30)
        ).all()
        
        if not recent_trends:
            return 0.0
        
        # Calculate average score from recent trends
        scores = [trend.score for trend in recent_trends]
        avg_score = sum(scores) / len(scores)
        
        # Add some randomization for demo purposes
        # In production, this would be based on actual metrics
        random_factor = np.random.normal(0, 5)  # Small random variation
        final_score = max(0, min(100, avg_score + random_factor))
        
        return final_score
    
    def _simulate_melon_data(self) -> List[Dict[str, Any]]:
        """Simulate Melon chart data"""
        return [
            {'artist': 'NewJeans', 'song': 'Super Shy', 'rank': 1, 'score': 95.5},
            {'artist': 'IVE', 'song': 'I AM', 'rank': 2, 'score': 92.3},
            {'artist': 'LE SSERAFIM', 'song': 'UNFORGIVEN', 'rank': 3, 'score': 89.7},
            {'artist': 'aespa', 'song': 'Spicy', 'rank': 4, 'score': 87.2},
            {'artist': 'BLACKPINK', 'song': 'Shut Down', 'rank': 5, 'score': 85.1}
        ]
    
    def _simulate_genie_data(self) -> List[Dict[str, Any]]:
        """Simulate Genie chart data"""
        return [
            {'artist': 'NewJeans', 'song': 'Super Shy', 'rank': 1, 'score': 94.8},
            {'artist': 'IVE', 'song': 'I AM', 'rank': 2, 'score': 91.5},
            {'artist': 'LE SSERAFIM', 'song': 'UNFORGIVEN', 'rank': 3, 'score': 88.9},
            {'artist': 'aespa', 'song': 'Spicy', 'rank': 4, 'score': 86.3},
            {'artist': 'BLACKPINK', 'song': 'Shut Down', 'rank': 5, 'score': 84.7}
        ]
    
    def _simulate_bugs_data(self) -> List[Dict[str, Any]]:
        """Simulate Bugs chart data"""
        return [
            {'artist': 'NewJeans', 'song': 'Super Shy', 'rank': 1, 'score': 93.2},
            {'artist': 'IVE', 'song': 'I AM', 'rank': 2, 'score': 90.8},
            {'artist': 'LE SSERAFIM', 'song': 'UNFORGIVEN', 'rank': 3, 'score': 87.5},
            {'artist': 'aespa', 'song': 'Spicy', 'rank': 4, 'score': 85.9},
            {'artist': 'BLACKPINK', 'song': 'Shut Down', 'rank': 5, 'score': 83.4}
        ]
    
    def _simulate_instagram_data(self) -> List[Dict[str, Any]]:
        """Simulate Instagram engagement data"""
        return [
            {'artist': 'BLACKPINK', 'followers': 50000000, 'engagement_rate': 3.2},
            {'artist': 'BTS', 'followers': 45000000, 'engagement_rate': 4.1},
            {'artist': 'TWICE', 'followers': 35000000, 'engagement_rate': 2.8},
            {'artist': 'Red Velvet', 'followers': 25000000, 'engagement_rate': 3.5},
            {'artist': 'aespa', 'followers': 20000000, 'engagement_rate': 4.2}
        ]
    
    def _simulate_twitter_data(self) -> List[Dict[str, Any]]:
        """Simulate Twitter engagement data"""
        return [
            {'artist': 'BTS', 'followers': 40000000, 'engagement_rate': 2.8},
            {'artist': 'BLACKPINK', 'followers': 35000000, 'engagement_rate': 3.1},
            {'artist': 'TWICE', 'followers': 30000000, 'engagement_rate': 2.5},
            {'artist': 'Red Velvet', 'followers': 20000000, 'engagement_rate': 3.0},
            {'artist': 'aespa', 'followers': 15000000, 'engagement_rate': 3.8}
        ]
    
    def _simulate_tiktok_data(self) -> List[Dict[str, Any]]:
        """Simulate TikTok engagement data"""
        return [
            {'artist': 'NewJeans', 'followers': 25000000, 'engagement_rate': 5.2},
            {'artist': 'IVE', 'followers': 20000000, 'engagement_rate': 4.8},
            {'artist': 'LE SSERAFIM', 'followers': 18000000, 'engagement_rate': 4.5},
            {'artist': 'aespa', 'followers': 15000000, 'engagement_rate': 4.9},
            {'artist': 'BLACKPINK', 'followers': 40000000, 'engagement_rate': 3.2}
        ]
    
    def _simulate_spotify_data(self) -> List[Dict[str, Any]]:
        """Simulate Spotify streaming data"""
        return [
            {'artist': 'BTS', 'monthly_listeners': 50000000, 'top_track': 'Dynamite'},
            {'artist': 'BLACKPINK', 'monthly_listeners': 45000000, 'top_track': 'Pink Venom'},
            {'artist': 'TWICE', 'monthly_listeners': 35000000, 'top_track': 'Moonlight Sunrise'},
            {'artist': 'NewJeans', 'monthly_listeners': 30000000, 'top_track': 'Super Shy'},
            {'artist': 'IVE', 'monthly_listeners': 25000000, 'top_track': 'I AM'}
        ]
    
    def _simulate_youtube_data(self) -> List[Dict[str, Any]]:
        """Simulate YouTube data"""
        return [
            {'artist': 'BLACKPINK', 'subscribers': 80000000, 'total_views': 25000000000},
            {'artist': 'BTS', 'subscribers': 75000000, 'total_views': 22000000000},
            {'artist': 'TWICE', 'subscribers': 60000000, 'total_views': 18000000000},
            {'artist': 'NewJeans', 'subscribers': 40000000, 'total_views': 12000000000},
            {'artist': 'IVE', 'subscribers': 35000000, 'total_views': 10000000000}
        ]
    
    def _simulate_apple_music_data(self) -> List[Dict[str, Any]]:
        """Simulate Apple Music data"""
        return [
            {'artist': 'BTS', 'monthly_listeners': 40000000, 'top_track': 'Dynamite'},
            {'artist': 'BLACKPINK', 'monthly_listeners': 38000000, 'top_track': 'Pink Venom'},
            {'artist': 'TWICE', 'monthly_listeners': 30000000, 'top_track': 'Moonlight Sunrise'},
            {'artist': 'NewJeans', 'monthly_listeners': 25000000, 'top_track': 'Super Shy'},
            {'artist': 'IVE', 'monthly_listeners': 20000000, 'top_track': 'I AM'}
        ]
    
    def _process_chart_data(self, db: Session, chart_data: Dict[str, List[Dict[str, Any]]]):
        """Process and store chart data"""
        # This would process the chart data and store it in the database
        # For now, we'll just create some trend data entries
        for source, data in chart_data.items():
            for entry in data:
                # Find idol by name (simplified)
                idol = db.query(Idol).filter(Idol.name == entry['artist']).first()
                if idol:
                    trend = TrendData(
                        idol_id=idol.id,
                        score=entry['score'],
                        rank=entry['rank'],
                        category='music',
                        date=datetime.now()
                    )
                    db.add(trend)
        
        db.commit()
    
    def _process_social_data(self, db: Session, social_data: Dict[str, List[Dict[str, Any]]]):
        """Process and store social media data"""
        # Similar to chart data processing
        for source, data in social_data.items():
            for entry in data:
                idol = db.query(Idol).filter(Idol.name == entry['artist']).first()
                if idol:
                    trend = TrendData(
                        idol_id=idol.id,
                        score=entry['engagement_rate'] * 10,  # Convert to 0-100 scale
                        rank=0,
                        category='social',
                        date=datetime.now()
                    )
                    db.add(trend)
        
        db.commit()
    
    def _process_streaming_data(self, db: Session, streaming_data: Dict[str, List[Dict[str, Any]]]):
        """Process and store streaming data"""
        # Similar to other data processing
        for source, data in streaming_data.items():
            for entry in data:
                idol = db.query(Idol).filter(Idol.name == entry['artist']).first()
                if idol:
                    # Convert monthly listeners to a score (simplified)
                    score = min(100, entry['monthly_listeners'] / 1000000)
                    trend = TrendData(
                        idol_id=idol.id,
                        score=score,
                        rank=0,
                        category='streaming',
                        date=datetime.now()
                    )
                    db.add(trend)
        
        db.commit() 
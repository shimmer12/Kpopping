#!/usr/bin/env python3
"""
Database initialization script for K-Pop Ranking Platform
Creates sample data for testing and development
"""

import asyncio
import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, engine
from models import Base, Idol, Group, DataSource
from services.data_collector import DataCollectorService

def init_database():
    """Initialize the database with sample data"""
    print("🚀 Initializing K-Pop Ranking Platform Database...")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_idols = db.query(Idol).count()
        if existing_idols > 0:
            print(f"⚠️  Database already contains {existing_idols} idols. Skipping initialization.")
            return
        
        # Create sample groups first
        sample_groups = [
            {
                'name': 'BTS',
                'company': 'HYBE',
                'is_active': True
            },
            {
                'name': 'BLACKPINK',
                'company': 'YG Entertainment',
                'is_active': True
            },
            {
                'name': 'TWICE',
                'company': 'JYP Entertainment',
                'is_active': True
            },
            {
                'name': 'SEVENTEEN',
                'company': 'PLEDIS Entertainment',
                'is_active': True
            },
            {
                'name': 'NewJeans',
                'company': 'ADOR',
                'is_active': True
            },
            {
                'name': 'IVE',
                'company': 'Starship Entertainment',
                'is_active': True
            },
            {
                'name': 'LE SSERAFIM',
                'company': 'Source Music',
                'is_active': True
            },
            {
                'name': 'aespa',
                'company': 'SM Entertainment',
                'is_active': True
            },
            {
                'name': 'Stray Kids',
                'company': 'JYP Entertainment',
                'is_active': True
            }
        ]
        
        # Create groups and store their IDs
        group_map = {}
        for group_data in sample_groups:
            group = Group(**group_data)
            db.add(group)
            db.flush()  # This gets the ID
            group_map[group.name] = group.id
        
        print(f"✅ Created {len(sample_groups)} sample groups")
        
        # Create sample idols with proper group_id references
        sample_idols = [
            {
                'name': 'BTS',
                'stage_name': 'BTS',
                'group_id': group_map['BTS'],
                'company': 'HYBE',
                'gender': 'male',
                'is_soloist': False,
                'is_active': True
            },
            {
                'name': 'BLACKPINK',
                'stage_name': 'BLACKPINK',
                'group_id': group_map['BLACKPINK'],
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
                'group_id': group_map['TWICE'],
                'company': 'JYP Entertainment',
                'gender': 'female',
                'is_soloist': False,
                'is_active': True
            },
            {
                'name': 'SEVENTEEN',
                'stage_name': 'SEVENTEEN',
                'group_id': group_map['SEVENTEEN'],
                'company': 'PLEDIS Entertainment',
                'gender': 'male',
                'is_soloist': False,
                'is_active': True
            },
            {
                'name': 'NewJeans',
                'stage_name': 'NewJeans',
                'group_id': group_map['NewJeans'],
                'company': 'ADOR',
                'gender': 'female',
                'is_soloist': False,
                'is_active': True
            },
            {
                'name': 'IVE',
                'stage_name': 'IVE',
                'group_id': group_map['IVE'],
                'company': 'Starship Entertainment',
                'gender': 'female',
                'is_soloist': False,
                'is_active': True
            },
            {
                'name': 'LE SSERAFIM',
                'stage_name': 'LE SSERAFIM',
                'group_id': group_map['LE SSERAFIM'],
                'company': 'Source Music',
                'gender': 'female',
                'is_soloist': False,
                'is_active': True
            },
            {
                'name': 'aespa',
                'stage_name': 'aespa',
                'group_id': group_map['aespa'],
                'company': 'SM Entertainment',
                'gender': 'female',
                'is_soloist': False,
                'is_active': True
            },
            {
                'name': 'Stray Kids',
                'stage_name': 'Stray Kids',
                'group_id': group_map['Stray Kids'],
                'company': 'JYP Entertainment',
                'gender': 'male',
                'is_soloist': False,
                'is_active': True
            }
        ]
        
        for idol_data in sample_idols:
            idol = Idol(**idol_data)
            db.add(idol)
        
        print(f"✅ Created {len(sample_idols)} sample idols")
        
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
                'name': 'TikTok API',
                'type': 'api',
                'url': 'https://developers.tiktok.com/',
                'is_active': True
            },
            {
                'name': 'Chart Scraper',
                'type': 'scraping',
                'url': 'https://www.melon.com',
                'is_active': True
            },
            {
                'name': 'Brand Reputation Scraper',
                'type': 'scraping',
                'url': 'https://www.koreaboo.com',
                'is_active': True
            },
            {
                'name': 'Trend Analysis',
                'type': 'scraping',
                'url': 'https://trends.google.com',
                'is_active': True
            }
        ]
        
        for source_data in data_sources:
            source = DataSource(**source_data)
            db.add(source)
        
        print(f"✅ Created {len(data_sources)} data sources")
        
        # Commit all changes
        db.commit()
        print("✅ Database initialization completed successfully!")
        
        # Generate sample metrics
        print("🔄 Generating sample metrics...")
        data_collector = DataCollectorService()
        asyncio.run(data_collector.refresh_all_data(db))
        print("✅ Sample metrics generated!")
        
    except Exception as e:
        print(f"❌ Error during database initialization: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_database() 
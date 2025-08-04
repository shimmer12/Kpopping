# 🎵 K-Pop Ranking Platform

A unified platform that aggregates and ranks K-Pop idols and groups based on multiple metrics including streaming performance, social media presence, brand reputation, and chart performance.

## 🌟 Features

### Core Features
- **Unified Ranking System**: Combines multiple data sources into weighted overall scores
- **Real-time Data**: Streaming charts, social media metrics, and brand reputation
- **Interactive Dashboards**: Beautiful visualizations and leaderboards
- **Comparison Tool**: Side-by-side idol/group comparisons
- **Trend Analysis**: Historical performance tracking

### Data Sources
- **Music Performance**: Spotify, YouTube, Melon, Gaon/Circle charts
- **Social Media**: Instagram, Twitter/X, TikTok follower growth and engagement
- **Brand Reputation**: Korean Consumer Forum rankings
- **Search Trends**: Google Trends and hashtag popularity
- **Award Recognition**: MAMA, SMA, and other voting-based awards

## 🛠️ Tech Stack

### Backend
- **FastAPI**: High-performance Python web framework
- **PostgreSQL**: Reliable relational database
- **Pandas/NumPy**: Data processing and analysis
- **SQLAlchemy**: Database ORM
- **Pydantic**: Data validation

### Frontend
- **React**: Modern UI framework
- **Tailwind CSS**: Utility-first styling
- **Chart.js**: Interactive data visualizations
- **Framer Motion**: Smooth animations
- **React Query**: Data fetching and caching

### Data Collection
- **YouTube Data API**: Video views and engagement
- **Spotify Web API**: Streaming data
- **Twitter API**: Social media metrics
- **Web Scraping**: Chart data and brand rankings

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL (optional - SQLite for development)

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (optional):
   ```bash
   # Create .env file
   echo "DATABASE_URL=sqlite:///./kpop_ranking.db" > .env
   echo "DEBUG=True" >> .env
   ```

5. **Initialize database with sample data**:
   ```bash
   python init_db.py
   ```

6. **Start the backend server**:
   ```bash
   python main.py
   ```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm start
   ```

The frontend will be available at `http://localhost:3000`

## 📊 Ranking Algorithm

The platform uses a weighted scoring system:

- **Music Performance (30%)**: Streaming numbers, chart positions
- **Social Media (25%)**: Follower growth, engagement rates
- **Brand Reputation (20%)**: Korean Consumer Forum rankings
- **Search Trends (15%)**: Google Trends, hashtag popularity
- **Award Recognition (10%)**: Industry awards and nominations

## 🎯 API Endpoints

### Core Endpoints
- `GET /api/rankings` - Get current rankings with filtering
- `GET /api/idols` - Get all idols with optional filtering
- `GET /api/idols/{id}` - Get specific idol details
- `GET /api/compare/{id1}/{id2}` - Compare two idols
- `GET /api/trends/{id}` - Get trend data for an idol
- `GET /api/stats` - Get platform statistics
- `POST /api/refresh-data` - Manually refresh data

### Query Parameters
- `category`: overall, music, social, brand, search
- `limit`: Number of results (default: 100)
- `group`: Filter by group name
- `gender`: Filter by gender (male, female, co-ed)

## 🎨 Frontend Features

### Pages
- **Home**: Platform overview and top rankings
- **Rankings**: Comprehensive ranking list with filters
- **Idol Details**: Individual idol information and metrics
- **Comparison**: Side-by-side idol comparison
- **Trends**: Historical performance analytics
- **About**: Platform information and methodology

### Components
- **Responsive Design**: Mobile-first approach
- **Glass Morphism**: Modern UI with blur effects
- **Smooth Animations**: Framer Motion integration
- **Interactive Charts**: Chart.js visualizations
- **Real-time Updates**: React Query for data fetching

## 🗄️ Database Schema

### Core Tables
- **idols**: Idol/group information
- **rankings**: Current and historical rankings
- **metrics**: Raw data from various sources
- **trends**: Trend analysis data
- **data_sources**: API and scraping configurations

### Key Relationships
- Idols have multiple rankings over time
- Metrics are linked to idols and data sources
- Trends track performance changes
- Rankings are calculated from aggregated metrics

## 🔧 Development

### Backend Development
```bash
# Run with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Run tests
pytest

# Format code
black .
```

### Frontend Development
```bash
# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test
```

### Database Management
```bash
# Initialize with sample data
python init_db.py

# Reset database
rm kpop_ranking.db
python init_db.py
```

## 🚀 Deployment

### Backend Deployment
1. Set up PostgreSQL database
2. Configure environment variables
3. Install dependencies: `pip install -r requirements.txt`
4. Run migrations: `alembic upgrade head`
5. Start server: `uvicorn main:app --host 0.0.0.0 --port 8000`

### Frontend Deployment
1. Build the application: `npm run build`
2. Serve static files from `build/` directory
3. Configure reverse proxy for API calls

### Environment Variables
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost/kpop_ranking

# API Keys (optional for development)
YOUTUBE_API_KEY=your_youtube_api_key
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret

# Debug mode
DEBUG=False
```

## 📈 Roadmap

### Phase 1 - MVP ✅
- [x] Basic API structure
- [x] Database schema
- [x] Core ranking algorithm
- [x] Leaderboard UI
- [x] Sample data generation

### Phase 2 - Enhanced Features 🚧
- [ ] Real-time data synchronization
- [ ] Advanced filtering and sorting
- [ ] Comparison tool
- [ ] Trend visualization
- [ ] User authentication
- [ ] Admin dashboard

### Phase 3 - Advanced Features 📋
- [ ] Custom ranking creation
- [ ] API for third-party integration
- [ ] Mobile app
- [ ] Machine learning predictions
- [ ] Real-time notifications
- [ ] Fan voting system

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines for more details.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Code Style
- Backend: Follow PEP 8 with Black formatting
- Frontend: Use Prettier and ESLint
- Commit messages: Use conventional commits

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- K-Pop industry data sources
- Open source community
- Contributors and beta testers

---

**K-Pop Radar** - The ultimate unified K-Pop ranking platform! 🎵✨ 
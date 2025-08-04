import React from 'react';
import { motion } from 'framer-motion';
import { 
  ChartBarIcon, 
  UserGroupIcon, 
  ArrowTrendingUpIcon ,
  StarIcon,
  MusicalNoteIcon,
  GlobeAltIcon,
  CogIcon,
  ShieldCheckIcon
} from '@heroicons/react/24/outline';

const About = () => {
  const features = [
    {
      icon: ChartBarIcon,
      title: 'Unified Rankings',
      description: 'Combines multiple data sources into weighted overall scores for accurate K-Pop idol rankings.'
    },
    {
      icon: ArrowTrendingUpIcon ,
      title: 'Real-time Trends',
      description: 'Track performance trends over time with interactive charts and analytics.'
    },
    {
      icon: UserGroupIcon,
      title: 'Idol Comparisons',
      description: 'Compare any two idols side-by-side with detailed metrics and performance data.'
    },
    {
      icon: StarIcon,
      title: 'Multi-source Data',
      description: 'Aggregates data from Spotify, YouTube, social media, charts, and brand reputation.'
    },
    {
      icon: MusicalNoteIcon,
      title: 'Music Performance',
      description: 'Track streaming numbers, chart positions, and music-related metrics.'
    },
    {
      icon: GlobeAltIcon,
      title: 'Global Reach',
      description: 'Monitor international popularity and global fan engagement metrics.'
    }
  ];

  const dataSources = [
    'Spotify Web API',
    'YouTube Data API',
    'Instagram Graph API',
    'Twitter API v2',
    'TikTok API',
    'Melon Chart Data',
    'Gaon/Circle Chart',
    'Korean Consumer Forum',
    'Google Trends',
    'Brand Reputation Rankings'
  ];

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.5
      }
    }
  };

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="text-center py-20">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="max-w-4xl mx-auto"
        >
          <h1 className="responsive-heading text-white mb-6">
            About K-Pop Radar
          </h1>
          <p className="text-xl text-white text-opacity-80 mb-8 max-w-3xl mx-auto">
            The ultimate unified platform for tracking K-Pop idol performance across multiple dimensions. 
            We aggregate data from various sources to provide comprehensive rankings and analytics.
          </p>
        </motion.div>
      </section>

      {/* Mission Section */}
      <section className="py-16">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="glass rounded-lg p-8 max-w-4xl mx-auto"
        >
          <h2 className="text-3xl font-bold text-white mb-6">Our Mission</h2>
          <p className="text-white text-opacity-80 text-lg leading-relaxed">
            K-Pop Radar aims to provide the most comprehensive and accurate ranking system for K-Pop idols 
            and groups. By combining multiple data sources and using sophisticated algorithms, we create 
            unified scores that reflect the true popularity and performance of artists in the industry.
          </p>
        </motion.div>
      </section>

      {/* Features Section */}
      <section className="py-16">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="text-center mb-12"
        >
          <h2 className="responsive-heading text-white mb-4">
            Platform Features
          </h2>
          <p className="text-xl text-white text-opacity-80">
            Comprehensive analytics and ranking system designed specifically for the K-Pop industry
          </p>
        </motion.div>

        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="responsive-grid max-w-6xl mx-auto"
        >
          {features.map((feature, index) => (
            <motion.div
              key={index}
              variants={itemVariants}
              className="ranking-card"
            >
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg flex items-center justify-center mr-4">
                  <feature.icon className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-white">{feature.title}</h3>
              </div>
              <p className="text-white text-opacity-80">{feature.description}</p>
            </motion.div>
          ))}
        </motion.div>
      </section>

      {/* Data Sources Section */}
      <section className="py-16">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="glass rounded-lg p-8 max-w-4xl mx-auto"
        >
          <h2 className="text-3xl font-bold text-white mb-6">Data Sources</h2>
          <p className="text-white text-opacity-80 mb-6">
            We aggregate data from multiple reliable sources to ensure comprehensive and accurate rankings:
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {dataSources.map((source, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3, delay: index * 0.1 }}
                className="flex items-center space-x-3"
              >
                <div className="w-2 h-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full"></div>
                <span className="text-white text-opacity-80">{source}</span>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </section>

      {/* Algorithm Section */}
      <section className="py-16">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="glass rounded-lg p-8 max-w-4xl mx-auto"
        >
          <h2 className="text-3xl font-bold text-white mb-6">Ranking Algorithm</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <h3 className="text-xl font-semibold text-white mb-4">Weighted Scoring System</h3>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-white text-opacity-80">Music Performance</span>
                  <span className="text-white font-semibold">30%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-white text-opacity-80">Social Media</span>
                  <span className="text-white font-semibold">25%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-white text-opacity-80">Brand Reputation</span>
                  <span className="text-white font-semibold">20%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-white text-opacity-80">Search Trends</span>
                  <span className="text-white font-semibold">15%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-white text-opacity-80">Award Recognition</span>
                  <span className="text-white font-semibold">10%</span>
                </div>
              </div>
            </div>
            <div>
              <h3 className="text-xl font-semibold text-white mb-4">Data Processing</h3>
              <ul className="text-white text-opacity-80 space-y-2">
                <li>• Real-time data collection</li>
                <li>• Normalized scoring (0-100)</li>
                <li>• Trend analysis and predictions</li>
                <li>• Comparative analytics</li>
                <li>• Historical performance tracking</li>
              </ul>
            </div>
          </div>
        </motion.div>
      </section>

      {/* Technology Stack */}
      <section className="py-16">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="text-center"
        >
          <h2 className="responsive-heading text-white mb-8">Technology Stack</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            <div className="glass rounded-lg p-6">
              <h3 className="text-xl font-semibold text-white mb-4">Backend</h3>
              <ul className="text-white text-opacity-80 space-y-2 text-left">
                <li>• FastAPI (Python)</li>
                <li>• PostgreSQL</li>
                <li>• SQLAlchemy ORM</li>
                <li>• Pandas/NumPy</li>
                <li>• Async data collection</li>
              </ul>
            </div>
            <div className="glass rounded-lg p-6">
              <h3 className="text-xl font-semibold text-white mb-4">Frontend</h3>
              <ul className="text-white text-opacity-80 space-y-2 text-left">
                <li>• React 18</li>
                <li>• Tailwind CSS</li>
                <li>• Framer Motion</li>
                <li>• Chart.js</li>
                <li>• React Query</li>
              </ul>
            </div>
            <div className="glass rounded-lg p-6">
              <h3 className="text-xl font-semibold text-white mb-4">APIs & Data</h3>
              <ul className="text-white text-opacity-80 space-y-2 text-left">
                <li>• YouTube Data API</li>
                <li>• Spotify Web API</li>
                <li>• Social Media APIs</li>
                <li>• Chart Data Scraping</li>
                <li>• Real-time Updates</li>
              </ul>
            </div>
          </div>
        </motion.div>
      </section>
    </div>
  );
};

export default About; 
import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useQuery } from 'react-query';
import { 
  ChartBarIcon, 
  UserGroupIcon, 
  ArrowTrendingUpIcon,  // ✅ correct replacement
  StarIcon,
  MusicalNoteIcon,
  GlobeAltIcon
} from '@heroicons/react/24/outline';
import axios from 'axios';

const Home = () => {
  // Fetch platform stats
  const { data: stats, isLoading: statsLoading } = useQuery('platformStats', async () => {
    const response = await axios.get('http://localhost:8000/api/stats');
    return response.data;
  });

  // Fetch top rankings
  const { data: rankings, isLoading: rankingsLoading } = useQuery('topRankings', async () => {
    const response = await axios.get('http://localhost:8000/api/rankings?limit=5');
    return response.data;
  });

  const features = [
    {
      icon: ChartBarIcon,
      title: 'Unified Rankings',
      description: 'Combines multiple data sources into weighted overall scores for accurate K-Pop idol rankings.'
    },
    {
      icon: ArrowTrendingUpIcon,  // ✅ change this from TrendingUpIcon
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
            <span className="gradient-text">K-Pop Radar</span>
            <br />
            <span className="text-3xl md:text-4xl lg:text-5xl font-light">
              Unified Ranking Platform
            </span>
          </h1>
          <p className="text-xl text-white text-opacity-80 mb-8 max-w-2xl mx-auto">
            The ultimate platform for tracking K-Pop idol performance across music charts, 
            social media, brand reputation, and global trends.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/rankings">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="btn-primary"
              >
                View Rankings
              </motion.button>
            </Link>
            <Link to="/about">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="btn-secondary"
              >
                Learn More
              </motion.button>
            </Link>
          </div>
        </motion.div>
      </section>

      {/* Stats Section */}
      <section className="py-12">
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto"
        >
          {statsLoading ? (
            <div className="col-span-4 flex justify-center">
              <div className="loading-spinner"></div>
            </div>
          ) : (
            <>
              <motion.div variants={itemVariants} className="stats-card">
                <div className="text-3xl font-bold text-white mb-2">
                  {stats?.total_idols || 0}
                </div>
                <div className="text-white text-opacity-70">Active Idols</div>
              </motion.div>
              <motion.div variants={itemVariants} className="stats-card">
                <div className="text-3xl font-bold text-white mb-2">
                  {stats?.total_groups || 0}
                </div>
                <div className="text-white text-opacity-70">Groups</div>
              </motion.div>
              <motion.div variants={itemVariants} className="stats-card">
                <div className="text-3xl font-bold text-white mb-2">
                  {stats?.total_soloists || 0}
                </div>
                <div className="text-white text-opacity-70">Soloists</div>
              </motion.div>
              <motion.div variants={itemVariants} className="stats-card">
                <div className="text-3xl font-bold text-white mb-2">
                  {stats?.data_sources_count || 0}
                </div>
                <div className="text-white text-opacity-70">Data Sources</div>
              </motion.div>
            </>
          )}
        </motion.div>
      </section>

      {/* Features Section */}
      <section className="py-16">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-12"
        >
          <h2 className="responsive-heading text-white mb-4">
            Platform Features
          </h2>
          <p className="text-xl text-white text-opacity-80 max-w-3xl mx-auto">
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

      {/* Top Rankings Preview */}
      <section className="py-16">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-12"
        >
          <h2 className="responsive-heading text-white mb-4">
            Current Top Rankings
          </h2>
          <p className="text-xl text-white text-opacity-80">
            See who's leading the K-Pop industry right now
          </p>
        </motion.div>

        {rankingsLoading ? (
          <div className="flex justify-center">
            <div className="loading-spinner"></div>
          </div>
        ) : (
          <motion.div
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            className="max-w-4xl mx-auto"
          >
            {rankings?.slice(0, 5).map((ranking, index) => (
              <motion.div
                key={ranking.id}
                variants={itemVariants}
                className="ranking-card mb-4"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div className="w-12 h-12 bg-gradient-to-r from-yellow-400 to-orange-500 rounded-full flex items-center justify-center mr-4">
                      <span className="text-white font-bold text-lg">#{index + 1}</span>
                    </div>
                    <div>
                      <h3 className="text-xl font-semibold text-white">
                        {ranking.idol.name}
                      </h3>
                      <p className="text-white text-opacity-70">
                        {ranking.idol.group || 'Solo Artist'}
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-2xl font-bold text-white">
                      {ranking.score.toFixed(1)}
                    </div>
                    <div className="text-white text-opacity-70">Score</div>
                  </div>
                </div>
              </motion.div>
            ))}
            <div className="text-center mt-8">
              <Link to="/rankings">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="btn-primary"
                >
                  View All Rankings
                </motion.button>
              </Link>
            </div>
          </motion.div>
        )}
      </section>

      {/* CTA Section */}
      <section className="py-16">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center"
        >
          <div className="glass rounded-2xl p-12 max-w-4xl mx-auto">
            <h2 className="responsive-heading text-white mb-6">
              Ready to Explore?
            </h2>
            <p className="text-xl text-white text-opacity-80 mb-8">
              Start exploring the comprehensive K-Pop ranking system and discover 
              detailed analytics for your favorite idols and groups.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link to="/rankings">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="btn-primary"
                >
                  Explore Rankings
                </motion.button>
              </Link>
              <Link to="/trends">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="btn-secondary"
                >
                  View Trends
                </motion.button>
              </Link>
            </div>
          </div>
        </motion.div>
      </section>
    </div>
  );
};

export default Home; 
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useQuery } from 'react-query';
import { 
  FunnelIcon, 
  MagnifyingGlassIcon,
  ChartBarIcon,
  UserGroupIcon,
  StarIcon
} from '@heroicons/react/24/outline';
import axios from 'axios';

const Rankings = () => {
  const [filters, setFilters] = useState({
    category: 'overall',
    group: '',
    gender: '',
    search: ''
  });

  const [sortBy, setSortBy] = useState('rank');

  // Fetch rankings with filters
  const { data: rankings, isLoading, error } = useQuery(
    ['rankings', filters],
    async () => {
      const params = new URLSearchParams();
      if (filters.category) params.append('category', filters.category);
      if (filters.group) params.append('group', filters.group);
      if (filters.gender) params.append('gender', filters.gender);
      
      const response = await axios.get(`http://localhost:8000/api/rankings?${params.toString()}`);
      return response.data;
    }
  );

  // Fetch all idols for filter options
  const { data: idols } = useQuery('idols', async () => {
    const response = await axios.get('http://localhost:8000/api/idols');
    return response.data;
  });

  const categories = [
    { value: 'overall', label: 'Overall', icon: StarIcon },
    { value: 'music', label: 'Music', icon: ChartBarIcon },
    { value: 'social', label: 'Social', icon: UserGroupIcon },
    { value: 'brand', label: 'Brand', icon: StarIcon },
    { value: 'search', label: 'Search', icon: MagnifyingGlassIcon }
  ];

  const genders = [
    { value: 'male', label: 'Male' },
    { value: 'female', label: 'Female' },
    { value: 'co-ed', label: 'Co-ed' }
  ];

  // Get unique groups from idols data
  const groups = idols ? [...new Set(idols.map(idol => idol.group).filter(Boolean))] : [];

  // Filter and sort rankings
  const filteredRankings = rankings ? rankings
    .filter(ranking => {
      if (filters.search) {
        const searchTerm = filters.search.toLowerCase();
        return ranking.idol.name.toLowerCase().includes(searchTerm) ||
               (ranking.idol.group && ranking.idol.group.toLowerCase().includes(searchTerm));
      }
      return true;
    })
    .sort((a, b) => {
      switch (sortBy) {
        case 'rank':
          return a.rank - b.rank;
        case 'score':
          return b.score - a.score;
        case 'name':
          return a.idol.name.localeCompare(b.idol.name);
        default:
          return a.rank - b.rank;
      }
    }) : [];

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.05
      }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.3
      }
    }
  };

  const getRankColor = (rank) => {
    if (rank === 1) return 'from-yellow-400 to-yellow-600';
    if (rank === 2) return 'from-gray-300 to-gray-500';
    if (rank === 3) return 'from-orange-400 to-orange-600';
    return 'from-purple-400 to-pink-400';
  };

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-400';
    if (score >= 60) return 'text-yellow-400';
    if (score >= 40) return 'text-orange-400';
    return 'text-red-400';
  };

  if (error) {
    return (
      <div className="text-center py-20">
        <div className="text-red-400 text-xl mb-4">Error loading rankings</div>
        <div className="text-white text-opacity-70">{error.message}</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="text-center mb-12"
      >
        <h1 className="responsive-heading text-white mb-4">
          K-Pop Rankings
        </h1>
        <p className="text-xl text-white text-opacity-80 max-w-3xl mx-auto">
          Comprehensive rankings based on music performance, social media presence, 
          brand reputation, search trends, and award recognition.
        </p>
      </motion.div>

      {/* Filters */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
        className="glass rounded-lg p-6 mb-8"
      >
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
          {/* Category Filter */}
          <div>
            <label className="block text-white text-sm font-medium mb-2">
              Category
            </label>
            <select
              value={filters.category}
              onChange={(e) => setFilters({ ...filters, category: e.target.value })}
              className="select-field w-full"
            >
              {categories.map(category => (
                <option key={category.value} value={category.value}>
                  {category.label}
                </option>
              ))}
            </select>
          </div>

          {/* Group Filter */}
          <div>
            <label className="block text-white text-sm font-medium mb-2">
              Group
            </label>
            <select
              value={filters.group}
              onChange={(e) => setFilters({ ...filters, group: e.target.value })}
              className="select-field w-full"
            >
              <option value="">All Groups</option>
              {groups.map(group => (
                <option key={group} value={group}>
                  {group}
                </option>
              ))}
            </select>
          </div>

          {/* Gender Filter */}
          <div>
            <label className="block text-white text-sm font-medium mb-2">
              Gender
            </label>
            <select
              value={filters.gender}
              onChange={(e) => setFilters({ ...filters, gender: e.target.value })}
              className="select-field w-full"
            >
              <option value="">All</option>
              {genders.map(gender => (
                <option key={gender.value} value={gender.value}>
                  {gender.label}
                </option>
              ))}
            </select>
          </div>

          {/* Search */}
          <div>
            <label className="block text-white text-sm font-medium mb-2">
              Search
            </label>
            <div className="relative">
              <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-white text-opacity-60" />
              <input
                type="text"
                placeholder="Search idols..."
                value={filters.search}
                onChange={(e) => setFilters({ ...filters, search: e.target.value })}
                className="input-field w-full pl-10"
              />
            </div>
          </div>

          {/* Sort */}
          <div>
            <label className="block text-white text-sm font-medium mb-2">
              Sort By
            </label>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="select-field w-full"
            >
              <option value="rank">Rank</option>
              <option value="score">Score</option>
              <option value="name">Name</option>
            </select>
          </div>
        </div>
      </motion.div>

      {/* Rankings List */}
      {isLoading ? (
        <div className="flex justify-center py-20">
          <div className="loading-spinner"></div>
        </div>
      ) : (
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="space-y-4"
        >
          {filteredRankings.map((ranking, index) => (
            <motion.div
              key={ranking.id}
              variants={itemVariants}
              className="ranking-card"
            >
              <div className="flex items-center justify-between">
                {/* Rank and Idol Info */}
                <div className="flex items-center space-x-6">
                  <div className={`w-16 h-16 bg-gradient-to-r ${getRankColor(ranking.rank)} rounded-full flex items-center justify-center`}>
                    <span className="text-white font-bold text-xl">#{ranking.rank}</span>
                  </div>
                  
                  <div className="flex items-center space-x-4">
                    <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg flex items-center justify-center">
                      <span className="text-white font-bold text-lg">
                        {ranking.idol.name.charAt(0)}
                      </span>
                    </div>
                    
                    <div>
                      <h3 className="text-xl font-semibold text-white">
                        {ranking.idol.name}
                      </h3>
                      <p className="text-white text-opacity-70">
                        {ranking.idol.group || 'Solo Artist'}
                      </p>
                      {ranking.idol.company && (
                        <p className="text-white text-opacity-50 text-sm">
                          {ranking.idol.company}
                        </p>
                      )}
                    </div>
                  </div>
                </div>

                {/* Scores */}
                <div className="flex items-center space-x-8">
                  <div className="text-center">
                    <div className={`text-3xl font-bold ${getScoreColor(ranking.score)}`}>
                      {ranking.score.toFixed(1)}
                    </div>
                    <div className="text-white text-opacity-70 text-sm">Overall</div>
                  </div>
                  
                  <div className="hidden lg:flex space-x-6">
                    {ranking.music_score && (
                      <div className="text-center">
                        <div className="text-lg font-semibold text-white">
                          {ranking.music_score.toFixed(1)}
                        </div>
                        <div className="text-white text-opacity-70 text-xs">Music</div>
                      </div>
                    )}
                    {ranking.social_score && (
                      <div className="text-center">
                        <div className="text-lg font-semibold text-white">
                          {ranking.social_score.toFixed(1)}
                        </div>
                        <div className="text-white text-opacity-70 text-xs">Social</div>
                      </div>
                    )}
                    {ranking.brand_score && (
                      <div className="text-center">
                        <div className="text-lg font-semibold text-white">
                          {ranking.brand_score.toFixed(1)}
                        </div>
                        <div className="text-white text-opacity-70 text-xs">Brand</div>
                      </div>
                    )}
                  </div>
                </div>

                {/* Actions */}
                <div className="flex space-x-2">
                  <Link to={`/idol/${ranking.idol.id}`}>
                    <motion.button
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      className="btn-secondary text-sm px-4 py-2"
                    >
                      Details
                    </motion.button>
                  </Link>
                </div>
              </div>
            </motion.div>
          ))}
        </motion.div>
      )}

      {/* No Results */}
      {!isLoading && filteredRankings.length === 0 && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-center py-20"
        >
          <div className="text-white text-xl mb-4">No rankings found</div>
          <div className="text-white text-opacity-70">
            Try adjusting your filters or search terms
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default Rankings; 
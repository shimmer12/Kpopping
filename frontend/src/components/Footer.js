import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { MusicalNoteIcon } from '@heroicons/react/24/outline';

const Footer = () => {
  return (
    <footer className="glass mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col md:flex-row justify-between items-center">
          {/* Logo and Description */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="flex items-center space-x-2 mb-4 md:mb-0"
          >
            <div className="w-8 h-8 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg flex items-center justify-center">
              <MusicalNoteIcon className="w-5 h-5 text-white" />
            </div>
            <div>
              <span className="text-lg font-bold text-white gradient-text">
                K-Pop Radar
              </span>
              <p className="text-white text-opacity-70 text-sm">
                Unified K-Pop Ranking Platform
              </p>
            </div>
          </motion.div>

          {/* Navigation Links */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="flex space-x-6 mb-4 md:mb-0"
          >
            <Link to="/" className="text-white text-opacity-70 hover:text-white transition-colors">
              Home
            </Link>
            <Link to="/rankings" className="text-white text-opacity-70 hover:text-white transition-colors">
              Rankings
            </Link>
            <Link to="/trends" className="text-white text-opacity-70 hover:text-white transition-colors">
              Trends
            </Link>
            <Link to="/about" className="text-white text-opacity-70 hover:text-white transition-colors">
              About
            </Link>
          </motion.div>

          {/* Copyright */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="text-white text-opacity-50 text-sm"
          >
            © 2024 K-Pop Radar. All rights reserved.
          </motion.div>
        </div>
      </div>
    </footer>
  );
};

export default Footer; 
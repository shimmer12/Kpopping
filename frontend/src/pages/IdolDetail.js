import React from 'react';
import { useParams } from 'react-router-dom';
import { motion } from 'framer-motion';

const IdolDetail = () => {
  const { id } = useParams();

  return (
    <div className="min-h-screen">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="text-center py-20"
      >
        <h1 className="responsive-heading text-white mb-4">
          Idol Details
        </h1>
        <p className="text-xl text-white text-opacity-80">
          Detailed information for idol ID: {id}
        </p>
        <div className="glass rounded-lg p-8 mt-8 max-w-2xl mx-auto">
          <p className="text-white text-opacity-70">
            This page will show detailed information about the idol, including:
          </p>
          <ul className="text-white text-opacity-70 mt-4 text-left">
            <li>• Personal information and background</li>
            <li>• Current rankings and scores</li>
            <li>• Performance metrics and trends</li>
            <li>• Social media statistics</li>
            <li>• Music chart performance</li>
            <li>• Brand reputation data</li>
          </ul>
        </div>
      </motion.div>
    </div>
  );
};

export default IdolDetail; 
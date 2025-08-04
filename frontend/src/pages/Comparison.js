import React from 'react';
import { useParams } from 'react-router-dom';
import { motion } from 'framer-motion';

const Comparison = () => {
  const { id1, id2 } = useParams();

  return (
    <div className="min-h-screen">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="text-center py-20"
      >
        <h1 className="responsive-heading text-white mb-4">
          Idol Comparison
        </h1>
        <p className="text-xl text-white text-opacity-80">
          Comparing idols ID: {id1} vs ID: {id2}
        </p>
        <div className="glass rounded-lg p-8 mt-8 max-w-4xl mx-auto">
          <p className="text-white text-opacity-70">
            This page will show a side-by-side comparison of two idols, including:
          </p>
          <ul className="text-white text-opacity-70 mt-4 text-left">
            <li>• Overall scores and rankings</li>
            <li>• Music performance metrics</li>
            <li>• Social media presence</li>
            <li>• Brand reputation scores</li>
            <li>• Search trend comparisons</li>
            <li>• Award recognition</li>
            <li>• Interactive charts and graphs</li>
          </ul>
        </div>
      </motion.div>
    </div>
  );
};

export default Comparison; 
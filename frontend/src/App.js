import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { motion } from 'framer-motion';

// Components
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Home from './pages/Home';
import Rankings from './pages/Rankings';
import IdolDetail from './pages/IdolDetail';
import Comparison from './pages/Comparison';
import Trends from './pages/Trends';
import About from './pages/About';

// Styles
import './index.css';

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="min-h-screen bg-gradient-to-br from-purple-900 via-pink-900 to-indigo-900">
          <Navbar />
          
          <motion.main
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="container mx-auto px-4 py-8"
          >
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/rankings" element={<Rankings />} />
              <Route path="/idol/:id" element={<IdolDetail />} />
              <Route path="/compare/:id1/:id2" element={<Comparison />} />
              <Route path="/trends" element={<Trends />} />
              <Route path="/about" element={<About />} />
            </Routes>
          </motion.main>
          
          <Footer />
        </div>
      </Router>
    </QueryClientProvider>
  );
}

export default App; 
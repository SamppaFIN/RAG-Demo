import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Moon, Sun, Languages, Sparkles, RefreshCw, Info } from 'lucide-react';
import QueryInput from './components/QueryInput';
import RAGPipeline from './components/RAGPipeline';
import CandyShowcase from './components/CandyShowcase';
import About from './components/About';
import { translations } from './utils/translations';
import './App.css';

interface QueryResponse {
  query: string;
  language: string;
  steps: RAGStep[];
  final_answer: { [key: string]: string };
  total_time: number;
}

interface RAGStep {
  step: string;
  title: { [key: string]: string };
  description: { [key: string]: string };
  data: any;
  processing_time: number;
}

function App() {
  const [darkMode, setDarkMode] = useState(false);
  const [language, setLanguage] = useState<'en' | 'fi'>('en');
  const [isLoading, setIsLoading] = useState(false);
  const [queryResponse, setQueryResponse] = useState<QueryResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [showAbout, setShowAbout] = useState(false);

  // Load preferences from localStorage
  useEffect(() => {
    const savedDarkMode = localStorage.getItem('darkMode');
    const savedLanguage = localStorage.getItem('language');
    
    if (savedDarkMode) {
      setDarkMode(JSON.parse(savedDarkMode));
    }
    
    if (savedLanguage && (savedLanguage === 'en' || savedLanguage === 'fi')) {
      setLanguage(savedLanguage as 'en' | 'fi');
    }
  }, []);

  // Apply dark mode class to document
  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
    localStorage.setItem('darkMode', JSON.stringify(darkMode));
  }, [darkMode]);

  // Save language preference
  useEffect(() => {
    localStorage.setItem('language', language);
  }, [language]);

  const handleQuery = async (query: string) => {
    setIsLoading(true);
    setError(null);
    setQueryResponse(null);

    try {
      const response = await fetch('/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query, language }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setQueryResponse(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = async () => {
    try {
      await fetch('/reset', { method: 'POST' });
      setQueryResponse(null);
      setError(null);
    } catch (err) {
      console.error('Reset failed:', err);
    }
  };

  const toggleDarkMode = () => setDarkMode(!darkMode);
  const toggleLanguage = () => setLanguage(language === 'en' ? 'fi' : 'en');

  const t = translations[language];

  return (
    <div className={`min-h-screen transition-colors duration-300 ${
      darkMode 
        ? 'bg-gradient-to-br from-dark-bg via-dark-surface to-dark-bg text-dark-text' 
        : 'bg-gradient-to-br from-candy-blue via-white to-candy-green text-gray-900'
    }`}>
      {/* Header */}
      <header className="relative z-10 p-4">
        <div className="max-w-6xl mx-auto flex justify-between items-center">
          <motion.div 
            className="flex items-center space-x-3"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
          >
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
              className="relative"
            >
              <Sparkles className={`w-8 h-8 ${darkMode ? 'text-candy-pink' : 'text-candy-purple'}`} />
            </motion.div>
            <div>
              <h1 className={`text-2xl md:text-3xl font-candy font-bold ${
                darkMode ? 'text-candy-pink' : 'text-candy-purple'
              }`}>
                {t.title}
              </h1>
              <p className={`text-sm ${darkMode ? 'text-dark-muted' : 'text-gray-600'}`}>
                {t.subtitle}
              </p>
            </div>
          </motion.div>

          {/* Controls */}
          <div className="flex items-center space-x-2">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => setShowAbout(true)}
              className={`p-2 rounded-full transition-colors ${
                darkMode 
                  ? 'bg-dark-surface hover:bg-dark-accent text-dark-text' 
                  : 'bg-white/70 hover:bg-white text-gray-700'
              }`}
              title={language === 'en' ? 'About' : 'Tietoa'}
            >
              <Info className="w-5 h-5" />
            </motion.button>

            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={toggleLanguage}
              className={`p-2 rounded-full transition-colors ${
                darkMode 
                  ? 'bg-dark-surface hover:bg-dark-accent text-dark-text' 
                  : 'bg-white/70 hover:bg-white text-gray-700'
              }`}
              title={t.toggleLanguage}
            >
              <Languages className="w-5 h-5" />
              <span className="ml-1 text-xs font-bold">
                {language.toUpperCase()}
              </span>
            </motion.button>

            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={toggleDarkMode}
              className={`p-2 rounded-full transition-colors ${
                darkMode 
                  ? 'bg-dark-surface hover:bg-dark-accent text-dark-text' 
                  : 'bg-white/70 hover:bg-white text-gray-700'
              }`}
              title={t.toggleTheme}
            >
              {darkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
            </motion.button>

            {queryResponse && (
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={handleReset}
                className={`p-2 rounded-full transition-colors ${
                  darkMode 
                    ? 'bg-dark-surface hover:bg-dark-accent text-dark-text' 
                    : 'bg-white/70 hover:bg-white text-gray-700'
                }`}
                title={t.reset}
              >
                <RefreshCw className="w-5 h-5" />
              </motion.button>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-4 pb-8">
        <AnimatePresence mode="wait">
          {!queryResponse && !isLoading && (
            <motion.div
              key="welcome"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.5 }}
              className="space-y-8"
            >
              {/* Welcome Section */}
              <div className={`text-center p-8 rounded-2xl ${
                darkMode ? 'bg-dark-surface/50' : 'bg-white/50'
              } backdrop-blur-sm`}>
                <motion.div
                  animate={{ y: [0, -10, 0] }}
                  transition={{ duration: 2, repeat: Infinity }}
                  className="text-6xl mb-4"
                >
                  🍭
                </motion.div>
                <h2 className={`text-xl md:text-2xl font-candy mb-4 ${
                  darkMode ? 'text-dark-text' : 'text-gray-800'
                }`}>
                  {t.welcome}
                </h2>
                <p className={`text-sm md:text-base max-w-2xl mx-auto ${
                  darkMode ? 'text-dark-muted' : 'text-gray-600'
                }`}>
                  {t.description}
                </p>
              </div>

              {/* Query Input */}
              <QueryInput onQuery={handleQuery} language={language} darkMode={darkMode} />

              {/* Candy Showcase */}
              <CandyShowcase language={language} darkMode={darkMode} />
            </motion.div>
          )}

          {/* Loading State */}
          {isLoading && (
            <motion.div
              key="loading"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="flex flex-col items-center justify-center py-16"
            >
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                className="text-6xl mb-4"
              >
                🍬
              </motion.div>
              <p className={`text-lg font-candy ${
                darkMode ? 'text-dark-text' : 'text-gray-800'
              }`}>
                {t.processing}
              </p>
            </motion.div>
          )}

          {/* RAG Pipeline Results */}
          {queryResponse && (
            <motion.div
              key="results"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.5 }}
            >
              <RAGPipeline
                queryResponse={queryResponse}
                language={language}
                darkMode={darkMode}
              />
            </motion.div>
          )}

          {/* Error State */}
          {error && (
            <motion.div
              key="error"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              className={`p-6 rounded-xl text-center ${
                darkMode ? 'bg-red-900/50 text-red-200' : 'bg-red-50 text-red-700'
              }`}
            >
              <div className="text-4xl mb-2">😔</div>
              <h3 className="font-candy text-lg mb-2">{t.error}</h3>
              <p className="text-sm">{error}</p>
              <button
                onClick={() => setError(null)}
                className={`mt-4 px-4 py-2 rounded-lg transition-colors ${
                  darkMode 
                    ? 'bg-dark-surface hover:bg-dark-accent' 
                    : 'bg-white hover:bg-gray-50'
                }`}
              >
                {t.tryAgain}
              </button>
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      {/* About Modal */}
      <AnimatePresence>
        {showAbout && (
          <About
            darkMode={darkMode}
            language={language}
            onClose={() => setShowAbout(false)}
          />
        )}
      </AnimatePresence>
    </div>
  );
}

export default App; 
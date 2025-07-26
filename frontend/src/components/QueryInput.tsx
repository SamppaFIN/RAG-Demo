import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Send, Lightbulb } from 'lucide-react';
import { translations } from '../utils/translations';

interface QueryInputProps {
  onQuery: (query: string) => void;
  language: 'en' | 'fi';
  darkMode: boolean;
}

const QueryInput: React.FC<QueryInputProps> = ({ onQuery, language, darkMode }) => {
  const [query, setQuery] = useState('');
  const [showExamples, setShowExamples] = useState(false);
  
  const t = translations[language];

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      onQuery(query.trim());
    }
  };

  const handleExampleClick = (example: string) => {
    setQuery(example);
    setShowExamples(false);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.2 }}
      className={`p-6 rounded-2xl ${
        darkMode ? 'bg-dark-surface/50' : 'bg-white/50'
      } backdrop-blur-sm`}
    >
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="relative">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder={t.queryPlaceholder}
            className={`w-full px-4 py-3 pr-12 rounded-xl border-2 transition-all duration-200 font-sans ${
              darkMode
                ? 'bg-dark-bg border-dark-accent text-dark-text placeholder-dark-muted focus:border-candy-pink'
                : 'bg-white border-gray-200 text-gray-900 placeholder-gray-500 focus:border-candy-purple'
            } focus:outline-none focus:ring-2 focus:ring-opacity-50 ${
              darkMode ? 'focus:ring-candy-pink' : 'focus:ring-candy-purple'
            }`}
          />
          <motion.button
            type="submit"
            disabled={!query.trim()}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className={`absolute right-2 top-1/2 transform -translate-y-1/2 p-2 rounded-lg transition-all ${
              query.trim()
                ? darkMode
                  ? 'bg-candy-pink hover:bg-candy-pink/80 text-white'
                  : 'bg-candy-purple hover:bg-candy-purple/80 text-white'
                : 'bg-gray-300 text-gray-500 cursor-not-allowed'
            }`}
          >
            <Send className="w-4 h-4" />
          </motion.button>
        </div>

        <div className="flex items-center justify-between">
          <motion.button
            type="button"
            onClick={() => setShowExamples(!showExamples)}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className={`flex items-center space-x-2 px-3 py-2 rounded-lg transition-colors ${
              darkMode
                ? 'text-dark-muted hover:text-dark-text hover:bg-dark-accent'
                : 'text-gray-600 hover:text-gray-800 hover:bg-gray-100'
            }`}
          >
            <Lightbulb className="w-4 h-4" />
            <span className="text-sm">{t.exampleQueries}</span>
          </motion.button>

          <motion.button
            type="submit"
            disabled={!query.trim()}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className={`px-6 py-2 rounded-xl font-candy font-semibold transition-all ${
              query.trim()
                ? darkMode
                  ? 'bg-gradient-to-r from-candy-pink to-candy-purple text-white hover:shadow-lg'
                  : 'bg-gradient-to-r from-candy-purple to-candy-pink text-white hover:shadow-lg'
                : 'bg-gray-300 text-gray-500 cursor-not-allowed'
            }`}
          >
            {t.askButton}
          </motion.button>
        </div>
      </form>

      {/* Example Queries */}
      <motion.div
        initial={false}
        animate={{
          height: showExamples ? 'auto' : 0,
          opacity: showExamples ? 1 : 0
        }}
        transition={{ duration: 0.3 }}
        className="overflow-hidden"
      >
        <div className="pt-4 space-y-2">
          {t.examples.map((example, index) => (
            <motion.button
              key={index}
              onClick={() => handleExampleClick(example)}
              whileHover={{ scale: 1.02, x: 5 }}
              whileTap={{ scale: 0.98 }}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              className={`block w-full text-left px-4 py-2 rounded-lg text-sm transition-colors ${
                darkMode
                  ? 'text-dark-muted hover:text-dark-text hover:bg-dark-accent'
                  : 'text-gray-600 hover:text-gray-800 hover:bg-gray-50'
              }`}
            >
              💭 {example}
            </motion.button>
          ))}
        </div>
      </motion.div>
    </motion.div>
  );
};

export default QueryInput; 
import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Star, DollarSign, Tag } from 'lucide-react';
import { translations } from '../utils/translations';

interface Candy {
  id: string;
  name: string;
  name_fi: string;
  description: string;
  description_fi: string;
  sweetness: number;
  category: string;
  category_fi: string;
  price: number;
  ingredients: string[];
  allergens: string[];
}

interface CandyShowcaseProps {
  language: 'en' | 'fi';
  darkMode: boolean;
}

const CandyShowcase: React.FC<CandyShowcaseProps> = ({ language, darkMode }) => {
  const [candies, setCandies] = useState<Candy[]>([]);
  const [loading, setLoading] = useState(true);
  const [hoveredCandy, setHoveredCandy] = useState<string | null>(null);
  
  const t = translations[language];

  useEffect(() => {
    const fetchCandies = async () => {
      try {
        const response = await fetch('/candies');
        const data = await response.json();
        setCandies(data.candies);
      } catch (error) {
        console.error('Failed to fetch candies:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchCandies();
  }, []);

  const getCandyEmoji = (category: string) => {
    const emojiMap: { [key: string]: string } = {
      'Gummy': '🐻',
      'Chocolate': '🍫',
      'Sour': '🌈',
      'Marshmallow': '☁️',
      'Hard Candy': '🍬',
      'Kumimaiset': '🐻',
      'Suklaa': '🍫',
      'Happamat': '🌈',
      'Vaahtokarkit': '☁️',
      'Kovat Karkit': '🍬'
    };
    return emojiMap[category] || '🍭';
  };

  const getSweetnessColor = (sweetness: number) => {
    if (sweetness >= 8) return 'text-red-500';
    if (sweetness >= 6) return 'text-orange-500';
    if (sweetness >= 4) return 'text-yellow-500';
    return 'text-green-500';
  };

  if (loading) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="flex justify-center py-8"
      >
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
          className="text-4xl"
        >
          🍭
        </motion.div>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.4 }}
      className={`p-6 rounded-2xl ${
        darkMode ? 'bg-dark-surface/50' : 'bg-white/50'
      } backdrop-blur-sm`}
    >
      <div className="text-center mb-6">
        <motion.h2
          className={`text-2xl font-candy font-bold mb-2 ${
            darkMode ? 'text-dark-text' : 'text-gray-800'
          }`}
        >
          {t.showcaseTitle}
        </motion.h2>
        <p className={`text-sm ${
          darkMode ? 'text-dark-muted' : 'text-gray-600'
        }`}>
          {t.showcaseSubtitle}
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {candies.map((candy, index) => (
          <motion.div
            key={candy.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: index * 0.1 }}
            whileHover={{ 
              scale: 1.02, 
              y: -5,
              transition: { duration: 0.2 }
            }}
            onHoverStart={() => setHoveredCandy(candy.id)}
            onHoverEnd={() => setHoveredCandy(null)}
            className={`p-4 rounded-xl cursor-pointer transition-all duration-300 ${
              darkMode 
                ? 'bg-dark-bg/70 hover:bg-dark-bg/90 border border-dark-accent hover:border-candy-pink/50' 
                : 'bg-white/70 hover:bg-white/90 border border-gray-200 hover:border-candy-purple/50'
            } hover:shadow-lg`}
          >
            {/* Candy Header */}
            <div className="flex items-center justify-between mb-3">
              <motion.div
                animate={{ 
                  rotate: hoveredCandy === candy.id ? [0, -10, 10, 0] : 0,
                  scale: hoveredCandy === candy.id ? 1.1 : 1
                }}
                transition={{ duration: 0.3 }}
                className="text-3xl"
              >
                {getCandyEmoji(candy.category)}
              </motion.div>
              
              <div className="flex items-center space-x-1">
                <div className="flex">
                  {[...Array(5)].map((_, i) => (
                    <Star
                      key={i}
                      className={`w-3 h-3 ${
                        i < Math.floor(candy.sweetness / 2)
                          ? getSweetnessColor(candy.sweetness)
                          : darkMode ? 'text-dark-accent' : 'text-gray-300'
                      }`}
                      fill="currentColor"
                    />
                  ))}
                </div>
                <span className={`text-xs ${
                  darkMode ? 'text-dark-muted' : 'text-gray-500'
                }`}>
                  {candy.sweetness}/10
                </span>
              </div>
            </div>

            {/* Candy Name */}
            <h3 className={`font-candy font-bold text-lg mb-2 ${
              darkMode ? 'text-dark-text' : 'text-gray-800'
            }`}>
              {language === 'en' ? candy.name : candy.name_fi}
            </h3>

            {/* Candy Description */}
            <p className={`text-sm mb-3 line-clamp-2 ${
              darkMode ? 'text-dark-muted' : 'text-gray-600'
            }`}>
              {language === 'en' ? candy.description : candy.description_fi}
            </p>

            {/* Candy Details */}
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Tag className="w-4 h-4" />
                  <span className={`text-xs px-2 py-1 rounded-full ${
                    darkMode 
                      ? 'bg-dark-accent text-dark-text' 
                      : 'bg-gray-100 text-gray-700'
                  }`}>
                    {language === 'en' ? candy.category : candy.category_fi}
                  </span>
                </div>
                
                <div className="flex items-center space-x-1">
                  <DollarSign className="w-4 h-4" />
                  <span className={`font-bold ${
                    darkMode ? 'text-candy-pink' : 'text-candy-purple'
                  }`}>
                    ${candy.price}
                  </span>
                </div>
              </div>

              <div className="flex items-center justify-between text-xs">
                <span className={darkMode ? 'text-dark-muted' : 'text-gray-500'}>
                  {t.sweetness}:
                </span>
                <div className="flex items-center space-x-1">
                  <div className={`h-2 w-16 rounded-full ${
                    darkMode ? 'bg-dark-accent' : 'bg-gray-200'
                  }`}>
                    <div 
                      className={`h-full rounded-full ${getSweetnessColor(candy.sweetness)} bg-current`}
                      style={{ width: `${candy.sweetness * 10}%` }}
                    />
                  </div>
                  <span className={getSweetnessColor(candy.sweetness)}>
                    {candy.sweetness}/10
                  </span>
                </div>
              </div>
            </div>

            {/* Hover Effect - Show More Details */}
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ 
                opacity: hoveredCandy === candy.id ? 1 : 0,
                height: hoveredCandy === candy.id ? 'auto' : 0
              }}
              transition={{ duration: 0.2 }}
              className="overflow-hidden"
            >
              <div className="mt-3 pt-3 border-t border-opacity-20 border-gray-400">
                <div className="text-xs space-y-1">
                  <div>
                    <span className={`font-medium ${
                      darkMode ? 'text-dark-muted' : 'text-gray-500'
                    }`}>
                      Ingredients:
                    </span>
                    <p className={`${
                      darkMode ? 'text-dark-text' : 'text-gray-700'
                    }`}>
                      {candy.ingredients.slice(0, 3).join(', ')}
                      {candy.ingredients.length > 3 && '...'}
                    </p>
                  </div>
                  {candy.allergens.length > 0 && candy.allergens[0] !== 'none' && (
                    <div>
                      <span className={`font-medium ${
                        darkMode ? 'text-dark-muted' : 'text-gray-500'
                      }`}>
                        Allergens:
                      </span>
                      <p className={`${
                        darkMode ? 'text-dark-text' : 'text-gray-700'
                      }`}>
                        {candy.allergens.join(', ')}
                      </p>
                    </div>
                  )}
                </div>
              </div>
            </motion.div>
          </motion.div>
        ))}
      </div>

      {/* Fun Stats */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.8 }}
        className={`mt-6 p-4 rounded-xl text-center ${
          darkMode ? 'bg-dark-bg/50' : 'bg-gray-50/50'
        }`}
      >
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div>
            <div className={`text-2xl font-bold ${
              darkMode ? 'text-candy-pink' : 'text-candy-purple'
            }`}>
              {candies.length}
            </div>
            <div className={darkMode ? 'text-dark-muted' : 'text-gray-600'}>
              Total Candies
            </div>
          </div>
          <div>
            <div className={`text-2xl font-bold ${
              darkMode ? 'text-candy-pink' : 'text-candy-purple'
            }`}>
              {Math.max(...candies.map(c => c.sweetness))}/10
            </div>
            <div className={darkMode ? 'text-dark-muted' : 'text-gray-600'}>
              Max Sweetness
            </div>
          </div>
          <div>
            <div className={`text-2xl font-bold ${
              darkMode ? 'text-candy-pink' : 'text-candy-purple'
            }`}>
              ${Math.min(...candies.map(c => c.price)).toFixed(2)}
            </div>
            <div className={darkMode ? 'text-dark-muted' : 'text-gray-600'}>
              Starting From
            </div>
          </div>
          <div>
            <div className={`text-2xl font-bold ${
              darkMode ? 'text-candy-pink' : 'text-candy-purple'
            }`}>
              {new Set(candies.map(c => language === 'en' ? c.category : c.category_fi)).size}
            </div>
            <div className={darkMode ? 'text-dark-muted' : 'text-gray-600'}>
              Categories
            </div>
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
};

export default CandyShowcase; 
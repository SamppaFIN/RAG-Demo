import React from 'react';
import { motion } from 'framer-motion';
import { BookOpen, Code, Cpu, Database, Globe, Palette, Sparkles, Zap } from 'lucide-react';

interface AboutProps {
  darkMode: boolean;
  language: 'en' | 'fi';
  onClose: () => void;
}

const About: React.FC<AboutProps> = ({ darkMode, language, onClose }) => {
  const translations = {
    en: {
      title: "About AI Candy Store RAG Demo",
      subtitle: "An Interactive Learning Experience for Retrieval-Augmented Generation",
      whatIsRag: "What is RAG?",
      ragDescription: "Retrieval-Augmented Generation (RAG) is a cutting-edge AI technique that combines the power of information retrieval with language generation. Instead of relying solely on pre-trained knowledge, RAG systems dynamically fetch relevant information from external sources to provide more accurate, up-to-date, and contextually relevant responses.",
      demoTitle: "About This Demo",
      demoDescription: "This interactive demo walks you through each step of the RAG pipeline using a playful 'AI Candy Store' theme. You can ask questions about candies and sweets, and watch as the system processes your query through five distinct phases:",
      phases: [
        "🔍 Query Processing - Text normalization and tokenization",
        "🧠 Vector Embedding - Converting text to mathematical vectors",
        "🎯 Vector Search - Finding similar content using cosine similarity",
        "📋 Context Preparation - Assembling relevant information",
        "✨ AI Generation - Creating the final response"
      ],
      technologiesTitle: "Technologies Used",
      backendTech: "Backend Technologies",
      frontendTech: "Frontend Technologies",
      aiTech: "AI & Machine Learning",
      close: "Close"
    },
    fi: {
      title: "Tietoa AI Makeiskauppa RAG-demosta",
      subtitle: "Interaktiivinen oppimiskokemus tiedonhakua täydentävälle tekstigeneraatiolle",
      whatIsRag: "Mikä on RAG?",
      ragDescription: "RAG (Retrieval-Augmented Generation) on huippuluokan tekoälyteknologia, joka yhdistää tiedonhaun ja tekstin tuottamisen. Sen sijaan, että luottaisi pelkästään ennalta koulutettuun tietoon, RAG-järjestelmät hakevat dynaamisesti relevanttia tietoa ulkoisista lähteistä tarjotakseen tarkempia, ajantasaisia ja kontekstiin sopivia vastauksia.",
      demoTitle: "Tietoa tästä demosta",
      demoDescription: "Tämä interaktiivinen demo opastaa sinut RAG-prosessin jokaisessa vaiheessa käyttäen leikkisää 'AI Makeiskauppa' -teemaa. Voit kysyä kysymyksiä makeisista ja herkkuista, ja seurata miten järjestelmä käsittelee kyselysi viidessä erillisessä vaiheessa:",
      phases: [
        "🔍 Kyselyn käsittely - Tekstin normalisointi ja tokenisointi",
        "🧠 Vektorin upottaminen - Tekstin muuntaminen matemaattisiksi vektoreiksi",
        "🎯 Vektorihaku - Samankaltaisen sisällön löytäminen kosinisamankaltaisuudella",
        "📋 Kontekstin valmistelu - Relevantin tiedon kokoaminen",
        "✨ Tekoäly-generointi - Lopullisen vastauksen luominen"
      ],
      technologiesTitle: "Käytetyt teknologiat",
      backendTech: "Backend-teknologiat",
      frontendTech: "Frontend-teknologiat",
      aiTech: "Tekoäly ja koneoppiminen",
      close: "Sulje"
    }
  };

  const t = translations[language];

  const technologies = {
    backend: [
      { name: "FastAPI", description: "Modern Python web framework for building APIs", icon: Zap },
      { name: "Python", description: "Programming language for AI and backend development", icon: Code },
      { name: "Pydantic", description: "Data validation and settings management", icon: Database },
      { name: "Uvicorn", description: "ASGI server for running FastAPI applications", icon: Cpu }
    ],
    frontend: [
      { name: "React", description: "JavaScript library for building user interfaces", icon: Code },
      { name: "TypeScript", description: "Typed superset of JavaScript", icon: Code },
      { name: "Tailwind CSS", description: "Utility-first CSS framework", icon: Palette },
      { name: "Framer Motion", description: "Animation library for React", icon: Sparkles }
    ],
    ai: [
      { name: "Vector Embeddings", description: "Text-to-vector conversion for semantic search", icon: Cpu },
      { name: "Cosine Similarity", description: "Mathematical similarity measurement", icon: Database },
      { name: "RAG Architecture", description: "Retrieval-Augmented Generation pattern", icon: BookOpen },
      { name: "Semantic Search", description: "Context-aware information retrieval", icon: Globe }
    ]
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      onClick={onClose}
    >
      <motion.div
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.9, opacity: 0 }}
        onClick={(e) => e.stopPropagation()}
        className={`max-w-4xl w-full max-h-[90vh] overflow-y-auto rounded-2xl shadow-2xl ${
          darkMode 
            ? 'bg-dark-surface text-dark-text' 
            : 'bg-white text-gray-800'
        }`}
      >
        {/* Header */}
        <div className={`px-8 py-6 border-b ${
          darkMode ? 'border-dark-accent' : 'border-gray-200'
        }`}>
          <div className="flex justify-between items-start">
            <div>
              <h1 className="text-3xl font-bold mb-2">{t.title}</h1>
              <p className={`text-lg ${
                darkMode ? 'text-dark-muted' : 'text-gray-600'
              }`}>
                {t.subtitle}
              </p>
            </div>
            <button
              onClick={onClose}
              className={`text-2xl p-2 rounded-full hover:bg-opacity-20 transition-colors ${
                darkMode 
                  ? 'hover:bg-dark-accent text-dark-muted hover:text-dark-text' 
                  : 'hover:bg-gray-100 text-gray-500 hover:text-gray-700'
              }`}
            >
              ×
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="px-8 py-6 space-y-8">
          {/* What is RAG */}
          <section>
            <h2 className="text-2xl font-bold mb-4 flex items-center">
              <BookOpen className="mr-3 text-purple-500" size={28} />
              {t.whatIsRag}
            </h2>
            <p className={`text-lg leading-relaxed ${
              darkMode ? 'text-dark-muted' : 'text-gray-600'
            }`}>
              {t.ragDescription}
            </p>
          </section>

          {/* About Demo */}
          <section>
            <h2 className="text-2xl font-bold mb-4 flex items-center">
              <Sparkles className="mr-3 text-pink-500" size={28} />
              {t.demoTitle}
            </h2>
            <p className={`text-lg leading-relaxed mb-4 ${
              darkMode ? 'text-dark-muted' : 'text-gray-600'
            }`}>
              {t.demoDescription}
            </p>
            <ul className="space-y-2">
              {t.phases.map((phase, index) => (
                <motion.li
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className={`flex items-center text-lg ${
                    darkMode ? 'text-dark-text' : 'text-gray-700'
                  }`}
                >
                  <span className="mr-3">{phase}</span>
                </motion.li>
              ))}
            </ul>
          </section>

          {/* Technologies */}
          <section>
            <h2 className="text-2xl font-bold mb-6 flex items-center">
              <Code className="mr-3 text-blue-500" size={28} />
              {t.technologiesTitle}
            </h2>
            
            <div className="grid md:grid-cols-3 gap-8">
              {/* Backend Technologies */}
              <div>
                <h3 className="text-xl font-semibold mb-4 text-green-500">
                  {t.backendTech}
                </h3>
                <div className="space-y-3">
                  {technologies.backend.map((tech, index) => (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.1 }}
                      className={`p-3 rounded-lg ${
                        darkMode ? 'bg-dark-bg' : 'bg-gray-50'
                      }`}
                    >
                      <div className="flex items-center mb-2">
                        <tech.icon size={20} className="mr-2 text-green-500" />
                        <span className="font-semibold">{tech.name}</span>
                      </div>
                      <p className={`text-sm ${
                        darkMode ? 'text-dark-muted' : 'text-gray-600'
                      }`}>
                        {tech.description}
                      </p>
                    </motion.div>
                  ))}
                </div>
              </div>

              {/* Frontend Technologies */}
              <div>
                <h3 className="text-xl font-semibold mb-4 text-blue-500">
                  {t.frontendTech}
                </h3>
                <div className="space-y-3">
                  {technologies.frontend.map((tech, index) => (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: (index + 4) * 0.1 }}
                      className={`p-3 rounded-lg ${
                        darkMode ? 'bg-dark-bg' : 'bg-gray-50'
                      }`}
                    >
                      <div className="flex items-center mb-2">
                        <tech.icon size={20} className="mr-2 text-blue-500" />
                        <span className="font-semibold">{tech.name}</span>
                      </div>
                      <p className={`text-sm ${
                        darkMode ? 'text-dark-muted' : 'text-gray-600'
                      }`}>
                        {tech.description}
                      </p>
                    </motion.div>
                  ))}
                </div>
              </div>

              {/* AI Technologies */}
              <div>
                <h3 className="text-xl font-semibold mb-4 text-purple-500">
                  {t.aiTech}
                </h3>
                <div className="space-y-3">
                  {technologies.ai.map((tech, index) => (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: (index + 8) * 0.1 }}
                      className={`p-3 rounded-lg ${
                        darkMode ? 'bg-dark-bg' : 'bg-gray-50'
                      }`}
                    >
                      <div className="flex items-center mb-2">
                        <tech.icon size={20} className="mr-2 text-purple-500" />
                        <span className="font-semibold">{tech.name}</span>
                      </div>
                      <p className={`text-sm ${
                        darkMode ? 'text-dark-muted' : 'text-gray-600'
                      }`}>
                        {tech.description}
                      </p>
                    </motion.div>
                  ))}
                </div>
              </div>
            </div>
          </section>
        </div>

        {/* Footer */}
        <div className={`px-8 py-4 border-t ${
          darkMode ? 'border-dark-accent' : 'border-gray-200'
        }`}>
          <div className="flex justify-end">
            <button
              onClick={onClose}
              className={`px-6 py-2 rounded-lg font-semibold transition-colors ${
                darkMode
                  ? 'bg-dark-accent text-dark-text hover:bg-opacity-80'
                  : 'bg-gray-200 text-gray-800 hover:bg-gray-300'
              }`}
            >
              {t.close}
            </button>
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
};

export default About; 
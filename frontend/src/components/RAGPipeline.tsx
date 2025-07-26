import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Search, 
  Brain, 
  Database, 
  Zap, 
  Sparkles, 
  Clock
} from 'lucide-react';
import { translations } from '../utils/translations';

interface RAGStep {
  step: string;
  title: { [key: string]: string };
  description: { [key: string]: string };
  data: any;
  processing_time: number;
}

interface QueryResponse {
  query: string;
  language: string;
  steps: RAGStep[];
  final_answer: { [key: string]: string };
  total_time: number;
}

interface RAGPipelineProps {
  queryResponse: QueryResponse;
  language: 'en' | 'fi';
  darkMode: boolean;
}

const stepIcons = {
  query_processing: Search,
  query_embedding: Brain,
  vector_search: Database,
  context_preparation: Zap,
  ai_generation: Sparkles
};

const stepColors = {
  query_processing: 'from-candy-blue to-candy-green',
  query_embedding: 'from-candy-green to-candy-yellow', 
  vector_search: 'from-candy-yellow to-candy-orange',
  context_preparation: 'from-candy-orange to-candy-pink',
  ai_generation: 'from-candy-pink to-candy-purple'
};

const RAGPipeline: React.FC<RAGPipelineProps> = ({ queryResponse, language, darkMode }) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [showFinalAnswer, setShowFinalAnswer] = useState(false);
  const t = translations[language];

  useEffect(() => {
    // Auto-progress through steps
    const timer = setInterval(() => {
      setCurrentStep((prev) => {
        if (prev < queryResponse.steps.length - 1) {
          return prev + 1;
        } else {
          setShowFinalAnswer(true);
          clearInterval(timer);
          return prev;
        }
      });
    }, 2000);

    return () => clearInterval(timer);
  }, [queryResponse.steps.length]);

  const handleStepClick = (index: number) => {
    setCurrentStep(index);
  };

  const formatTime = (seconds: number) => {
    return `${(seconds * 1000).toFixed(0)}ms`;
  };

  return (
    <div className="space-y-6">
      {/* Query Display */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className={`p-4 rounded-xl ${
          darkMode ? 'bg-dark-surface/50' : 'bg-white/50'
        } backdrop-blur-sm`}
      >
        <div className="flex items-center space-x-3 mb-2">
          <div className="text-2xl">🤔</div>
          <h3 className={`font-candy text-lg ${
            darkMode ? 'text-dark-text' : 'text-gray-800'
          }`}>
            {t.yourQuery}
          </h3>
        </div>
        <p className={`text-lg italic ${
          darkMode ? 'text-candy-pink' : 'text-candy-purple'
        }`}>
          "{queryResponse.query}"
        </p>
      </motion.div>

      {/* Step Navigation */}
      <div className="flex flex-wrap justify-center gap-2 mb-6">
        {queryResponse.steps.map((step, index) => {
          const IconComponent = stepIcons[step.step as keyof typeof stepIcons];
          const isActive = index === currentStep;
          const isCompleted = index < currentStep || showFinalAnswer;
          
          return (
            <motion.button
              key={index}
              onClick={() => handleStepClick(index)}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className={`flex items-center space-x-2 px-4 py-2 rounded-full transition-all ${
                isActive
                  ? darkMode
                    ? 'bg-candy-pink text-white shadow-lg'
                    : 'bg-candy-purple text-white shadow-lg'
                  : isCompleted
                  ? darkMode
                    ? 'bg-dark-accent text-dark-text'
                    : 'bg-gray-200 text-gray-700'
                  : darkMode
                  ? 'bg-dark-surface text-dark-muted'
                  : 'bg-gray-100 text-gray-500'
              }`}
            >
              <IconComponent className="w-4 h-4" />
              <span className="text-sm font-medium hidden sm:inline">
                {step.title[language]}
              </span>
              <span className="text-xs">
                {index + 1}
              </span>
            </motion.button>
          );
        })}
      </div>

      {/* Current Step Display */}
      <AnimatePresence mode="wait">
        {currentStep < queryResponse.steps.length && (
          <motion.div
            key={currentStep}
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -50 }}
            transition={{ duration: 0.5 }}
            className={`p-6 rounded-2xl ${
              darkMode ? 'bg-dark-surface/70' : 'bg-white/70'
            } backdrop-blur-sm`}
          >
            <div className="space-y-4">
              {/* Step Header */}
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                    className={`p-3 rounded-full bg-gradient-to-r ${
                      stepColors[queryResponse.steps[currentStep].step as keyof typeof stepColors]
                    }`}
                  >
                    {React.createElement(
                      stepIcons[queryResponse.steps[currentStep].step as keyof typeof stepIcons],
                      { className: "w-6 h-6 text-white" }
                    )}
                  </motion.div>
                  <div>
                    <h3 className={`text-xl font-candy font-bold ${
                      darkMode ? 'text-dark-text' : 'text-gray-800'
                    }`}>
                      {queryResponse.steps[currentStep].title[language]}
                    </h3>
                    <div className="flex items-center space-x-2 text-sm">
                      <Clock className="w-4 h-4" />
                      <span className={darkMode ? 'text-dark-muted' : 'text-gray-600'}>
                        {formatTime(queryResponse.steps[currentStep].processing_time)}
                      </span>
                    </div>
                  </div>
                </div>
                
                <div className={`text-sm px-3 py-1 rounded-full ${
                  darkMode ? 'bg-dark-accent text-dark-text' : 'bg-gray-100 text-gray-700'
                }`}>
                  {currentStep + 1} / {queryResponse.steps.length}
                </div>
              </div>

              {/* Step Description */}
              <p className={`text-base ${
                darkMode ? 'text-dark-muted' : 'text-gray-600'
              }`}>
                {queryResponse.steps[currentStep].description[language]}
              </p>

              {/* Step Data Visualization */}
              <div className={`p-4 rounded-xl ${
                darkMode ? 'bg-dark-bg/50' : 'bg-gray-50/50'
              }`}>
                <StepDataVisualization 
                  step={queryResponse.steps[currentStep]}
                  language={language}
                  darkMode={darkMode}
                />
              </div>

              {/* Progress Animation */}
              <div className="relative">
                <div className={`h-2 rounded-full ${
                  darkMode ? 'bg-dark-accent' : 'bg-gray-200'
                }`}>
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${((currentStep + 1) / queryResponse.steps.length) * 100}%` }}
                    transition={{ duration: 0.5 }}
                    className={`h-full rounded-full bg-gradient-to-r ${
                      stepColors[queryResponse.steps[currentStep].step as keyof typeof stepColors]
                    }`}
                  />
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Final Answer */}
      <AnimatePresence>
        {showFinalAnswer && (
          <motion.div
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            transition={{ duration: 0.6, type: "spring" }}
            className={`p-6 rounded-2xl ${
              darkMode 
                ? 'bg-gradient-to-r from-dark-surface to-dark-accent' 
                : 'bg-gradient-to-r from-candy-purple/10 to-candy-pink/10'
            } border-2 ${
              darkMode ? 'border-candy-pink/30' : 'border-candy-purple/30'
            }`}
          >
            <div className="space-y-4">
              <div className="flex items-center space-x-3">
                <motion.div
                  animate={{ y: [0, -10, 0] }}
                  transition={{ duration: 1, repeat: Infinity }}
                  className="text-3xl"
                >
                  🎉
                </motion.div>
                <h3 className={`text-2xl font-candy font-bold ${
                  darkMode ? 'text-candy-pink' : 'text-candy-purple'
                }`}>
                  {t.aiAnswer}
                </h3>
              </div>
              
              <div className={`text-lg leading-relaxed ${
                darkMode ? 'text-dark-text' : 'text-gray-800'
              }`}>
                {queryResponse.final_answer[language]}
              </div>

              <div className="flex flex-wrap gap-4 text-sm">
                <div className={`flex items-center space-x-2 ${
                  darkMode ? 'text-dark-muted' : 'text-gray-600'
                }`}>
                  <Clock className="w-4 h-4" />
                  <span>{t.totalTime}: {formatTime(queryResponse.total_time)}</span>
                </div>
                <div className={`flex items-center space-x-2 ${
                  darkMode ? 'text-dark-muted' : 'text-gray-600'
                }`}>
                  <Database className="w-4 h-4" />
                  <span>{t.sources}: {queryResponse.steps.length} steps</span>
                </div>
              </div>

              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => window.location.reload()}
                className={`mt-4 px-6 py-3 rounded-xl font-candy font-semibold transition-all ${
                  darkMode
                    ? 'bg-gradient-to-r from-candy-pink to-candy-purple text-white hover:shadow-lg'
                    : 'bg-gradient-to-r from-candy-purple to-candy-pink text-white hover:shadow-lg'
                }`}
              >
                {t.askAnother}
              </motion.button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

// Component to visualize step-specific data
const StepDataVisualization: React.FC<{
  step: RAGStep;
  language: 'en' | 'fi';
  darkMode: boolean;
}> = ({ step, language, darkMode }) => {
  const renderStepData = () => {
    switch (step.step) {
      case 'query_processing':
        return (
          <div className="space-y-4">
            <div className="grid grid-cols-1 gap-3">
              <div>
                <span className={`text-sm font-semibold ${darkMode ? 'text-dark-muted' : 'text-gray-600'}`}>
                  Original Query:
                </span>
                <div className={`mt-1 p-2 rounded font-mono text-sm ${darkMode ? 'bg-dark-bg text-dark-text' : 'bg-gray-50 text-gray-800'}`}>
                  "{step.data.original_query}"
                </div>
              </div>
              
              {step.data.tokenization && (
                <div>
                  <span className={`text-sm font-semibold ${darkMode ? 'text-dark-muted' : 'text-gray-600'}`}>
                    Tokenization Analysis:
                  </span>
                  <div className="mt-2 space-y-2 text-xs">
                    <div>
                      <strong>Raw tokens:</strong> [{step.data.tokenization.raw_tokens?.join(', ') || 'N/A'}]
                    </div>
                    <div>
                      <strong>Filtered tokens:</strong> [{step.data.tokenization.filtered_tokens?.join(', ') || 'N/A'}]
                    </div>
                    <div>
                      <strong>Removed stop words:</strong> [{step.data.tokenization.removed_stop_words?.join(', ') || 'none'}]
                    </div>
                    <div>
                      <strong>Final token count:</strong> {step.data.tokenization.token_count || 0}
                    </div>
                  </div>
                </div>
              )}

              {step.data.preprocessing_steps && (
                <div>
                  <span className={`text-sm font-semibold ${darkMode ? 'text-dark-muted' : 'text-gray-600'}`}>
                    Processing Pipeline:
                  </span>
                  <div className="mt-2">
                    {step.data.preprocessing_steps.map((processStep: string, index: number) => (
                      <div key={index} className="text-xs py-1">
                        {processStep}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <div className="flex justify-between items-center">
                <span className={darkMode ? 'text-dark-muted' : 'text-gray-600'}>
                  Language:
                </span>
                <span className={darkMode ? 'text-dark-text' : 'text-gray-800'}>
                  {step.data.language === 'en' ? '🇬🇧 English' : '🇫🇮 Finnish'}
                </span>
              </div>
            </div>
          </div>
        );

      case 'query_embedding':
        return (
          <div className="space-y-4">
            {/* Model Information */}
            {step.data.model_info && (
              <div className={`p-3 rounded-lg ${darkMode ? 'bg-dark-bg' : 'bg-gray-50'}`}>
                <div className="text-xs space-y-1">
                  <div><strong>Model:</strong> {step.data.model_info.model}</div>
                  <div><strong>Architecture:</strong> {step.data.model_info.architecture}</div>
                  <div><strong>Dimensions:</strong> {step.data.model_info.dimensions}</div>
                  <div><strong>Max Sequence Length:</strong> {step.data.model_info.max_sequence_length}</div>
                </div>
              </div>
            )}

            {/* Vector Properties */}
            {step.data.embedding_vector && (
              <div className="space-y-3">
                <span className={`text-sm font-semibold ${darkMode ? 'text-dark-muted' : 'text-gray-600'}`}>
                  Vector Analysis:
                </span>
                <div className="grid grid-cols-2 gap-4 text-xs">
                  <div>
                    <strong>Magnitude:</strong> {step.data.embedding_vector.magnitude}
                  </div>
                  <div>
                    <strong>Sparsity:</strong> {step.data.embedding_vector.sparsity}
                  </div>
                </div>
                
                <div>
                  <strong className="text-xs">Sample Values (first 10 dimensions):</strong>
                  <div className={`mt-1 p-2 rounded font-mono text-xs overflow-x-auto ${darkMode ? 'bg-dark-bg' : 'bg-gray-50'}`}>
                    [{step.data.embedding_vector.sample_values?.map((val: number) => val.toFixed(4)).join(', ') || 'N/A'}...]
                  </div>
                </div>
              </div>
            )}

            {/* Statistical Properties */}
            {step.data.vector_properties && (
              <div className="space-y-2">
                <span className={`text-sm font-semibold ${darkMode ? 'text-dark-muted' : 'text-gray-600'}`}>
                  Statistical Properties:
                </span>
                <div className="grid grid-cols-2 gap-2 text-xs">
                  <div><strong>Min:</strong> {step.data.vector_properties.min_value?.toFixed(4)}</div>
                  <div><strong>Max:</strong> {step.data.vector_properties.max_value?.toFixed(4)}</div>
                  <div><strong>Mean:</strong> {step.data.vector_properties.mean?.toFixed(4)}</div>
                  <div><strong>Std Dev:</strong> {step.data.vector_properties.std_dev?.toFixed(4)}</div>
                </div>
              </div>
            )}

            {/* Semantic Encoding */}
            {step.data.semantic_encoding && (
              <div className={`text-xs ${darkMode ? 'text-dark-muted' : 'text-gray-600'} italic`}>
                🧠 {step.data.semantic_encoding}
              </div>
            )}
          </div>
        );

      case 'vector_search':
        return (
          <div className="space-y-4">
            {/* Search Algorithm Info */}
            <div className={`p-3 rounded-lg ${darkMode ? 'bg-dark-bg' : 'bg-gray-50'}`}>
              <div className="text-xs font-mono">
                <div><strong>Method:</strong> {step.data.search_algorithm?.method || 'Cosine Similarity'}</div>
                <div><strong>Formula:</strong> {step.data.search_algorithm?.formula || 'cos(θ) = (A·B) / (||A|| × ||B||)'}</div>
                <div><strong>Database Size:</strong> {step.data.search_algorithm?.database_size || 'N/A'}</div>
              </div>
            </div>

            {/* Similarity Distribution */}
            {step.data.similarity_distribution && (
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className={darkMode ? 'text-dark-muted' : 'text-gray-600'}>Highest Score:</span>
                  <span className={`ml-2 font-bold ${darkMode ? 'text-dark-text' : 'text-gray-800'}`}>
                    {(step.data.similarity_distribution.highest_score || 0).toFixed(3)}
                  </span>
                </div>
                <div>
                  <span className={darkMode ? 'text-dark-muted' : 'text-gray-600'}>Average:</span>
                  <span className={`ml-2 font-bold ${darkMode ? 'text-dark-text' : 'text-gray-800'}`}>
                    {(step.data.similarity_distribution.average_score || 0).toFixed(3)}
                  </span>
                </div>
              </div>
            )}

            {/* Top Matches */}
            <div className="space-y-2">
              <span className={`text-sm font-semibold ${darkMode ? 'text-dark-muted' : 'text-gray-600'}`}>
                Top Matches:
              </span>
              {step.data.top_matches && step.data.top_matches.length > 0 ? (
                step.data.top_matches.map((match: any, index: number) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className={`p-3 rounded-lg border ${
                      darkMode ? 'bg-dark-surface border-dark-accent' : 'bg-white border-gray-200'
                    }`}
                  >
                    <div className="flex justify-between items-start mb-2">
                      <div className="flex items-center space-x-2">
                        <span className={`text-xs px-2 py-1 rounded-full ${
                          darkMode ? 'bg-dark-accent text-dark-text' : 'bg-gray-100 text-gray-600'
                        }`}>
                          #{match.rank || index + 1}
                        </span>
                        <span className="font-medium text-sm">
                          {match.candy_name}
                        </span>
                      </div>
                      <span className={`text-sm font-bold ${
                        (match.cosine_similarity || match.similarity_score || 0) > 0.8 
                          ? 'text-green-500' 
                          : (match.cosine_similarity || match.similarity_score || 0) > 0.6 
                          ? 'text-yellow-500' 
                          : 'text-gray-500'
                      }`}>
                        {((match.cosine_similarity || match.similarity_score || 0) * 100).toFixed(1)}%
                      </span>
                    </div>
                    
                    <div className="text-xs space-y-1">
                      {match.similarity_explanation && (
                        <div className={`font-mono ${darkMode ? 'text-dark-muted' : 'text-gray-500'}`}>
                          {match.similarity_explanation}
                        </div>
                      )}
                      {match.matched_tokens && match.matched_tokens.length > 0 && (
                        <div>
                          <span className={darkMode ? 'text-dark-muted' : 'text-gray-500'}>
                            Matched tokens: 
                          </span>
                          <span className={`ml-1 ${darkMode ? 'text-dark-text' : 'text-gray-700'}`}>
                            [{match.matched_tokens.join(', ')}]
                          </span>
                        </div>
                      )}
                      <div>
                        <span className={darkMode ? 'text-dark-muted' : 'text-gray-500'}>
                          Category: 
                        </span>
                        <span className={`ml-1 ${darkMode ? 'text-dark-text' : 'text-gray-700'}`}>
                          {match.category}
                        </span>
                      </div>
                    </div>
                  </motion.div>
                ))
              ) : (
                <div className={`text-sm ${darkMode ? 'text-dark-muted' : 'text-gray-500'}`}>
                  No matches found
                </div>
              )}
            </div>

            {/* Vector Space Analysis */}
            {step.data.vector_space_analysis && (
              <div className={`text-xs ${darkMode ? 'text-dark-muted' : 'text-gray-600'} italic`}>
                🔬 {step.data.vector_space_analysis}
              </div>
            )}
          </div>
        );

      case 'context_preparation':
        return (
          <div className="space-y-4">
            {/* Context Window Information */}
            {step.data.context_window && (
              <div className={`p-3 rounded-lg ${darkMode ? 'bg-dark-bg' : 'bg-gray-50'}`}>
                <div className="text-xs space-y-1">
                  <div><strong>Token Budget:</strong> {step.data.context_window.total_tokens}/{step.data.context_window.max_context_length}</div>
                  <div><strong>Utilization:</strong> {step.data.context_window.utilization}</div>
                  <div><strong>Chunks Included:</strong> {step.data.context_window.chunks_included}</div>
                </div>
              </div>
            )}

            {/* RAG Strategy */}
            {step.data.rag_strategy && (
              <div className="space-y-2">
                <span className={`text-sm font-semibold ${darkMode ? 'text-dark-muted' : 'text-gray-600'}`}>
                  RAG Strategy:
                </span>
                <div className="text-xs space-y-1">
                  <div><strong>Retrieval Count:</strong> {step.data.rag_strategy.retrieval_count}</div>
                  <div><strong>Selection Method:</strong> {step.data.rag_strategy.context_selection}</div>
                  <div><strong>Chunk Size:</strong> {step.data.rag_strategy.chunk_size}</div>
                  <div><strong>Metadata:</strong> [{step.data.rag_strategy.metadata_included?.join(', ') || 'N/A'}]</div>
                </div>
              </div>
            )}

            {/* Context Structure */}
            {step.data.context_structure && step.data.context_structure.length > 0 && (
              <div className="space-y-2">
                <span className={`text-sm font-semibold ${darkMode ? 'text-dark-muted' : 'text-gray-600'}`}>
                  Context Chunks:
                </span>
                <div className="space-y-2">
                  {step.data.context_structure.map((chunk: any, index: number) => (
                    <div key={index} className={`p-2 rounded border text-xs ${
                      darkMode ? 'bg-dark-surface border-dark-accent' : 'bg-white border-gray-200'
                    }`}>
                      <div className="flex justify-between items-center mb-1">
                        <span className="font-semibold">{chunk.candy_name}</span>
                        <span className={`px-2 py-1 rounded-full text-xs ${
                          darkMode ? 'bg-dark-accent text-dark-text' : 'bg-gray-100 text-gray-600'
                        }`}>
                          Rank #{chunk.similarity_rank}
                        </span>
                      </div>
                      <div className="text-xs space-y-1">
                        <div><strong>Tokens:</strong> {chunk.token_count}</div>
                        <div><strong>Metadata:</strong> {chunk.metadata}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Context Preview */}
            {step.data.context_preview && (
              <div className="space-y-2">
                <span className={`text-sm font-semibold ${darkMode ? 'text-dark-muted' : 'text-gray-600'}`}>
                  Context Preview:
                </span>
                <div className={`p-2 rounded font-mono text-xs ${darkMode ? 'bg-dark-bg text-dark-text' : 'bg-gray-50 text-gray-800'} max-h-32 overflow-y-auto`}>
                  {step.data.context_preview}
                </div>
              </div>
            )}
          </div>
        );

      case 'ai_generation':
        return (
          <div className="space-y-4">
            {/* Generation Model Info */}
            {step.data.generation_model && (
              <div className={`p-3 rounded-lg ${darkMode ? 'bg-dark-bg' : 'bg-gray-50'}`}>
                <div className="text-xs space-y-1">
                  <div><strong>Approach:</strong> {step.data.generation_model.approach}</div>
                  <div><strong>Context Injection:</strong> {step.data.generation_model.context_injection}</div>
                  <div><strong>Fallback Strategy:</strong> {step.data.generation_model.fallback_strategy}</div>
                  <div><strong>Response Format:</strong> {step.data.generation_model.response_format}</div>
                </div>
              </div>
            )}

            {/* Prompt Engineering */}
            {step.data.prompt_engineering && (
              <div className="space-y-2">
                <span className={`text-sm font-semibold ${darkMode ? 'text-dark-muted' : 'text-gray-600'}`}>
                  Prompt Engineering:
                </span>
                <div className="text-xs space-y-2">
                  <div>
                    <strong>System Prompt:</strong>
                    <div className={`mt-1 p-2 rounded ${darkMode ? 'bg-dark-surface' : 'bg-white'}`}>
                      {step.data.prompt_engineering.system_prompt}
                    </div>
                  </div>
                  <div>
                    <strong>Context Template:</strong>
                    <div className={`mt-1 p-2 rounded font-mono ${darkMode ? 'bg-dark-surface' : 'bg-white'}`}>
                      {step.data.prompt_engineering.context_template}
                    </div>
                  </div>
                  <div>
                    <strong>Query Processing:</strong> {step.data.prompt_engineering.user_query_processing}
                  </div>
                  <div>
                    <strong>Response Strategy:</strong> {step.data.prompt_engineering.response_strategy}
                  </div>
                </div>
              </div>
            )}

            {/* Output Analysis */}
            {step.data.output_analysis && (
              <div className="space-y-2">
                <span className={`text-sm font-semibold ${darkMode ? 'text-dark-muted' : 'text-gray-600'}`}>
                  Output Analysis:
                </span>
                <div className="grid grid-cols-2 gap-4 text-xs">
                  <div><strong>Characters:</strong> {step.data.output_analysis.character_count}</div>
                  <div><strong>Words:</strong> {step.data.output_analysis.word_count}</div>
                  <div><strong>Sources:</strong> {step.data.output_analysis.sources_referenced}</div>
                  <div><strong>Confidence:</strong> {(step.data.output_analysis.confidence_score * 100).toFixed(1)}%</div>
                </div>
                <div>
                  <strong>Generation Method:</strong> {step.data.output_analysis.generation_method}
                </div>
              </div>
            )}

            {/* RAG Effectiveness */}
            {step.data.rag_effectiveness && (
              <div className="space-y-2">
                <span className={`text-sm font-semibold ${darkMode ? 'text-dark-muted' : 'text-gray-600'}`}>
                  RAG Effectiveness:
                </span>
                <div className="text-xs space-y-1">
                  <div><strong>Retrieval Success:</strong> {step.data.rag_effectiveness.retrieval_success ? '✅ Yes' : '❌ No'}</div>
                  <div><strong>Context Utilization:</strong> {step.data.rag_effectiveness.context_utilization}</div>
                  <div><strong>Semantic Matching:</strong> {step.data.rag_effectiveness.semantic_matching}</div>
                  <div><strong>Response Grounding:</strong> {step.data.rag_effectiveness.response_grounding}</div>
                </div>
              </div>
            )}
          </div>
        );

      default:
        return <div>Processing...</div>;
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.3 }}
    >
      {renderStepData()}
    </motion.div>
  );
};

export default RAGPipeline; 
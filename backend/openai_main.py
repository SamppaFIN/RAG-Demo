from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import asyncio
import logging

from openai_rag_service import OpenAIRAGService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Candy Store RAG Demo with OpenAI",
    description="Interactive Retrieval-Augmented Generation demo with OpenAI integration and playful candy theme",
    version="2.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG service
try:
    rag_service = OpenAIRAGService()
    logger.info("OpenAI RAG Service initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize OpenAI RAG Service: {e}")
    # Fallback to simple service if OpenAI fails
    from simple_rag_service import SimpleRAGService
    rag_service = SimpleRAGService()
    logger.info("Fallback to Simple RAG Service")

# Request/Response models
class QueryRequest(BaseModel):
    query: str
    language: str = "en"

class QueryResponse(BaseModel):
    query: str
    language: str
    steps: List[Dict[str, Any]]
    final_answer: Dict[str, str]
    total_time: float

class CandyResponse(BaseModel):
    candies: List[Dict[str, Any]]

class ResetResponse(BaseModel):
    status: str
    message: str

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "🍭 AI Candy Store RAG Demo API",
        "version": "2.0.0",
        "description": "Interactive RAG pipeline demonstration with OpenAI integration",
        "endpoints": [
            "/query - Process RAG queries with step-by-step breakdown",
            "/candies - Get all available candies in the demo",
            "/reset - Reset the demo state"
        ],
        "features": [
            "✨ Real OpenAI integration (GPT-3.5-turbo + text-embedding-3-small)",
            "🔍 Step-by-step RAG pipeline visualization",
            "🌍 Bilingual support (English & Finnish)",
            "🍬 Educational candy-themed content",
            "🎯 Vector similarity search with cosine similarity"
        ]
    }

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Process a user query through the RAG pipeline.
    
    Returns detailed step-by-step information about:
    - Query processing and tokenization
    - OpenAI embedding generation
    - Vector similarity search
    - Context preparation
    - AI response generation
    """
    try:
        logger.info(f"Processing query: '{request.query}' in language: {request.language}")
        
        result = await rag_service.process_query_with_steps(
            query=request.query,
            language=request.language
        )
        
        logger.info(f"Query processed successfully in {result['total_time']:.2f}s")
        return QueryResponse(**result)
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.get("/candies", response_model=CandyResponse)
async def get_candies():
    """
    Get all available candies in the demo database.
    
    Returns comprehensive information about each candy including:
    - Name, category, and description
    - Sweetness level and flavor profile
    - Texture and origin information
    """
    try:
        candies = await rag_service.get_all_candies()
        logger.info(f"Retrieved {len(candies)} candies")
        return CandyResponse(candies=candies)
        
    except Exception as e:
        logger.error(f"Error retrieving candies: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving candies: {str(e)}")

@app.post("/reset", response_model=ResetResponse)
async def reset_demo():
    """
    Reset the demo state.
    
    Clears any cached data and prepares for a fresh demo session.
    """
    try:
        result = await rag_service.reset_demo()
        logger.info("Demo reset successfully")
        return ResetResponse(**result)
        
    except Exception as e:
        logger.error(f"Error resetting demo: {e}")
        raise HTTPException(status_code=500, detail=f"Error resetting demo: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "AI Candy Store RAG Demo",
        "version": "2.0.0",
        "openai_integration": "active" if hasattr(rag_service, 'client') else "inactive"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info") 
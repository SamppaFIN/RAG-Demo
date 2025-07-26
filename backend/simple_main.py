from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import asyncio
import logging

from simple_rag_service import SimpleRAGService

# Initialize FastAPI
app = FastAPI(
    title="AI Candy Store RAG Demo",
    description="Interactive Retrieval-Augmented Generation demo with a playful candy theme",
    version="1.0.0"
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
rag_service = SimpleRAGService()

# Pydantic models
class QueryRequest(BaseModel):
    query: str
    language: str = "en"  # "en" or "fi"

class RAGStepResponse(BaseModel):
    step: str
    title: Dict[str, str]  # {"en": "title", "fi": "title"}
    description: Dict[str, str]
    data: Any
    processing_time: float

class RAGResponse(BaseModel):
    query: str
    language: str
    steps: List[RAGStepResponse]
    final_answer: Dict[str, str]
    total_time: float

@app.on_event("startup")
async def startup_event():
    """Initialize the RAG service with sample data"""
    await rag_service.initialize()

@app.get("/")
async def root():
    return {"message": "Welcome to the AI Candy Store RAG Demo! 🍭"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "AI Candy Store RAG API"}

@app.post("/query", response_model=RAGResponse)
async def process_query(request: QueryRequest):
    """Process a query through the complete RAG pipeline with step-by-step visualization"""
    try:
        start_time = asyncio.get_event_loop().time()
        
        # Process query through RAG pipeline
        result = await rag_service.process_query_with_steps(request.query, request.language)
        
        end_time = asyncio.get_event_loop().time()
        total_time = end_time - start_time
        
        return RAGResponse(
            query=request.query,
            language=request.language,
            steps=result["steps"],
            final_answer=result["final_answer"],
            total_time=total_time
        )
    
    except Exception as e:
        logging.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.get("/candies")
async def get_candies():
    """Get all available candy data for display"""
    try:
        candies = await rag_service.get_all_candies()
        return {"candies": candies}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching candies: {str(e)}")

@app.post("/reset")
async def reset_demo():
    """Reset the demo state"""
    try:
        await rag_service.reset()
        return {"message": "Demo reset successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error resetting demo: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
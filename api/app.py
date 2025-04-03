from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn
from src.agent import PetitionAnalyzer
from api.model import PetitionRequest, PetitionResponse

app = FastAPI(
    title="Petition Analysis API",
    description="API for analyzing government petitions in the Indian context",
    version="1.0.0"
)

petition_analyzer = PetitionAnalyzer()

@app.get("/")
async def root():
    """Root endpoint that returns API information."""
    return {
        "message": "Welcome to the Petition Analysis API",
        "version": "1.0.0",
        "endpoints": {
            "/analyze": "POST - Analyze a petition"
        }
    }

@app.post("/analyze", response_model=PetitionResponse)
async def analyze_petition(request: PetitionRequest):
    """
    Analyze a petition and return structured results.
    """
    try:
        result = petition_analyzer.get_response(
            petition_text=request.petition_text,
            additional_context=request.additional_context
        )
        
        result_dict = result.dict()
        
        return PetitionResponse(
            success=True,
            data=result_dict
        )
    except Exception as e:
        return PetitionResponse(
            success=False,
            error=str(e)
        )

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy",
            "message": "The API is running smoothly."}

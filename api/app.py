from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import numpy as np
import os
import ktrain

# Local imports
from src.agent import PetitionAnalyzer
from api.model import PetitionRequest, PetitionResponse

# --- Environment & Predictor ---
os.environ['TF_USE_LEGACY_KERAS'] = 'True'
predictor_file_path = r'D:\FOML-MiniProject\twitter_disaster_predictor'
predictor = ktrain.load_predictor(predictor_file_path)

# --- FastAPI app setup ---
app = FastAPI(
    title="Petition Analysis API",
    description="API for analyzing government petitions in the Indian context",
    version="1.0.0"
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

petition_analyzer = PetitionAnalyzer()

# --- Utilities ---
def make_serializable(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, np.float32):
        return float(obj)
    if isinstance(obj, np.float64):
        return float(obj)
    return obj

# --- Endpoints ---

@app.get("/")
async def root():
    """Asynchronous function that returns a welcome message and API version details.

    Args:
        None(None): No parameters are required.

    Returns:
        dict: A dictionary containing a welcome message, API version, and available endpoints.

    Raises:
        Exception: Generic exception for any unexpected errors during execution.
    """
    return {
        "message": "Welcome to the Petition Analysis API",
        "version": "1.0.0",
        "endpoints": {
            "/analyze": "POST - Analyze a petition using LangChain",
            "/verify": "POST - Verify if a petition is disaster-related"
        }
    }

@app.post("/analyze", response_model=PetitionResponse)
async def analyze_petition(request: PetitionRequest):
    """Analyzes a given petition asynchronously.

    Args:
        request(PetitionRequest): The petition request object containing the petition text and additional context.

    Returns:
        PetitionResponse: A PetitionResponse object indicating success or failure, containing result data or error message.

    Raises:
        Exception: Any exception raised during petition analysis.
    """
    try:
        result = petition_analyzer.get_response(
            petition_text=request.petition_text,
            additional_context=request.additional_context
        )
        return PetitionResponse(success=True, data=result.dict())
    except Exception as e:
        return PetitionResponse(success=False, error=str(e))

# New input model for verification
class VerificationRequest(BaseModel):
    petition: str

@app.post("/verify")
async def verify_petition(request: VerificationRequest):
    """Verifies a petition asynchronously using a prediction model.

    Args:
        request(VerificationRequest): Request object containing the petition to verify.

    Returns:
        dict: A dictionary containing the original petition text, prediction result, and confidence score. Returns None if an error occurs.

    Raises:
        HTTPException: Raises HTTPException with status code 400 if the petition is empty. Raises HTTPException with status code 500 if any other error occurs during processing.
        Exception: Any unhandled exception during prediction will result in an HTTP 500 error.
    """
    try:
        petition = request.petition

        if not petition.strip():
            raise HTTPException(status_code=400, detail="Petition must be a non-empty string")

        prediction = predictor.predict(petition)
        confidence = predictor.predict_proba(petition)

        return {
            'text': petition,
            'prediction': make_serializable(prediction),
            'confidence': make_serializable(confidence),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "The API is running smoothly."}

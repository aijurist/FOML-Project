from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class PetitionAnalysisOutput(BaseModel):
    '''Model for Petition Analysis Output'''
    
    # Metadata
    petition_id: str = Field(..., description="Unique identifier for the petition")
    title: str = Field(..., description="Title of the petition")
    description: str = Field(..., description="Detailed description of the petition")
    category: str = Field(..., description="Main department assigned to the petition")
    sub_category: Optional[str] = Field(None, description="Specific classification under the department")
    
    urgency_level: str = Field(..., description="Urgency level: Low, Medium, High, Critical")
    priority_score: float = Field(..., description="Numerical priority rating (0 to 1)")
    keywords: List[str] = Field(..., description="Extracted key phrases")
    sentiment: str = Field(..., description="Sentiment of the petition: Positive, Neutral, Negative")
    
    # Duplicate Detection
    duplicate_detected: bool = Field(..., description="Indicates if a similar petition exists")
    duplicate_petition_id: Optional[str] = Field(None, description="Reference ID of the duplicate petition")
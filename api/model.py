from pydantic import BaseModel
from typing import Optional, Dict, Any

class PetitionRequest(BaseModel):
    petition_text: str
    additional_context: Optional[str] = ""

# Response model
class PetitionResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
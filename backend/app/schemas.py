
from typing import Dict, Any, Optional
from pydantic import BaseModel


class CalorieAnalysisRequest(BaseModel):
    description: str
    image_features: Dict[str, Any]


class Macros(BaseModel):
    protein_g: Optional[float] = None
    carbs_g: Optional[float] = None
    fats_g: Optional[float] = None


class CalorieAnalysisResponse(BaseModel):
    image_features: Dict[str, Any]
    model_name: str
    total_calories: Optional[float] = None
    macros: Optional[Macros] = None
    reasoning: Optional[str] = None
    suggestions: Optional[Any] = None
    raw_response: Optional[str] = None

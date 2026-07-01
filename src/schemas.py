from pydantic import BaseModel, Field
from typing import List, Literal


class PredictionOutput(BaseModel):
    image_quality: Literal["good", "limited", "poor"]
    predicted_class: Literal["normal", "suspected_opacity", "uncertain"]
    confidence: float = Field(ge=0.0, le=1.0)
    visual_evidence: List[str]
    justification: str
    limitations: List[str]
    warning: str
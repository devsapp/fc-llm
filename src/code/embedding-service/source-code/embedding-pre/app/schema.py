from typing import List, Dict, Any
from pydantic import BaseModel


class EmbeddingRequest(BaseModel):
    sentences: List[str]


class EmbeddingResponse(BaseModel):
    embeddings: List[List[float]]


class SimilarityResponse(BaseModel):
    score: List[Dict[str, Any]]

from typing import List, Union, Dict, Any
from pydantic import BaseModel, Field


class EmbeddingRequest(BaseModel):
    sentences: Union[str, List[str]]=Field(alias="input")


class EmbeddingResponse(BaseModel):
    data: List[Dict[str, Any]]
    object:str


class SimilarityResponse(BaseModel):
    score: List[Dict[str, Any]]

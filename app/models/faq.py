from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid

class FAQ(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    question: str
    answer: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class FAQCreate(BaseModel):
    question: str
    answer: str

class FAQUpdate(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None

class QueryLog(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    query: str
    response: str
    score: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

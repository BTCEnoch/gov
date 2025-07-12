"""Schemas for the interview system."""
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class InterviewQuestion:
    """Schema for a single interview question."""
    id: str
    question: str
    description: str
    options: List[str]

@dataclass
class QuestionCategory:
    """Schema for a category of questions."""
    name: str
    description: str
    questions: List[InterviewQuestion]

@dataclass
class InterviewResponse:
    """Schema for a response to an interview question."""
    question_id: str
    selected_option: str
    notes: Optional[str] = None

@dataclass
class InterviewSession:
    """Schema for an interview session."""
    governor_id: str
    responses: List[InterviewResponse]
    timestamp: str
    version: str = "1.0" 
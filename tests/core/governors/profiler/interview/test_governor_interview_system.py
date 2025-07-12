"""Tests for the governor interview system."""
import json
import pytest
from pathlib import Path
from datetime import datetime

from core.governors.profiler.interview.governor_interview_system import GovernorInterviewSystem
from core.governors.profiler.interview.schemas.interview_schemas import (
    InterviewQuestion,
    QuestionCategory,
    InterviewResponse,
    InterviewSession
)

@pytest.fixture
def test_questions():
    """Sample interview questions for testing."""
    return {
        "version": "1.0",
        "categories": {
            "form": {
                "name": "Form and Manifestation",
                "description": "Basic form characteristics",
                "questions": [
                    {
                        "id": "form_base_type",
                        "question": "What is the primary form type?",
                        "description": "Basic form type",
                        "options": ["geometric", "organic", "abstract"]
                    },
                    {
                        "id": "form_complexity",
                        "question": "How complex is the form?",
                        "description": "Form complexity level",
                        "options": ["simple", "moderate", "complex"]
                    }
                ]
            }
        }
    }

@pytest.fixture
def test_dir(tmp_path):
    """Create test directory structure."""
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()
    
    questions_file = templates_dir / "interview_questions.json"
    with open(questions_file, 'w') as f:
        json.dump(test_questions(), f)
        
    return tmp_path

def test_load_interview_categories(test_dir):
    """Test loading interview categories."""
    system = GovernorInterviewSystem(test_dir)
    
    assert "form" in system.categories
    category = system.categories["form"]
    assert category.name == "Form and Manifestation"
    assert len(category.questions) == 2
    
    question = category.questions[0]
    assert question.id == "form_base_type"
    assert len(question.options) == 3

def test_start_interview(test_dir):
    """Test starting a new interview session."""
    system = GovernorInterviewSystem(test_dir)
    system.start_interview("TEST001")
    
    assert system.current_session is not None
    assert system.current_session.governor_id == "TEST001"
    assert len(system.current_session.responses) == 0

def test_get_next_question(test_dir):
    """Test getting next unanswered question."""
    system = GovernorInterviewSystem(test_dir)
    system.start_interview("TEST001")
    
    # First question should be form_base_type
    question = system.get_next_question("form")
    assert question is not None
    assert question.id == "form_base_type"
    
    # Record response and get next question
    system.record_response("form_base_type", "geometric")
    question = system.get_next_question("form")
    assert question is not None
    assert question.id == "form_complexity"
    
    # Record response and verify no more questions
    system.record_response("form_complexity", "simple")
    question = system.get_next_question("form")
    assert question is None

def test_record_response(test_dir):
    """Test recording interview responses."""
    system = GovernorInterviewSystem(test_dir)
    system.start_interview("TEST001")
    
    # Valid response
    assert system.record_response("form_base_type", "geometric")
    assert len(system.current_session.responses) == 1
    
    # Invalid question ID
    assert not system.record_response("invalid_id", "geometric")
    
    # Invalid option
    assert not system.record_response("form_base_type", "invalid_option")

def test_save_session(test_dir):
    """Test saving interview session."""
    system = GovernorInterviewSystem(test_dir)
    system.start_interview("TEST001")
    
    system.record_response("form_base_type", "geometric")
    system.record_response("form_complexity", "simple")
    
    output_dir = test_dir / "output"
    assert system.save_session(output_dir)
    
    # Verify saved file
    gov_dir = output_dir / "TEST001"
    saved_files = list(gov_dir.glob("interview_*.json"))
    assert len(saved_files) == 1
    
    with open(saved_files[0]) as f:
        data = json.load(f)
        assert data["governor_id"] == "TEST001"
        assert len(data["responses"]) == 2

def test_is_category_complete(test_dir):
    """Test checking category completion."""
    system = GovernorInterviewSystem(test_dir)
    system.start_interview("TEST001")
    
    assert not system.is_category_complete("form")
    
    system.record_response("form_base_type", "geometric")
    assert not system.is_category_complete("form")
    
    system.record_response("form_complexity", "simple")
    assert system.is_category_complete("form") 
"""Governor interview system for determining visual aspects."""
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

from .schemas.interview_schemas import (
    InterviewQuestion,
    QuestionCategory,
    InterviewResponse,
    InterviewSession
)

logger = logging.getLogger(__name__)

class GovernorInterviewSystem:
    """Handles interviews for individual governors to determine visual aspects."""
    
    def __init__(self, knowledge_base_path: str):
        """Initialize the interview system.
        
        Args:
            knowledge_base_path: Path to the knowledge base directory
        """
        self.knowledge_base_path = Path(knowledge_base_path)
        self.categories = self._load_interview_categories()
        self.current_session: Optional[InterviewSession] = None
        
    def _load_interview_categories(self) -> Dict[str, QuestionCategory]:
        """Load interview categories and questions from template."""
        try:
            questions_path = self.knowledge_base_path / "templates" / "interview_questions.json"
            with open(questions_path) as f:
                data = json.load(f)
                categories = {}
                
                for cat_id, cat_data in data["categories"].items():
                    questions = [
                        InterviewQuestion(
                            id=q["id"],
                            question=q["question"],
                            description=q["description"],
                            options=q["options"]
                        )
                        for q in cat_data["questions"]
                    ]
                    
                    categories[cat_id] = QuestionCategory(
                        name=cat_data["name"],
                        description=cat_data["description"],
                        questions=questions
                    )
                    
                return categories
                
        except Exception as e:
            logger.error(f"Failed to load interview questions: {e}")
            return {}
            
    def start_interview(self, governor_id: str) -> None:
        """Start a new interview session for a governor.
        
        Args:
            governor_id: ID of the governor being interviewed
        """
        self.current_session = InterviewSession(
            governor_id=governor_id,
            responses=[],
            timestamp=datetime.now().isoformat(),
        )
        
    def get_next_question(self, category: str) -> Optional[InterviewQuestion]:
        """Get the next unanswered question in a category.
        
        Args:
            category: Category to get question from
            
        Returns:
            Next unanswered question or None if all answered
        """
        if not self.current_session:
            logger.error("No active interview session")
            return None
            
        category_data = self.categories.get(category)
        if not category_data:
            logger.error(f"Invalid category: {category}")
            return None
            
        # Find first question in category not yet answered
        answered_ids = {r.question_id for r in self.current_session.responses}
        for question in category_data.questions:
            if question.id not in answered_ids:
                return question
                
        return None
        
    def record_response(self, question_id: str, selected_option: str, notes: Optional[str] = None) -> bool:
        """Record a response to an interview question.
        
        Args:
            question_id: ID of the question being answered
            selected_option: Selected response option
            notes: Optional notes about the response
            
        Returns:
            True if response recorded successfully
        """
        if not self.current_session:
            logger.error("No active interview session")
            return False
            
        # Validate question exists
        question = None
        for category in self.categories.values():
            for q in category.questions:
                if q.id == question_id:
                    question = q
                    break
            if question:
                break
                
        if not question:
            logger.error(f"Invalid question ID: {question_id}")
            return False
            
        # Validate option is valid
        if selected_option not in question.options:
            logger.error(f"Invalid option for question {question_id}: {selected_option}")
            return False
            
        response = InterviewResponse(
            question_id=question_id,
            selected_option=selected_option,
            notes=notes
        )
        
        self.current_session.responses.append(response)
        return True
        
    def save_session(self, output_dir: Path) -> bool:
        """Save the current interview session.
        
        Args:
            output_dir: Directory to save session data
            
        Returns:
            True if saved successfully
        """
        if not self.current_session:
            logger.error("No active interview session to save")
            return False
            
        try:
            # Create governor directory
            gov_dir = output_dir / self.current_session.governor_id
            gov_dir.mkdir(parents=True, exist_ok=True)
            
            # Save session data
            session_file = gov_dir / f"interview_{self.current_session.timestamp}.json"
            with open(session_file, 'w') as f:
                json.dump({
                    "governor_id": self.current_session.governor_id,
                    "timestamp": self.current_session.timestamp,
                    "version": self.current_session.version,
                    "responses": [
                        {
                            "question_id": r.question_id,
                            "selected_option": r.selected_option,
                            "notes": r.notes
                        }
                        for r in self.current_session.responses
                    ]
                }, f, indent=2)
                
            return True
            
        except Exception as e:
            logger.error(f"Failed to save interview session: {e}")
            return False
            
    def is_category_complete(self, category: str) -> bool:
        """Check if all questions in a category have been answered.
        
        Args:
            category: Category to check
            
        Returns:
            True if all questions answered
        """
        if not self.current_session:
            return False
            
        category_data = self.categories.get(category)
        if not category_data:
            return False
            
        answered_ids = {r.question_id for r in self.current_session.responses}
        category_question_ids = {q.id for q in category_data.questions}
        
        return category_question_ids.issubset(answered_ids) 
"""
Base utilities for mystical operations
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum, auto
from pydantic import BaseModel, Field, ConfigDict

def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Set up a logger with consistent formatting
    
    Args:
        name: Logger name
        level: Logging level
        
    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    logger.setLevel(level)
    return logger

class ValidationStatus(Enum):
    """Validation status enum"""
    SUCCESS = auto()
    WARNING = auto()
    ERROR = auto()

@dataclass
class ValidationResult:
    """Result of a validation operation"""
    status: ValidationStatus
    message: str
    details: Optional[Dict[str, Any]] = None

class MysticalEntity(BaseModel):
    """Base class for mystical entities"""
    id: str = Field(..., description="Entity identifier")
    name: str = Field(..., description="Entity name")
    attributes: Dict[str, Any] = Field(default_factory=dict, description="Entity attributes")
        
    def validate(self) -> ValidationResult:
        """Validate the entity"""
        if not self.id or not self.name:
            return ValidationResult(
                status=ValidationStatus.ERROR,
                message="Entity must have both id and name"
            )
        return ValidationResult(
            status=ValidationStatus.SUCCESS,
            message="Entity is valid"
        )
    
    def add_attribute(self, name: str, value: Any, source: Optional[str] = None) -> None:
        """Add a mystical attribute to the entity"""
        attr = MysticalAttribute(name=name, value=value, source=source)
        self.attributes[name] = attr.dict()

class MysticalAttribute(BaseModel):
    """Represents a mystical attribute"""
    name: str = Field(..., description="Attribute name")
    value: Any = Field(..., description="Attribute value")
    source: Optional[str] = Field(None, description="Source of the attribute")
        
    def validate(self) -> ValidationResult:
        """Validate the attribute"""
        if not self.name:
            return ValidationResult(
                status=ValidationStatus.ERROR,
                message="Attribute must have a name"
            )
        return ValidationResult(
            status=ValidationStatus.SUCCESS,
            message="Attribute is valid"
        )

class MysticalSystem(BaseModel):
    """Base class for all mystical systems"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    name: str = Field(..., description="System name")
    description: Optional[str] = Field(None, description="System description")
    entities: Dict[str, MysticalEntity] = Field(default_factory=dict, description="Registered entities")

    def __init__(self, **data):
        super().__init__(**data)
        self.logger = setup_logger(f"mystical.{self.name}")

    def validate_entity(self, entity: MysticalEntity) -> ValidationResult:
        """Validate an entity in this system"""
        return entity.validate()
        
    def validate_attribute(self, attribute: MysticalAttribute) -> ValidationResult:
        """Validate an attribute in this system"""
        return attribute.validate()
    
    def register_entity(self, entity: MysticalEntity) -> None:
        """Register an entity with this system"""
        validation = self.validate_entity(entity)
        if validation.status == ValidationStatus.ERROR:
            raise ValueError(f"Invalid entity: {validation.message}")
        self.entities[entity.id] = entity
    
    def get_entity(self, entity_id: str) -> Optional[MysticalEntity]:
        """Get an entity by ID"""
        return self.entities.get(entity_id)

class BitcoinMysticalSystem(MysticalSystem):
    """Base class for Bitcoin-integrated mystical systems"""
    
    def __init__(self, name: str, description: Optional[str] = None):
        super().__init__(name=name, description=description)
        self.logger = setup_logger(f"mystical.{name}")
        
    def get_bitcoin_entropy(self, seed: str) -> str:
        """
        Get Bitcoin-based entropy for the system
        
        Args:
            seed: Seed value for entropy generation
            
        Returns:
            Generated entropy string
            
        Raises:
            ImportError: If bitcoin integration module is not available
            ValueError: If seed is invalid
        """
        try:
            from .bitcoin_integration import get_bitcoin_entropy
            return get_bitcoin_entropy(seed)
        except ImportError as e:
            self.logger.error(f"Failed to import bitcoin integration: {e}")
            raise ImportError("Bitcoin integration module not available") from e
        except ValueError as e:
            self.logger.error(f"Invalid seed value: {e}")
            raise ValueError(f"Invalid seed value: {e}") from e 
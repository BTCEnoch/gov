"""Custom logging setup for the application."""

import logging
from typing import Optional

def setup_logger(name: Optional[str] = None) -> logging.Logger:
    """Set up a logger with consistent formatting.
    
    Args:
        name: Optional name for the logger. If None, returns root logger.
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:  # Only add handler if none exists
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # Set level to INFO by default
        logger.setLevel(logging.INFO)
    
    return logger 
"""File operations utilities for safe JSON handling."""

import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

def safe_json_read(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Safely read JSON from a file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Parsed JSON data or None if failed
    """
    try:
        path = Path(file_path)
        if not path.exists():
            logger.warning(f"JSON file not found: {file_path}")
            return None
            
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
            
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in file {file_path}: {e}")
        return None
    except Exception as e:
        logger.error(f"Error reading JSON file {file_path}: {e}")
        return None

def safe_json_write(data: Dict[str, Any], file_path: str, indent: int = 2) -> bool:
    """
    Safely write JSON to a file.
    
    Args:
        data: Data to write as JSON
        file_path: Path to write the JSON file
        indent: JSON indentation level
        
    Returns:
        True if successful, False otherwise
    """
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
            
        return True
        
    except Exception as e:
        logger.error(f"Error writing JSON file {file_path}: {e}")
        return False

"""
Tests for the I Ching System
"""

from core.mystical_systems.iching_system.iching_system import IChingSystem

def test_iching_system():
    """Test basic I Ching system functionality"""
    system = IChingSystem()
    assert system is not None 
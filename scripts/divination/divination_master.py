#!/usr/bin/env python3
"""
Enochian Cyphers Lighthouse: Unified Divination Master
Single interface for all divination systems
"""

from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from pathlib import Path

from .tarot_engine import TarotEngine, TarotReading
from .i_ching_engine import IChingEngine, IChing_Reading
from .astrology_engine import AstrologyEngine, AstrologyReading

class DivinationMaster:
    """Unified interface for all divination systems"""
    
    def __init__(self, lighthouse_path: str = "lighthouse/complete_lighthouse"):
        self.lighthouse_path = lighthouse_path
        self.tarot = TarotEngine(lighthouse_path)
        self.iching = IChingEngine(lighthouse_path)
        self.astrology = AstrologyEngine(lighthouse_path)
        
        self.available_systems = {
            "tarot": self.tarot,
            "i_ching": self.iching,
            "astrology": self.astrology
        }
    
    def tarot_reading(self, spread_type: str = "single_card", question: str = "") -> TarotReading:
        """Perform Tarot reading"""
        return self.tarot.perform_reading(spread_type, question)
    
    def iching_reading(self, question: str = "", method: str = "coins") -> IChing_Reading:
        """Perform I Ching reading"""
        return self.iching.perform_reading(question, method)
    
    def astrology_reading(self, birth_datetime: datetime, birth_location: str = "Unknown", 
                         focus: str = "general") -> AstrologyReading:
        """Perform Astrology reading"""
        return self.astrology.perform_reading(birth_datetime, birth_location, focus)
    
    def combined_reading(self, question: str, systems: List[str] = None) -> Dict[str, Any]:
        """Perform combined reading across multiple systems"""
        if systems is None:
            systems = ["tarot", "i_ching"]
        
        results = {}
        
        if "tarot" in systems:
            results["tarot"] = self.tarot_reading("three_card", question)
        
        if "i_ching" in systems:
            results["i_ching"] = self.iching_reading(question)
        
        if "astrology" in systems and "birth_datetime" in question.lower():
            # Would need birth info for astrology
            pass
        
        # Generate synthesis
        results["synthesis"] = self._synthesize_readings(results, question)
        
        return results
    
    def _synthesize_readings(self, readings: Dict[str, Any], question: str) -> str:
        """Synthesize multiple divination readings"""
        synthesis = f"Combined Divination Synthesis for: {question}\n\n"
        
        themes = []
        guidance_points = []
        
        if "tarot" in readings:
            tarot_reading = readings["tarot"]
            synthesis += f"Tarot Perspective:\n{tarot_reading.guidance}\n\n"
            themes.append("Tarot emphasizes practical guidance and emotional insights")
        
        if "i_ching" in readings:
            iching_reading = readings["i_ching"]
            synthesis += f"I Ching Perspective:\n{iching_reading.guidance}\n\n"
            themes.append("I Ching reveals the natural flow and timing of change")
        
        synthesis += "Unified Guidance:\n"
        synthesis += "Both systems point toward the importance of understanding "
        synthesis += "the current moment and working with natural rhythms. "
        synthesis += "Trust your intuition while taking practical action."
        
        return synthesis
    
    def get_daily_guidance(self, focus_area: str = "general") -> Dict[str, Any]:
        """Get daily guidance from multiple systems"""
        daily_guidance = {}
        
        # Single Tarot card for the day
        daily_guidance["tarot_card"] = self.tarot_reading("single_card", f"Daily guidance for {focus_area}")
        
        # I Ching for deeper wisdom
        daily_guidance["iching_wisdom"] = self.iching_reading(f"What wisdom do I need today regarding {focus_area}?")
        
        # Combined daily message
        daily_guidance["daily_message"] = self._create_daily_message(daily_guidance, focus_area)
        
        return daily_guidance
    
    def _create_daily_message(self, guidance: Dict[str, Any], focus_area: str) -> str:
        """Create unified daily message"""
        message = f"Daily Guidance for {focus_area.title()}:\n\n"
        
        tarot_card = guidance["tarot_card"].cards_drawn[0][0]
        message += f"Tarot Card: {tarot_card.name}\n"
        message += f"Key Energy: {', '.join(tarot_card.keywords[:3])}\n\n"
        
        iching_hex = guidance["iching_wisdom"].primary_hexagram
        message += f"I Ching Hexagram: {iching_hex.number} - {iching_hex.name}\n"
        message += f"Core Wisdom: {', '.join(iching_hex.keywords[:3])}\n\n"
        
        message += "Today's Focus:\n"
        message += f"Embrace the energy of {tarot_card.name.lower()} while "
        message += f"applying the wisdom of {iching_hex.name.lower()}. "
        message += "Stay present and trust the natural flow of events."
        
        return message
    
    def save_reading_session(self, session_data: Dict[str, Any], filename: str) -> None:
        """Save complete reading session"""
        import json
        
        # Convert readings to serializable format
        serializable_data = {
            "session_timestamp": datetime.now().isoformat(),
            "readings": {}
        }
        
        for system, reading in session_data.items():
            if system == "synthesis":
                serializable_data["readings"][system] = reading
            elif hasattr(reading, '__dict__'):
                # Convert dataclass to dict
                serializable_data["readings"][system] = self._reading_to_dict(reading)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(serializable_data, f, indent=2, ensure_ascii=False)
    
    def _reading_to_dict(self, reading: Any) -> Dict[str, Any]:
        """Convert reading object to dictionary"""
        if hasattr(reading, 'interpretation'):
            # Basic reading structure
            return {
                "interpretation": reading.interpretation,
                "guidance": reading.guidance,
                "timestamp": reading.timestamp
            }
        else:
            return {"reading": str(reading)}
    
    def get_available_spreads(self) -> Dict[str, List[str]]:
        """Get available spreads for each system"""
        return {
            "tarot": self.tarot.get_available_spreads(),
            "i_ching": ["coins", "yarrow"],
            "astrology": ["natal", "transit", "compatibility"]
        }
    
    def validate_question(self, question: str, system: str) -> bool:
        """Validate question appropriateness for system"""
        if not question.strip():
            return False
        
        # Basic validation - could be enhanced
        if system == "astrology" and "birth" not in question.lower():
            return False
        
        return True

if __name__ == "__main__":
    # Example usage
    divination = DivinationMaster()
    
    # Single system reading
    tarot_reading = divination.tarot_reading("three_card", "What should I focus on this week?")
    print("=== TAROT READING ===")
    print(tarot_reading.interpretation)
    
    # Combined reading
    combined = divination.combined_reading("How should I approach my current challenges?")
    print("\n=== COMBINED READING ===")
    print(combined["synthesis"])
    
    # Daily guidance
    daily = divination.get_daily_guidance("career")
    print("\n=== DAILY GUIDANCE ===")
    print(daily["daily_message"])

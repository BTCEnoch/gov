#!/usr/bin/env python3
"""
Enochian Cyphers Lighthouse: I Ching Divination Engine
Complete I Ching system with 64 hexagrams for divination and wisdom
"""

import json
import random
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Hexagram:
    """I Ching hexagram with complete attributes"""
    number: int
    name: str
    chinese_name: str
    trigrams: Tuple[str, str]  # (upper, lower)
    judgment: str
    image: str
    meaning: str
    changing_lines: Dict[int, str]
    keywords: List[str]
    element: str
    season: str

@dataclass
class IChing_Reading:
    """Complete I Ching reading with interpretation"""
    primary_hexagram: Hexagram
    changing_lines: List[int]
    secondary_hexagram: Optional[Hexagram]
    interpretation: str
    guidance: str
    question: str
    timestamp: str

class IChingEngine:
    """Complete I Ching divination system"""
    
    def __init__(self, lighthouse_path: str = "lighthouse/complete_lighthouse"):
        self.lighthouse_path = Path(lighthouse_path)
        self.hexagrams = self._load_hexagrams()
        self.trigrams = self._initialize_trigrams()
    
    def _load_hexagrams(self) -> Dict[int, Hexagram]:
        """Load all 64 hexagrams from lighthouse"""
        iching_file = self.lighthouse_path / "i_ching.json"
        
        if not iching_file.exists():
            return self._create_default_hexagrams()
        
        with open(iching_file, 'r', encoding='utf-8') as f:
            iching_data = json.load(f)
        
        hexagrams = {}
        for entry in iching_data.get("entries", []):
            # Extract hexagram number from ID
            hex_num = int(entry["id"].split("_")[-1])
            
            hexagram = Hexagram(
                number=hex_num,
                name=entry["name"].split(": ")[1].split(" - ")[0],
                chinese_name=entry["name"].split(": ")[1].split(" - ")[1] if " - " in entry["name"] else "",
                trigrams=("Heaven", "Earth"),  # Would be extracted from description
                judgment=entry["description"][:200],
                image=entry.get("historical_context", ""),
                meaning=entry["description"],
                changing_lines={i: f"Line {i} guidance" for i in range(1, 7)},
                keywords=entry.get("keywords", []),
                element=entry.get("element", "Earth"),
                season=entry.get("season", "All seasons")
            )
            hexagrams[hex_num] = hexagram
        
        return hexagrams
    
    def _create_default_hexagrams(self) -> Dict[int, Hexagram]:
        """Create default hexagrams if lighthouse data unavailable"""
        default_hexagrams = [
            (1, "Qian", "The Creative", ("Heaven", "Heaven"), "Pure yang energy, creative force"),
            (2, "Kun", "The Receptive", ("Earth", "Earth"), "Pure yin energy, receptive force"),
            (3, "Zhun", "Difficulty at the Beginning", ("Water", "Thunder"), "Initial challenges"),
            (4, "Meng", "Youthful Folly", ("Mountain", "Water"), "Learning and inexperience"),
            (5, "Xu", "Waiting", ("Water", "Heaven"), "Patience and timing"),
            (6, "Song", "Conflict", ("Heaven", "Water"), "Disputes and tension"),
            (7, "Shi", "The Army", ("Earth", "Water"), "Organization and discipline"),
            (8, "Pi", "Holding Together", ("Water", "Earth"), "Unity and cooperation")
        ]
        
        hexagrams = {}
        for num, chinese, english, trigrams, meaning in default_hexagrams:
            hexagram = Hexagram(
                number=num,
                name=english,
                chinese_name=chinese,
                trigrams=trigrams,
                judgment=f"Judgment for {english}: {meaning}",
                image=f"Image of {trigrams[0]} over {trigrams[1]}",
                meaning=meaning,
                changing_lines={i: f"Line {i}: Guidance for this position" for i in range(1, 7)},
                keywords=meaning.split(", "),
                element="Earth",
                season="All seasons"
            )
            hexagrams[num] = hexagram
        
        # Fill remaining hexagrams with placeholders
        for i in range(9, 65):
            hexagram = Hexagram(
                number=i,
                name=f"Hexagram {i}",
                chinese_name=f"Chinese {i}",
                trigrams=("Heaven", "Earth"),
                judgment=f"Judgment for hexagram {i}",
                image=f"Image for hexagram {i}",
                meaning=f"Meaning for hexagram {i}",
                changing_lines={j: f"Line {j}: Guidance" for j in range(1, 7)},
                keywords=["wisdom", "guidance"],
                element="Earth",
                season="All seasons"
            )
            hexagrams[i] = hexagram
        
        return hexagrams
    
    def _initialize_trigrams(self) -> Dict[str, Dict]:
        """Initialize the 8 trigrams"""
        return {
            "Heaven": {"symbol": "☰", "element": "Metal", "direction": "Northwest"},
            "Earth": {"symbol": "☷", "element": "Earth", "direction": "Southwest"},
            "Thunder": {"symbol": "☳", "element": "Wood", "direction": "East"},
            "Water": {"symbol": "☵", "element": "Water", "direction": "North"},
            "Mountain": {"symbol": "☶", "element": "Earth", "direction": "Northeast"},
            "Wind": {"symbol": "☴", "element": "Wood", "direction": "Southeast"},
            "Fire": {"symbol": "☲", "element": "Fire", "direction": "South"},
            "Lake": {"symbol": "☱", "element": "Metal", "direction": "West"}
        }
    
    def cast_coins(self) -> List[int]:
        """Cast three coins six times to generate hexagram"""
        lines = []
        for _ in range(6):
            # Three coin tosses (heads=3, tails=2)
            total = sum(random.choice([2, 3]) for _ in range(3))
            lines.append(total)
        return lines
    
    def cast_yarrow_stalks(self) -> List[int]:
        """Simulate yarrow stalk method (more traditional)"""
        lines = []
        for _ in range(6):
            # Simplified yarrow stalk simulation
            # Results in 6, 7, 8, or 9
            result = random.choices([6, 7, 8, 9], weights=[1, 5, 7, 3])[0]
            lines.append(result)
        return lines
    
    def lines_to_hexagram(self, lines: List[int]) -> Tuple[int, List[int]]:
        """Convert line values to hexagram number and changing lines"""
        # Convert to binary (yin/yang)
        binary_lines = []
        changing_lines = []
        
        for i, line in enumerate(lines):
            if line in [6, 8]:  # Yin lines
                binary_lines.append(0)
                if line == 6:  # Changing yin
                    changing_lines.append(i + 1)
            else:  # Yang lines (7, 9)
                binary_lines.append(1)
                if line == 9:  # Changing yang
                    changing_lines.append(i + 1)
        
        # Convert binary to hexagram number (simplified)
        hex_number = 1 + sum(binary_lines[i] * (2 ** i) for i in range(6)) % 64
        
        return hex_number, changing_lines
    
    def get_secondary_hexagram(self, primary_hex: int, changing_lines: List[int]) -> Optional[int]:
        """Calculate secondary hexagram from changing lines"""
        if not changing_lines:
            return None
        
        # Simplified calculation - in practice would flip the changing lines
        secondary = (primary_hex + len(changing_lines)) % 64
        if secondary == 0:
            secondary = 64
        
        return secondary
    
    def perform_reading(self, question: str = "", method: str = "coins") -> IChing_Reading:
        """Perform complete I Ching reading"""
        # Cast for hexagram
        if method == "yarrow":
            lines = self.cast_yarrow_stalks()
        else:
            lines = self.cast_coins()
        
        primary_num, changing_lines = self.lines_to_hexagram(lines)
        primary_hexagram = self.hexagrams[primary_num]
        
        # Get secondary hexagram if there are changing lines
        secondary_num = self.get_secondary_hexagram(primary_num, changing_lines)
        secondary_hexagram = self.hexagrams[secondary_num] if secondary_num else None
        
        interpretation = self._interpret_reading(primary_hexagram, changing_lines, secondary_hexagram, question)
        guidance = self._generate_guidance(primary_hexagram, changing_lines, secondary_hexagram)
        
        return IChing_Reading(
            primary_hexagram=primary_hexagram,
            changing_lines=changing_lines,
            secondary_hexagram=secondary_hexagram,
            interpretation=interpretation,
            guidance=guidance,
            question=question,
            timestamp=self._get_timestamp()
        )
    
    def _interpret_reading(self, primary: Hexagram, changing_lines: List[int], 
                          secondary: Optional[Hexagram], question: str) -> str:
        """Generate interpretation for the reading"""
        interpretation = f"I Ching Reading: Hexagram {primary.number} - {primary.name}\n\n"
        
        if question:
            interpretation += f"Question: {question}\n\n"
        
        interpretation += f"Primary Hexagram: {primary.chinese_name} ({primary.name})\n"
        interpretation += f"Judgment: {primary.judgment}\n"
        interpretation += f"Image: {primary.image}\n\n"
        
        if changing_lines:
            interpretation += f"Changing Lines: {', '.join(map(str, changing_lines))}\n"
            for line in changing_lines:
                interpretation += f"Line {line}: {primary.changing_lines.get(line, 'Guidance for this line')}\n"
            interpretation += "\n"
        
        if secondary:
            interpretation += f"Secondary Hexagram: {secondary.number} - {secondary.name}\n"
            interpretation += f"Future situation: {secondary.meaning}\n\n"
        
        return interpretation
    
    def _generate_guidance(self, primary: Hexagram, changing_lines: List[int], 
                          secondary: Optional[Hexagram]) -> str:
        """Generate wisdom guidance from the reading"""
        guidance = "I Ching Wisdom:\n\n"
        
        # Primary guidance
        guidance += f"The situation is characterized by {primary.name.lower()}. "
        guidance += f"The key themes are: {', '.join(primary.keywords)}.\n\n"
        
        # Changing lines guidance
        if changing_lines:
            guidance += f"There are {len(changing_lines)} changing lines, indicating "
            guidance += "transformation and movement in the situation. "
            guidance += "Pay attention to the timing of changes.\n\n"
        else:
            guidance += "No changing lines indicate a stable situation. "
            guidance += "The current conditions will persist.\n\n"
        
        # Secondary hexagram guidance
        if secondary:
            guidance += f"The situation is evolving toward {secondary.name.lower()}. "
            guidance += "Prepare for this transformation and align your actions accordingly.\n\n"
        
        guidance += "Remember: The I Ching teaches us about the natural flow of change. "
        guidance += "Work with the current rather than against it."
        
        return guidance
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_hexagram_by_number(self, number: int) -> Optional[Hexagram]:
        """Get specific hexagram by number"""
        return self.hexagrams.get(number)
    
    def search_hexagrams(self, keyword: str) -> List[Hexagram]:
        """Search hexagrams by keyword"""
        results = []
        keyword_lower = keyword.lower()
        
        for hexagram in self.hexagrams.values():
            if (keyword_lower in hexagram.name.lower() or 
                keyword_lower in hexagram.chinese_name.lower() or
                any(keyword_lower in kw.lower() for kw in hexagram.keywords)):
                results.append(hexagram)
        
        return results
    
    def save_reading(self, reading: IChing_Reading, filename: str) -> None:
        """Save reading to file"""
        reading_data = {
            "primary_hexagram": {
                "number": reading.primary_hexagram.number,
                "name": reading.primary_hexagram.name,
                "chinese_name": reading.primary_hexagram.chinese_name
            },
            "changing_lines": reading.changing_lines,
            "secondary_hexagram": {
                "number": reading.secondary_hexagram.number,
                "name": reading.secondary_hexagram.name
            } if reading.secondary_hexagram else None,
            "interpretation": reading.interpretation,
            "guidance": reading.guidance,
            "question": reading.question,
            "timestamp": reading.timestamp
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(reading_data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    # Example usage
    iching = IChingEngine()
    
    # Perform a reading
    reading = iching.perform_reading("What should I focus on in my current situation?", "coins")
    
    print("=== I CHING READING ===")
    print(reading.interpretation)
    print(reading.guidance)

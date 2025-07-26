#!/usr/bin/env python3
"""
Enochian Cyphers Lighthouse: Tarot Divination Engine
Complete Tarot system for divination, meditation, and spiritual guidance
"""

import json
import random
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path

@dataclass
class TarotCard:
    """Individual Tarot card with complete attributes"""
    id: str
    name: str
    number: str
    suit: Optional[str]
    arcana_type: str  # major or minor
    upright_meaning: str
    reversed_meaning: str
    element: Optional[str]
    astrological_correspondence: Optional[str]
    keywords: List[str]
    symbolism: str
    meditation_focus: str

@dataclass
class TarotReading:
    """Complete Tarot reading with interpretation"""
    spread_type: str
    cards_drawn: List[Tuple[TarotCard, bool]]  # (card, is_reversed)
    interpretation: str
    guidance: str
    timestamp: str

class TarotEngine:
    """Complete Tarot divination system"""
    
    def __init__(self, lighthouse_path: str = "lighthouse/complete_lighthouse"):
        self.lighthouse_path = Path(lighthouse_path)
        self.deck = self._load_tarot_deck()
        self.spreads = self._initialize_spreads()
    
    def _load_tarot_deck(self) -> List[TarotCard]:
        """Load complete 78-card Tarot deck from lighthouse"""
        tarot_file = self.lighthouse_path / "tarot.json"
        
        if not tarot_file.exists():
            return self._create_default_deck()
        
        with open(tarot_file, 'r', encoding='utf-8') as f:
            tarot_data = json.load(f)
        
        deck = []
        for entry in tarot_data.get("entries", []):
            card = TarotCard(
                id=entry["id"],
                name=entry["name"],
                number=entry.get("number", ""),
                suit=entry.get("suit"),
                arcana_type="major" if "major" in entry["id"] else "minor",
                upright_meaning=entry["description"][:200] + "...",
                reversed_meaning=f"Reversed: {entry['description'][:150]}...",
                element=entry.get("element"),
                astrological_correspondence=entry.get("astrology"),
                keywords=entry.get("keywords", []),
                symbolism=entry["description"],
                meditation_focus=entry.get("meditation_focus", "Focus on card imagery")
            )
            deck.append(card)
        
        return deck
    
    def _create_default_deck(self) -> List[TarotCard]:
        """Create default deck if lighthouse data unavailable"""
        major_arcana = [
            ("The Fool", "0", "New beginnings, innocence, spontaneity"),
            ("The Magician", "I", "Manifestation, resourcefulness, power"),
            ("The High Priestess", "II", "Intuition, sacred knowledge, divine feminine"),
            ("The Empress", "III", "Femininity, beauty, nature, abundance"),
            ("The Emperor", "IV", "Authority, establishment, structure"),
            ("The Hierophant", "V", "Spiritual wisdom, religious beliefs, tradition"),
            ("The Lovers", "VI", "Love, harmony, relationships, choices"),
            ("The Chariot", "VII", "Control, willpower, success, determination"),
            ("Strength", "VIII", "Strength, courage, persuasion, influence"),
            ("The Hermit", "IX", "Soul searching, introspection, inner guidance"),
            ("Wheel of Fortune", "X", "Good luck, karma, life cycles, destiny"),
            ("Justice", "XI", "Justice, fairness, truth, cause and effect"),
            ("The Hanged Man", "XII", "Suspension, restriction, letting go"),
            ("Death", "XIII", "Endings, beginnings, change, transformation"),
            ("Temperance", "XIV", "Balance, moderation, patience, purpose"),
            ("The Devil", "XV", "Bondage, addiction, sexuality, materialism"),
            ("The Tower", "XVI", "Sudden change, upheaval, chaos, revelation"),
            ("The Star", "XVII", "Hope, faith, purpose, renewal, spirituality"),
            ("The Moon", "XVIII", "Illusion, fear, anxiety, subconscious"),
            ("The Sun", "XIX", "Positivity, fun, warmth, success, vitality"),
            ("Judgement", "XX", "Judgement, rebirth, inner calling, absolution"),
            ("The World", "XXI", "Completion, accomplishment, travel, fulfillment")
        ]
        
        deck = []
        for name, number, meaning in major_arcana:
            card = TarotCard(
                id=f"tarot_major_{name.lower().replace(' ', '_')}",
                name=name,
                number=number,
                suit=None,
                arcana_type="major",
                upright_meaning=meaning,
                reversed_meaning=f"Reversed: {meaning} blocked or excessive",
                element=None,
                astrological_correspondence=None,
                keywords=meaning.split(", "),
                symbolism=f"Traditional symbolism of {name}",
                meditation_focus=f"Meditate on {name} imagery and meaning"
            )
            deck.append(card)
        
        return deck
    
    def _initialize_spreads(self) -> Dict[str, Dict]:
        """Initialize Tarot spread configurations"""
        return {
            "single_card": {
                "positions": 1,
                "description": "Single card for daily guidance",
                "positions_meaning": ["Daily guidance"]
            },
            "three_card": {
                "positions": 3,
                "description": "Past, Present, Future spread",
                "positions_meaning": ["Past", "Present", "Future"]
            },
            "celtic_cross": {
                "positions": 10,
                "description": "Complete Celtic Cross spread",
                "positions_meaning": [
                    "Present situation", "Challenge/Cross", "Distant past/Foundation",
                    "Recent past", "Possible outcome", "Near future",
                    "Your approach", "External influences", "Hopes and fears", "Final outcome"
                ]
            },
            "relationship": {
                "positions": 7,
                "description": "Relationship dynamics spread",
                "positions_meaning": [
                    "You", "Partner", "Relationship", "Challenges",
                    "Strengths", "Advice", "Outcome"
                ]
            },
            "decision": {
                "positions": 5,
                "description": "Decision-making spread",
                "positions_meaning": [
                    "Current situation", "Option A", "Option B",
                    "What you need to know", "Recommended path"
                ]
            }
        }
    
    def shuffle_deck(self) -> None:
        """Shuffle the Tarot deck"""
        random.shuffle(self.deck)
    
    def draw_cards(self, count: int) -> List[Tuple[TarotCard, bool]]:
        """Draw cards with random reversal"""
        self.shuffle_deck()
        drawn = []
        
        for i in range(min(count, len(self.deck))):
            card = self.deck[i]
            is_reversed = random.choice([True, False])
            drawn.append((card, is_reversed))
        
        return drawn
    
    def perform_reading(self, spread_type: str = "single_card", question: str = "") -> TarotReading:
        """Perform complete Tarot reading"""
        if spread_type not in self.spreads:
            spread_type = "single_card"
        
        spread_config = self.spreads[spread_type]
        cards_drawn = self.draw_cards(spread_config["positions"])
        
        interpretation = self._interpret_reading(cards_drawn, spread_config, question)
        guidance = self._generate_guidance(cards_drawn, question)
        
        return TarotReading(
            spread_type=spread_type,
            cards_drawn=cards_drawn,
            interpretation=interpretation,
            guidance=guidance,
            timestamp=self._get_timestamp()
        )
    
    def _interpret_reading(self, cards: List[Tuple[TarotCard, bool]], 
                          spread_config: Dict, question: str) -> str:
        """Generate interpretation for the reading"""
        interpretation = f"Tarot Reading: {spread_config['description']}\n\n"
        
        if question:
            interpretation += f"Question: {question}\n\n"
        
        for i, (card, is_reversed) in enumerate(cards):
            position = spread_config["positions_meaning"][i]
            meaning = card.reversed_meaning if is_reversed else card.upright_meaning
            reversal_text = " (Reversed)" if is_reversed else ""
            
            interpretation += f"{position}: {card.name}{reversal_text}\n"
            interpretation += f"Meaning: {meaning}\n\n"
        
        return interpretation
    
    def _generate_guidance(self, cards: List[Tuple[TarotCard, bool]], question: str) -> str:
        """Generate spiritual guidance from the reading"""
        guidance = "Spiritual Guidance:\n\n"
        
        # Analyze overall energy
        major_count = sum(1 for card, _ in cards if card.arcana_type == "major")
        
        if major_count > len(cards) / 2:
            guidance += "This reading shows strong spiritual forces at work. "
            guidance += "Major life themes and karmic influences are prominent.\n\n"
        else:
            guidance += "This reading focuses on practical, everyday matters. "
            guidance += "The guidance relates to immediate circumstances and choices.\n\n"
        
        # Key themes
        all_keywords = []
        for card, is_reversed in cards:
            all_keywords.extend(card.keywords)
        
        common_themes = list(set(all_keywords))[:3]
        if common_themes:
            guidance += f"Key themes: {', '.join(common_themes)}\n\n"
        
        guidance += "Trust your intuition as you apply this guidance to your situation."
        
        return guidance
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_card_by_name(self, name: str) -> Optional[TarotCard]:
        """Get specific card by name"""
        for card in self.deck:
            if card.name.lower() == name.lower():
                return card
        return None
    
    def get_available_spreads(self) -> List[str]:
        """Get list of available spread types"""
        return list(self.spreads.keys())
    
    def save_reading(self, reading: TarotReading, filename: str) -> None:
        """Save reading to file"""
        reading_data = {
            "spread_type": reading.spread_type,
            "cards": [
                {
                    "name": card.name,
                    "reversed": is_reversed,
                    "meaning": card.reversed_meaning if is_reversed else card.upright_meaning
                }
                for card, is_reversed in reading.cards_drawn
            ],
            "interpretation": reading.interpretation,
            "guidance": reading.guidance,
            "timestamp": reading.timestamp
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(reading_data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    # Example usage
    tarot = TarotEngine()
    
    # Perform a three-card reading
    reading = tarot.perform_reading("three_card", "What do I need to know about my current path?")
    
    print("=== TAROT READING ===")
    print(reading.interpretation)
    print(reading.guidance)

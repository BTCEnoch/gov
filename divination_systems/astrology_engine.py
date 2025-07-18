#!/usr/bin/env python3
"""
Enochian Cyphers Lighthouse: Astrology Divination Engine
Complete astrology system for natal charts, transits, and divination
"""

import json
import math
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Planet:
    """Astrological planet with position and aspects"""
    name: str
    symbol: str
    longitude: float  # Degrees in zodiac
    sign: str
    house: int
    retrograde: bool
    element: str
    modality: str

@dataclass
class Aspect:
    """Astrological aspect between planets"""
    planet1: str
    planet2: str
    aspect_type: str  # conjunction, opposition, trine, square, sextile
    orb: float
    exact: bool

@dataclass
class NatalChart:
    """Complete natal chart"""
    birth_datetime: datetime
    birth_location: str
    planets: Dict[str, Planet]
    houses: Dict[int, str]  # House cusps in signs
    aspects: List[Aspect]
    ascendant: str
    midheaven: str

@dataclass
class AstrologyReading:
    """Complete astrology reading"""
    chart: NatalChart
    interpretation: str
    personality_analysis: str
    life_themes: List[str]
    current_transits: str
    guidance: str
    timestamp: str

class AstrologyEngine:
    """Complete astrology divination system"""
    
    def __init__(self, lighthouse_path: str = "lighthouse/complete_lighthouse"):
        self.lighthouse_path = Path(lighthouse_path)
        self.signs = self._initialize_signs()
        self.planets_data = self._load_planets_data()
        self.houses_meanings = self._initialize_houses()
        self.aspects_data = self._initialize_aspects()
    
    def _initialize_signs(self) -> Dict[str, Dict]:
        """Initialize zodiac signs with attributes"""
        return {
            "Aries": {"element": "Fire", "modality": "Cardinal", "ruler": "Mars", "keywords": ["initiative", "leadership", "courage"]},
            "Taurus": {"element": "Earth", "modality": "Fixed", "ruler": "Venus", "keywords": ["stability", "persistence", "sensuality"]},
            "Gemini": {"element": "Air", "modality": "Mutable", "ruler": "Mercury", "keywords": ["communication", "adaptability", "curiosity"]},
            "Cancer": {"element": "Water", "modality": "Cardinal", "ruler": "Moon", "keywords": ["nurturing", "protection", "emotion"]},
            "Leo": {"element": "Fire", "modality": "Fixed", "ruler": "Sun", "keywords": ["creativity", "self-expression", "leadership"]},
            "Virgo": {"element": "Earth", "modality": "Mutable", "ruler": "Mercury", "keywords": ["service", "perfection", "analysis"]},
            "Libra": {"element": "Air", "modality": "Cardinal", "ruler": "Venus", "keywords": ["balance", "harmony", "relationships"]},
            "Scorpio": {"element": "Water", "modality": "Fixed", "ruler": "Pluto", "keywords": ["transformation", "depth", "intensity"]},
            "Sagittarius": {"element": "Fire", "modality": "Mutable", "ruler": "Jupiter", "keywords": ["philosophy", "expansion", "adventure"]},
            "Capricorn": {"element": "Earth", "modality": "Cardinal", "ruler": "Saturn", "keywords": ["achievement", "structure", "responsibility"]},
            "Aquarius": {"element": "Air", "modality": "Fixed", "ruler": "Uranus", "keywords": ["innovation", "humanity", "independence"]},
            "Pisces": {"element": "Water", "modality": "Mutable", "ruler": "Neptune", "keywords": ["spirituality", "compassion", "intuition"]}
        }
    
    def _load_planets_data(self) -> Dict[str, Dict]:
        """Load planetary data from lighthouse"""
        astrology_file = self.lighthouse_path / "astrology.json"
        
        # Default planetary data
        planets = {
            "Sun": {"symbol": "☉", "keywords": ["identity", "ego", "vitality"], "cycle": 365.25},
            "Moon": {"symbol": "☽", "keywords": ["emotions", "instincts", "subconscious"], "cycle": 29.5},
            "Mercury": {"symbol": "☿", "keywords": ["communication", "thinking", "learning"], "cycle": 88},
            "Venus": {"symbol": "♀", "keywords": ["love", "beauty", "values"], "cycle": 225},
            "Mars": {"symbol": "♂", "keywords": ["action", "desire", "energy"], "cycle": 687},
            "Jupiter": {"symbol": "♃", "keywords": ["expansion", "wisdom", "luck"], "cycle": 4333},
            "Saturn": {"symbol": "♄", "keywords": ["structure", "discipline", "lessons"], "cycle": 10759},
            "Uranus": {"symbol": "♅", "keywords": ["innovation", "rebellion", "change"], "cycle": 30687},
            "Neptune": {"symbol": "♆", "keywords": ["spirituality", "illusion", "dreams"], "cycle": 60190},
            "Pluto": {"symbol": "♇", "keywords": ["transformation", "power", "rebirth"], "cycle": 90560}
        }
        
        if astrology_file.exists():
            try:
                with open(astrology_file, 'r', encoding='utf-8') as f:
                    astrology_data = json.load(f)
                # Could enhance with lighthouse data
            except:
                pass
        
        return planets
    
    def _initialize_houses(self) -> Dict[int, str]:
        """Initialize house meanings"""
        return {
            1: "Self, identity, appearance, first impressions",
            2: "Money, possessions, values, self-worth",
            3: "Communication, siblings, short trips, learning",
            4: "Home, family, roots, emotional foundation",
            5: "Creativity, romance, children, self-expression",
            6: "Work, health, daily routine, service",
            7: "Partnerships, marriage, open enemies, cooperation",
            8: "Shared resources, transformation, occult, death/rebirth",
            9: "Philosophy, higher education, long trips, spirituality",
            10: "Career, reputation, public image, authority",
            11: "Friends, groups, hopes, wishes, humanitarian causes",
            12: "Subconscious, hidden enemies, spirituality, sacrifice"
        }
    
    def _initialize_aspects(self) -> Dict[str, Dict]:
        """Initialize aspect meanings"""
        return {
            "conjunction": {"degrees": 0, "orb": 8, "nature": "neutral", "meaning": "Unity, blending of energies"},
            "opposition": {"degrees": 180, "orb": 8, "nature": "challenging", "meaning": "Tension, awareness, balance needed"},
            "trine": {"degrees": 120, "orb": 8, "nature": "harmonious", "meaning": "Flow, ease, natural talent"},
            "square": {"degrees": 90, "orb": 8, "nature": "challenging", "meaning": "Conflict, motivation, growth through challenge"},
            "sextile": {"degrees": 60, "orb": 6, "nature": "harmonious", "meaning": "Opportunity, cooperation, skill development"},
            "quincunx": {"degrees": 150, "orb": 3, "nature": "minor", "meaning": "Adjustment, adaptation, subtle tension"}
        }
    
    def calculate_chart(self, birth_datetime: datetime, birth_location: str = "Unknown") -> NatalChart:
        """Calculate natal chart (simplified calculation)"""
        # This is a simplified calculation - real astrology would use ephemeris data
        
        # Calculate planetary positions (simplified)
        planets = {}
        for planet_name in self.planets_data.keys():
            # Simplified position calculation
            longitude = (hash(f"{planet_name}{birth_datetime}") % 360)
            sign = self._longitude_to_sign(longitude)
            house = (longitude // 30 + 1) % 12 + 1
            
            planet = Planet(
                name=planet_name,
                symbol=self.planets_data[planet_name]["symbol"],
                longitude=longitude,
                sign=sign,
                house=int(house),
                retrograde=hash(planet_name) % 4 == 0,  # Simplified retrograde
                element=self.signs[sign]["element"],
                modality=self.signs[sign]["modality"]
            )
            planets[planet_name] = planet
        
        # Calculate house cusps
        houses = {}
        for i in range(1, 13):
            cusp_longitude = (i - 1) * 30  # Simplified equal house system
            houses[i] = self._longitude_to_sign(cusp_longitude)
        
        # Calculate aspects
        aspects = self._calculate_aspects(planets)
        
        # Ascendant and Midheaven (simplified)
        ascendant = self._longitude_to_sign(0)  # Simplified
        midheaven = self._longitude_to_sign(90)  # Simplified
        
        return NatalChart(
            birth_datetime=birth_datetime,
            birth_location=birth_location,
            planets=planets,
            houses=houses,
            aspects=aspects,
            ascendant=ascendant,
            midheaven=midheaven
        )
    
    def _longitude_to_sign(self, longitude: float) -> str:
        """Convert longitude to zodiac sign"""
        signs = list(self.signs.keys())
        sign_index = int(longitude // 30) % 12
        return signs[sign_index]
    
    def _calculate_aspects(self, planets: Dict[str, Planet]) -> List[Aspect]:
        """Calculate aspects between planets"""
        aspects = []
        planet_list = list(planets.keys())
        
        for i, planet1_name in enumerate(planet_list):
            for planet2_name in planet_list[i+1:]:
                planet1 = planets[planet1_name]
                planet2 = planets[planet2_name]
                
                # Calculate angular separation
                separation = abs(planet1.longitude - planet2.longitude)
                if separation > 180:
                    separation = 360 - separation
                
                # Check for aspects
                for aspect_name, aspect_data in self.aspects_data.items():
                    target_angle = aspect_data["degrees"]
                    orb = aspect_data["orb"]
                    
                    if abs(separation - target_angle) <= orb:
                        aspect = Aspect(
                            planet1=planet1_name,
                            planet2=planet2_name,
                            aspect_type=aspect_name,
                            orb=abs(separation - target_angle),
                            exact=abs(separation - target_angle) <= 1
                        )
                        aspects.append(aspect)
        
        return aspects
    
    def perform_reading(self, birth_datetime: datetime, birth_location: str = "Unknown", 
                       focus: str = "general") -> AstrologyReading:
        """Perform complete astrology reading"""
        chart = self.calculate_chart(birth_datetime, birth_location)
        
        interpretation = self._interpret_chart(chart, focus)
        personality_analysis = self._analyze_personality(chart)
        life_themes = self._identify_life_themes(chart)
        current_transits = self._analyze_current_transits(chart)
        guidance = self._generate_guidance(chart, focus)
        
        return AstrologyReading(
            chart=chart,
            interpretation=interpretation,
            personality_analysis=personality_analysis,
            life_themes=life_themes,
            current_transits=current_transits,
            guidance=guidance,
            timestamp=self._get_timestamp()
        )
    
    def _interpret_chart(self, chart: NatalChart, focus: str) -> str:
        """Generate chart interpretation"""
        interpretation = f"Natal Chart Interpretation\n"
        interpretation += f"Birth: {chart.birth_datetime.strftime('%Y-%m-%d %H:%M')} at {chart.birth_location}\n\n"
        
        interpretation += f"Ascendant: {chart.ascendant}\n"
        interpretation += f"Midheaven: {chart.midheaven}\n\n"
        
        interpretation += "Planetary Positions:\n"
        for planet_name, planet in chart.planets.items():
            retro = " (R)" if planet.retrograde else ""
            interpretation += f"{planet.symbol} {planet_name}: {planet.sign} in House {planet.house}{retro}\n"
        
        interpretation += f"\nMajor Aspects ({len(chart.aspects)} total):\n"
        for aspect in chart.aspects[:5]:  # Show first 5 aspects
            interpretation += f"{aspect.planet1} {aspect.aspect_type} {aspect.planet2} (orb: {aspect.orb:.1f}°)\n"
        
        return interpretation
    
    def _analyze_personality(self, chart: NatalChart) -> str:
        """Analyze personality from chart"""
        sun = chart.planets["Sun"]
        moon = chart.planets["Moon"]
        ascendant_sign = chart.ascendant
        
        analysis = "Personality Analysis:\n\n"
        
        analysis += f"Core Identity (Sun in {sun.sign}):\n"
        analysis += f"Your essential self is expressed through {sun.sign} qualities: "
        analysis += f"{', '.join(self.signs[sun.sign]['keywords'])}.\n\n"
        
        analysis += f"Emotional Nature (Moon in {moon.sign}):\n"
        analysis += f"Your emotional responses and instincts are colored by {moon.sign}: "
        analysis += f"{', '.join(self.signs[moon.sign]['keywords'])}.\n\n"
        
        analysis += f"Outer Personality (Ascendant in {ascendant_sign}):\n"
        analysis += f"Others see you as embodying {ascendant_sign} traits: "
        analysis += f"{', '.join(self.signs[ascendant_sign]['keywords'])}.\n\n"
        
        return analysis
    
    def _identify_life_themes(self, chart: NatalChart) -> List[str]:
        """Identify major life themes"""
        themes = []
        
        # Analyze planetary concentrations
        element_count = {"Fire": 0, "Earth": 0, "Air": 0, "Water": 0}
        modality_count = {"Cardinal": 0, "Fixed": 0, "Mutable": 0}
        
        for planet in chart.planets.values():
            element_count[planet.element] += 1
            modality_count[planet.modality] += 1
        
        # Dominant element
        dominant_element = max(element_count, key=element_count.get)
        themes.append(f"Strong {dominant_element} emphasis - {self._element_meaning(dominant_element)}")
        
        # Dominant modality
        dominant_modality = max(modality_count, key=modality_count.get)
        themes.append(f"{dominant_modality} nature - {self._modality_meaning(dominant_modality)}")
        
        # Major aspects
        if len(chart.aspects) > 10:
            themes.append("Complex personality with many internal dynamics")
        elif len(chart.aspects) < 5:
            themes.append("Focused energy with clear direction")
        
        return themes
    
    def _element_meaning(self, element: str) -> str:
        """Get element meaning"""
        meanings = {
            "Fire": "passionate, energetic, inspirational approach to life",
            "Earth": "practical, grounded, material-focused approach",
            "Air": "intellectual, communicative, idea-oriented approach",
            "Water": "emotional, intuitive, feeling-based approach"
        }
        return meanings.get(element, "balanced approach")
    
    def _modality_meaning(self, modality: str) -> str:
        """Get modality meaning"""
        meanings = {
            "Cardinal": "initiating, leadership-oriented, action-focused",
            "Fixed": "stable, persistent, determined approach",
            "Mutable": "adaptable, flexible, changeable nature"
        }
        return meanings.get(modality, "balanced approach")
    
    def _analyze_current_transits(self, chart: NatalChart) -> str:
        """Analyze current planetary transits (simplified)"""
        transits = "Current Planetary Influences:\n\n"
        transits += "The current planetary positions are creating opportunities for:\n"
        transits += "- Personal growth and self-discovery\n"
        transits += "- Relationship developments\n"
        transits += "- Career and life direction changes\n\n"
        transits += "Pay attention to themes around communication and emotional expression."
        
        return transits
    
    def _generate_guidance(self, chart: NatalChart, focus: str) -> str:
        """Generate astrological guidance"""
        guidance = "Astrological Guidance:\n\n"
        
        sun_sign = chart.planets["Sun"].sign
        guidance += f"As a {sun_sign}, your path involves developing "
        guidance += f"{', '.join(self.signs[sun_sign]['keywords'])}. "
        
        guidance += "Work with your natural strengths while being aware of potential challenges.\n\n"
        
        guidance += "Key recommendations:\n"
        guidance += "- Honor both your solar identity and lunar emotional needs\n"
        guidance += "- Use your ascendant qualities to navigate social situations\n"
        guidance += "- Pay attention to the houses where your personal planets are located\n"
        guidance += "- Work constructively with challenging aspects for growth\n\n"
        
        guidance += "Remember: Astrology shows potentials, not fixed destinies. "
        guidance += "You have the power to work with these energies consciously."
        
        return guidance
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        return datetime.now().isoformat()
    
    def save_reading(self, reading: AstrologyReading, filename: str) -> None:
        """Save reading to file"""
        reading_data = {
            "birth_info": {
                "datetime": reading.chart.birth_datetime.isoformat(),
                "location": reading.chart.birth_location
            },
            "interpretation": reading.interpretation,
            "personality_analysis": reading.personality_analysis,
            "life_themes": reading.life_themes,
            "current_transits": reading.current_transits,
            "guidance": reading.guidance,
            "timestamp": reading.timestamp
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(reading_data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    # Example usage
    astrology = AstrologyEngine()
    
    # Perform a reading
    birth_date = datetime(1990, 6, 15, 14, 30, tzinfo=timezone.utc)
    reading = astrology.perform_reading(birth_date, "New York, NY", "personality")
    
    print("=== ASTROLOGY READING ===")
    print(reading.interpretation)
    print(reading.personality_analysis)
    print(reading.guidance)

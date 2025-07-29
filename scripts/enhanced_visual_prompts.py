#!/usr/bin/env python3
"""
Enhanced Visual Profile Generation for 91 Governor Angels
Incorporates tradition-based traits, NLP improvements, and advanced templating
"""

import json
import re
import random
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple, Any
from collections import defaultdict

class EnhancedVisualPromptGenerator:
    def __init__(self):
        self.governor_profiles_dir = Path("governor_profiles")
        self.output_dir = Path("visual_prompt_gen")
        
        # Initialize tradition traits dictionary
        self.tradition_traits = self._load_tradition_traits()
        
        # Enhanced tarot poses with more nuanced descriptions
        self.tarot_gesture_interpretations = {
            "The Hermit": "front-facing centered standing pose with one hand raised holding an ethereal lantern, other hand in contemplative gesture",
            "The Magician": "front-facing centered dynamic pose with one arm raised toward heaven, one pointing to earth",
            "The High Priestess": "front-facing centered seated meditation pose with hands resting on sacred geometry",
            "The Emperor": "front-facing centered authoritative standing pose with arms crossed over geometric chest piece",
            "The Empress": "front-facing centered nurturing pose with arms open in welcoming embrace",
            "The Hierophant": "front-facing centered blessing pose with both hands raised in sacred mudra",
            "The Lovers": "front-facing centered balanced pose with arms extended in harmonious gesture",
            "The Chariot": "front-facing centered forward-leaning pose with hands gripping ethereal reins",
            "Strength": "front-facing centered gentle pose with hands in taming gesture over geometric beast",
            "Wheel of Fortune": "front-facing centered spinning pose with arms in circular motion",
            "Justice": "front-facing centered balanced pose holding geometric scales in one hand",
            "The Hanged Man": "front-facing centered suspended pose with arms at sides in surrender",
            "Death": "front-facing centered transformative striding pose with scythe-like geometric tool",
            "Temperance": "front-facing centered pouring pose with hands managing flow between vessels",
            "The Devil": "front-facing centered crouched binding pose with chains of geometric patterns",
            "The Tower": "front-facing centered dramatic pose with arms raised as if struck by lightning",
            "The Star": "front-facing centered kneeling pose pouring geometric patterns like starlight",
            "The Moon": "front-facing centered howling pose with head tilted toward lunar geometry",
            "The Sun": "front-facing centered joyful dancing pose with arms raised in celebration",
            "Judgement": "front-facing centered rising pose with arms spread in resurrection gesture",
            "The World": "front-facing centered cosmic dancing pose within geometric mandala circle"
        }
        
        # Enhanced element outfits
        self.element_outfit_details = {
            "Air": {
                "base": "ethereal flowing robes with geometric wind patterns",
                "texture": "flat with sharpie-style lines for depth and movement",
                "details": "Air element glyphs and spiral motifs",
                "magical_essence": "faint wind wisps and floating geometric particles"
            },
            "Fire": {
                "base": "angular armor-like robes with flame geometric patterns",
                "texture": "flat with sharpie-style lines for heat and energy",
                "details": "Fire element triangular motifs and ascending patterns",
                "magical_essence": "flickering flame wisps and ember particles"
            },
            "Water": {
                "base": "fluid draped garments with wave geometric patterns",
                "texture": "flat with sharpie-style lines for flow and depth",
                "details": "Water element curved motifs and descending patterns",
                "magical_essence": "rippling water wisps and droplet particles"
            },
            "Earth": {
                "base": "structured solid robes with crystalline geometric patterns",
                "texture": "flat with sharpie-style lines for stability and grounding",
                "details": "Earth element square motifs and foundational patterns",
                "magical_essence": "crystalline dust wisps and mineral particles"
            },
            "Spirit": {
                "base": "transcendent layered robes combining all elemental patterns",
                "texture": "flat with sharpie-style lines for unity and synthesis",
                "details": "Spirit element pentagram motifs and unifying patterns",
                "magical_essence": "rainbow essence wisps and transcendent particles"
            }
        }
        
        # Enhanced sephirot accessories
        self.sephirot_accessories = {
            "Kether": "crown of pure geometric light with emanating patterns",
            "Chokhmah": "wand of wisdom with spiral geometric engravings",
            "Binah": "cup of understanding with triangular geometric patterns",
            "Chesed": "orb of mercy with hexagonal geometric surface",
            "Geburah": "sword of severity with angular geometric blade",
            "Tiphareth": "solar medallion with golden ratio geometric design",
            "Netzach": "rose of victory with seven-fold geometric petals",
            "Hod": "caduceus of communication with intertwined geometric serpents",
            "Yesod": "lunar crescent with silver geometric inscriptions",
            "Malkuth": "earthen cube with all geometric patterns unified"
        }

    def _load_tradition_traits(self) -> Dict[str, Dict[str, List[str]]]:
        """Load comprehensive tradition traits dictionary"""
        return {
            "enochian_magic": {
                "clothing": ["White linen robes with sigils", "hooded cloaks inscribed with angelic names", "tablet-embroidered tunics", "Aethyr-layered vests"],
                "accessories": ["Holy Table miniature", "PELE ring", "Enochian chess pieces", "crystal scrying ball", "sigil-etched wand"],
                "fabrics": ["Translucent silk with geometric overlays", "starched cotton for rigidity", "embroidered velvet with golden threads", "ethereal gauze suggesting Aethyrs"]
            },
            "hermetic_qabalah": {
                "clothing": ["Tree of Life embroidered robes", "Sephiroth-colored sashes", "pathworking capes", "divine name tabards"],
                "accessories": ["Lamen pendant", "Hexagram talisman", "Path symbols on belts", "Qabalistic rose cross"],
                "fabrics": ["Brocade with symbolic patterns", "heavy wool for grounding", "silk with metallic weaves", "layered linen representing veils"]
            },
            "thelema": {
                "clothing": ["Scarlet woman gowns", "black Nuit-inspired cloaks", "Hadit-winged jackets", "True Will inscribed shirts"],
                "accessories": ["Stele of Revealing replica", "Abrahadabra talisman", "Holy Guardian Angel evocation tool", "Thelemic phoenix brooch"],
                "fabrics": ["Velvet with starry patterns", "leather with embossed symbols", "flowing chiffon for freedom", "red-dyed cotton for passion"]
            },
            "celtic_druidic": {
                "clothing": ["Green hooded druid robes", "torque-collared tunics", "ogham-scripted cloaks", "sacred grove mantles"],
                "accessories": ["Torc necklace", "mistletoe sickle", "Awen-inspired staff", "Celtic knot amulet"],
                "fabrics": ["Woolen plaids with natural dyes", "bark-textured linen", "fur-trimmed hides", "woven reeds for elemental connection"]
            },
            "chaos_magic": {
                "clothing": ["Paradigm-shifting patchwork robes", "sigil-collage jackets", "belief-altering capes", "meta-magic hoods"],
                "accessories": ["Servitor creation tools", "chaos star pendant", "random symbol dice", "paradigm wheel"],
                "fabrics": ["Mismatched fabrics sewn together", "synthetic blends for modernity", "rubberized materials for flexibility", "printed cotton with custom sigils"]
            },
            "alchemy": {
                "clothing": ["Alchemical apron over robes", "hermaphroditic dual-toned garments", "Great Work symbolic vests", "transmutation cloaks"],
                "accessories": ["Athanor miniature", "philosopher's stone replica", "elixir vial necklace", "alchemical retort pendant"],
                "fabrics": ["Metallic-threaded silk", "stained linen from experiments", "leather with etched symbols", "iridescent fabrics suggesting transmutation"]
            },
            "golden_dawn": {
                "clothing": ["Grade-specific colored robes", "elemental quarter tunics", "ritual officer mantles", "invocation capes"],
                "accessories": ["Rose Cross lamen", "elemental dagger", "pentacle disk", "wand of power"],
                "fabrics": ["Satin with embroidered borders", "velvet with zodiac symbols", "cotton with colored hems", "layered gauze for veils"]
            },
            "taoism": {
                "clothing": ["Flowing Taoist priest robes", "yin-yang balanced tunics", "wu wei minimalist garments", "taiji pattern sashes"],
                "accessories": ["Bagua mirror", "yin-yang pendant", "bamboo staff", "I Ching coins"],
                "fabrics": ["Natural silk for flow", "cotton with circular patterns", "hemp for simplicity", "breathable linen suggesting qi movement"]
            },
            "traditional_kabbalah": {
                "clothing": ["Tzitzit-fringed prayer shawls", "tefillin-wrapped robes", "sefirot-mapped cloaks", "mystical tallit"],
                "accessories": ["Mezuzah amulet", "Kabbalistic tree pendant", "divine name scroll", "yarmulke with symbols"],
                "fabrics": ["Wool with knotted fringes", "linen with Hebrew script", "velvet for sacred texts", "striped fabrics representing paths"]
            },
            "sufism": {
                "clothing": ["Whirling dervish skirts", "simple woolen robes", "ecstatic dance mantles", "divine love sashes"],
                "accessories": ["Prayer beads (misbaha)", "reed flute", "Sufi heart pendant", "zikr ring"],
                "fabrics": ["Coarse wool for humility", "spinning-friendly cotton", "embroidered silk with Arabic calligraphy", "light fabrics for ecstasy"]
            },
            "gnosticism": {
                "clothing": ["Archon-resistant armored robes", "divine spark tunics", "pleroma-inspired capes", "sophia wisdom vests"],
                "accessories": ["Gnostic gem amulet", "serpent Ouroboros ring", "demiurge-binding chain", "hymn scroll"],
                "fabrics": ["Reinforced leather for protection", "metallic weaves for divine light", "dark fabrics with hidden symbols", "translucent veils for revelation"]
            },
            "norse_traditions": {
                "clothing": ["Rune-etched Viking tunics", "fur-lined cloaks", "valknut-patterned garments", "Yggdrasil tree robes"],
                "accessories": ["Mjolnir pendant", "rune stones", "Odin raven brooch", "Valkyrie helm"],
                "fabrics": ["Fur-trimmed wool", "leather with stamped runes", "chainmail accents", "woven fabrics with knotwork"]
            },
            "greek_philosophy": {
                "clothing": ["Toga-style philosophical robes", "laurel-wreathed tunics", "Stoic minimalist garments", "Platonic ideal capes"],
                "accessories": ["Lyre miniature", "olive branch staff", "Socratic dialogue scroll", "golden mean compass"],
                "fabrics": ["White linen drapes", "wool with geometric borders", "simple cotton for virtue", "silk with philosophical symbols"]
            },
            "tarot": {
                "clothing": ["Arcana-illustrated cloaks", "Major/Minor suit robes", "fool's motley tunic", "tower-structured vests"],
                "accessories": ["Tarot deck pouch", "key of Solomon pendant", "wheel of fortune medallion", "trump symbol brooch"],
                "fabrics": ["Patterned velvet with card imagery", "embroidered satin", "layered paper-like fabrics", "colorful accents on grey base"]
            },
            "i_ching": {
                "clothing": ["Hexagram-patterned robes", "trigram sashes", "change-dynamic capes", "oracle consultant tunics"],
                "accessories": ["Yarrow stalks", "hexagram coins", "bagua mirror", "change book pendant"],
                "fabrics": ["Silk with line patterns", "bamboo-woven fabrics", "flexible cotton for adaptation", "black/white duality weaves"]
            },
            "astrology": {
                "clothing": ["Zodiac-embroidered robes", "planetary symbol tunics", "horoscope chart capes", "stellar alignment vests"],
                "accessories": ["Astrolabe pendant", "zodiac wheel ring", "planetary talisman", "star map scroll"],
                "fabrics": ["Celestial-patterned velvet", "metallic thread for planets", "dark fabrics with star points", "flowing silk for cosmic movement"]
            },
            "natal_astrology": {
                "clothing": ["Birth chart mapped garments", "ascendant sign robes", "house division sashes", "transit tracking cloaks"],
                "accessories": ["Natal wheel amulet", "aspect symbol pins", "house ruler medallions", "progression calculator"],
                "fabrics": ["Personalized patterned linen", "zodiac-dyed cotton", "layered fabrics for houses", "starry gauze overlays"]
            },
            "egyptian_magic": {
                "clothing": ["Pharaoh-inspired linen robes", "ankh-collared tunics", "Nile god capes", "heka-symbol vests"],
                "accessories": ["Ankh cross", "scarab amulet", "was scepter", "eye of Horus pendant"],
                "fabrics": ["White linen with hieroglyphs", "gold-threaded cotton", "papyrus-like textures", "beaded fabrics for protection"]
            },
            "shamanism": {
                "clothing": ["Animal spirit hide cloaks", "feather-adorned tunics", "journey drum vests", "totem pole garments"],
                "accessories": ["Medicine bag", "spirit rattle", "power animal fetish", "dream catcher"],
                "fabrics": ["Animal hides with natural markings", "feathered wool", "beaded leather", "woven grass for earth connection"]
            },
            "numerology": {
                "clothing": ["Number-patterned robes", "sacred digit tunics", "Pythagorean theorem capes", "vibration level sashes"],
                "accessories": ["Number wheel pendant", "abacus talisman", "sacred ratio compass", "digit ring"],
                "fabrics": ["Geometric-printed cotton", "numerical embroidered silk", "layered fabrics for multiples", "harmonic patterned linen"]
            },
            "sacred_geometry": {
                "clothing": ["Platonic solid robes", "golden ratio tunics", "flower of life capes", "metatron cube vests"],
                "accessories": ["Geometric compass", "crystal grid pendant", "vesica piscis amulet", "fractal mirror"],
                "fabrics": ["Patterned silk with ratios", "crystalline-textured fabrics", "metallic weaves for shapes", "layered paper for dimensions"]
            },
            "quantum_physics": {
                "clothing": ["Wave-particle duality garments", "entanglement-linked robes", "observer effect capes", "superposition tunics"],
                "accessories": ["Quantum bit pendant", "Schrödinger box amulet", "wave function staff", "particle accelerator ring"],
                "fabrics": ["Holographic fabrics", "probabilistic patterns on cotton", "metallic quantum dots", "fluctuating textures"]
            },
            "kuji_kiri": {
                "clothing": ["Ninja hand seal robes", "mudra-patterned tunics", "energy channel sashes", "protection grid capes"],
                "accessories": ["Kuji-in hand symbols", "ninja star talisman", "energy blade", "seal scroll"],
                "fabrics": ["Black cotton for stealth", "embroidered silk with seals", "flexible fabrics for movement", "reinforced linen for protection"]
            },
            "greek_mythology": {
                "clothing": ["Olympian chiton robes", "god-symbol tunics", "heroic quest capes", "mythic creature vests"],
                "accessories": ["Thunderbolt pendant", "aegis shield amulet", "golden fleece brooch", "labyrinth map"],
                "fabrics": ["Draped linen with myths", "wool with border patterns", "leather with embossed gods", "flowing fabrics for epics"]
            },
            "digital_physics": {
                "clothing": ["Pixelated code robes", "simulation glitch tunics", "holographic interface capes", "algorithm pattern vests"],
                "accessories": ["Binary code pendant", "matrix glitch amulet", "simulation console", "bit stream ring"],
                "fabrics": ["Digital-printed fabrics", "glitch-textured cotton", "holographic weaves", "circuit-patterned silk"]
            },
            "m_theory": {
                "clothing": ["Multidimensional string robes", "brane-world tunics", "unified field capes", "superstring vests"],
                "accessories": ["String theory loop pendant", "membrane amulet", "dimension portal", "quantum foam brooch"],
                "fabrics": ["Vibrating patterned silk", "multidimensional layered fabrics", "wave-like wool", "unified metallic threads"]
            },
            # Additional traditions and aliases
            "hermetic_philosophy": {
                "clothing": ["Hermetic axiom robes", "as above so below tunics", "alchemical wisdom capes", "emerald tablet vests"],
                "accessories": ["Hermetic seal pendant", "caduceus staff", "philosophical mercury vial", "axiom scroll"],
                "fabrics": ["Wisdom-woven silk", "axiom-embroidered linen", "philosophical cotton", "hermetic velvet with symbols"]
            },
            "complexity_science": {
                "clothing": ["Fractal pattern robes", "emergence theory tunics", "chaos theory capes", "systems dynamics vests"],
                "accessories": ["Butterfly effect pendant", "strange attractor model", "complexity compass", "emergence calculator"],
                "fabrics": ["Fractal-patterned silk", "emergent cotton weaves", "chaotic fiber blends", "complex system textiles"]
            },
            "scrying": {
                "clothing": ["Crystal gazer robes", "vision-seeking tunics", "prophetic sight capes", "oracle divination vests"],
                "accessories": ["Crystal ball", "scrying mirror", "vision stone", "prophetic lens"],
                "fabrics": ["Translucent vision silk", "crystal-clear linen", "prophetic gauze", "oracle-woven cotton"]
            },
            "ritual_magic": {
                "clothing": ["Ceremonial ritual robes", "invocation tunics", "banishing capes", "circle-casting vests"],
                "accessories": ["Ritual athame", "ceremonial chalice", "invocation wand", "banishing pentacle"],
                "fabrics": ["Ceremonial silk", "ritual-blessed linen", "sacred cotton", "consecrated velvet"]
            }
        }

    def get_deterministic_seed(self, governor_name: str) -> int:
        """Generate deterministic seed based on governor name for reproducibility"""
        return int(hashlib.md5(governor_name.encode()).hexdigest()[:8], 16)

    def extract_knowledge_base_traditions(self, knowledge_base: Dict) -> List[str]:
        """Extract all traditions from governor's knowledge base"""
        traditions = []
        for category, systems in knowledge_base.items():
            if isinstance(systems, list):
                traditions.extend(systems)
            elif isinstance(systems, str):
                traditions.append(systems)
        return list(set(traditions))  # Remove duplicates

    def generate_tradition_traits(self, traditions: List[str], governor_name: str) -> Dict[str, List[str]]:
        """Generate combined tradition traits with deterministic randomness"""
        random.seed(self.get_deterministic_seed(governor_name))
        
        combined_traits = {
            "clothing": [],
            "accessories": [],
            "fabrics": []
        }
        
        for tradition in traditions:
            if tradition in self.tradition_traits:
                traits = self.tradition_traits[tradition]
                
                # Select 2-3 clothing traits
                clothing_count = random.randint(2, 3)
                selected_clothing = random.sample(traits["clothing"], min(clothing_count, len(traits["clothing"])))
                combined_traits["clothing"].extend(selected_clothing)
                
                # Select 1-2 accessories
                accessory_count = random.randint(1, 2)
                selected_accessories = random.sample(traits["accessories"], min(accessory_count, len(traits["accessories"])))
                combined_traits["accessories"].extend(selected_accessories)
                
                # Select 1 fabric
                selected_fabric = random.choice(traits["fabrics"])
                combined_traits["fabrics"].append(selected_fabric)
        
        return combined_traits

    def enhanced_descriptor_extraction(self, profile_data: Dict) -> Dict[str, List[str]]:
        """Enhanced descriptor extraction with NLP-like improvements"""
        
        # Enhanced patterns with more sophisticated matching
        form_desc = profile_data.get('form_description', '')
        form_words = re.findall(r'\b(translucent|prismatic|multi-faceted|interconnected|planes|fractal|edges|shift|definition|ethereality|crystal|luminous|geometric|fluid|flame|solid|organic|spiral|wave|angular|curved|flowing|structured|radiant|shimmering|iridescent|opalescent|crystallographic|merkaba|rotating|pulsing|vibrating|shifting|dynamic|ethereal|transcendent|mystical|divine|sacred|holy|blessed|brilliant|gleaming|sparkling|glowing|incandescent|faceted|crystalline|prismatic|geometric|multifaceted|oak-wood|oak|wood|crystalline)\b', form_desc, re.IGNORECASE)
        unique_form = list(dict.fromkeys(form_words))
        
        # Enhanced role extraction
        role_desc = profile_data.get('angelic_role', '')
        role_words = re.findall(r'\b(virtue|winds|equilibrium|commands|empyrean|legions|dance|guides|herald|messenger|guardian|warrior|sage|keeper|weaver|catalyst|throne|cherub|seraph|dominion|prince|princess|lord|lady|master|mistress|angel|archangel|power|principality|authority|ruler|commander|leader|marshals|hosts|oak-crowned)\b', role_desc, re.IGNORECASE)
        
        # Enhanced essence extraction
        essence_desc = profile_data.get('essence', '')
        essence_words = re.findall(r'\b(balanced|benevolent|gentle|wind|fairness|compassion|clears|prejudice|cosmic|choreography|strategy|crystallize|provident|insight|methodical|exhilarating|imminent|catalytic|breaks|bonds|motivates|transcendent|mystical|ethereal|divine|sacred|holy|blessed|luminous|radiant|flowing|shifting|dynamic|transformative|harmonious|peaceful|powerful|wise|ancient|eternal|infinite|depths|darkness|humility|arrogance|pride|anonymous|blessing|assistance|fear|fearless|strength|introspection|flame|steady|resolve|melts|aura|forges|lights|time|still|eternity|ages|wheel|intuition|cycles|reflection|patterns|repeat|comforting|lunar|phases|paradoxical|sunlight|spirit-fire|burns|dims|transmutes)\b', essence_desc, re.IGNORECASE)
        
        # Enhanced geometry extraction
        geo_desc = profile_data.get('geometry_reasoning', '')
        geo_themes = re.findall(r'\b(equilibrium|cosmic|law|transformative|potential|dance|dimensional|transition|interconnectedness|wisdom|precision|complexity|infinite|strategic|beehive|platonic|solids|fractal|patterns|sacred|divine|mystical|transcendent|unity|harmony|balance|order|structure|foundation|stability|flow|movement|energy|light|darkness|creation|destruction|renewal|rebirth|depths|tides|humility|pride|anonymous|blessing|geometric|tetrahedron|octahedron|stellated|polyhedron|hexagonal|mobius|crescent|spiral|perfect|spiritual|geometry|merkaba|symbolizes|vehicle|transformation|flower|life|indicates|interconnectedness)\b', geo_desc, re.IGNORECASE)
        
        # Enhanced color extraction
        color_desc = profile_data.get('color_reasoning', '')
        color_moods = re.findall(r'\b(silver|lunar|wisdom|azure|clarity|electric|blue|golden|crimson|emerald|violet|mercurial|intelligence|communication|celestial|transmission|shifting|dynamic|nature|revelation|radiant|luminous|brilliant|shimmering|iridescent|opalescent|metallic|crystalline|prismatic|translucent|transparent|opaque|solid|fluid|flowing|structured|depths|darkness|tides|anonymous|fear|fearless|strength|flame|steady|time|eternity|intuition|cycles|reflection|patterns|comforting|phases|saffron|spiritual|fire|sagittarian|expansiveness|indigo|deep|vision|insight|transformative|energy)\b', color_desc, re.IGNORECASE)
        
        return {
            'head_descriptors': [w for w in unique_form if w.lower() != 'crystal'] + geo_themes[:2],
            'appendage_style': role_words + essence_words[:3],
            'motion_vibe': essence_words[:2] + geo_themes[:1],
            'color_influences': color_moods[:3],
            'primary_form_words': unique_form[:3]
        }

    def calculate_distinctiveness_score(self, visual_elements: Dict) -> float:
        """Calculate distinctiveness score for quality control"""
        unique_elements = set()
        
        # Count unique descriptors
        if 'unique_descriptors' in visual_elements:
            for category, descriptors in visual_elements['unique_descriptors'].items():
                if isinstance(descriptors, list):
                    unique_elements.update(descriptors)
        
        # Count tradition traits
        if 'tradition_traits' in visual_elements:
            for category, traits in visual_elements['tradition_traits'].items():
                if isinstance(traits, list):
                    unique_elements.update(traits)
        
        # Score based on uniqueness (higher is more distinctive)
        return len(unique_elements) / 20.0  # Normalize to 0-1 range

    def interpret_color_to_greyscale(self, color_name: str, color_influences: List[str] = None) -> str:
        """Enhanced color interpretation with mood influences"""
        base_color_map = {
            "silvery-white": "light grey with metallic sheen",
            "pale azure": "mid-grey with cool undertones",
            "electric blue": "dark grey with high contrast",
            "golden": "warm light grey",
            "crimson": "dark grey with intensity",
            "emerald": "mid-grey with depth",
            "violet": "dark grey with mystery",
            "orange": "warm mid-grey",
            "white": "pure light grey",
            "black": "pure dark grey",
            "silver": "metallic light grey",
            "copper": "warm mid-grey with texture",
            "azure": "cool mid-grey",
            "blue": "cool dark grey",
            "gold": "warm light grey",
            "red": "dark grey with warmth",
            "green": "mid-grey with natural tone",
            "purple": "dark grey with depth",
            "yellow": "bright light grey",
            "pink": "soft light grey",
            "brown": "warm dark grey",
            "grey": "neutral grey",
            "gray": "neutral grey",
            "saffron": "warm golden grey",
            "indigo": "deep dark grey"
        }
        
        base_color = base_color_map.get(color_name.lower(), "neutral grey")
        
        if color_influences and len(color_influences) > 0:
            mood_descriptor = color_influences[0]
            if mood_descriptor:
                return f"{base_color} inspired by {mood_descriptor}"
        
        return base_color

    def generate_enhanced_prompt(self, profile: Dict) -> Dict[str, Any]:
        """Generate enhanced visual prompt with tradition traits and improved templating"""
        gov_profile = profile["governor_profile"]
        governor_name = profile["governor_name"]

        # Extract visual data
        visual_aspects = gov_profile.get("visual_aspects", {})
        form_data = visual_aspects.get("form", {})
        color_data = visual_aspects.get("color", {})
        geometry_data = visual_aspects.get("geometry", {})

        # Core attributes
        element = gov_profile.get("element", "Air")
        tarot = gov_profile.get("archetypal_correspondences", {}).get("tarot", "The Hermit")
        sephirot = gov_profile.get("archetypal_correspondences", {}).get("sephirot", "Kether")
        zodiac = gov_profile.get("archetypal_correspondences", {}).get("zodiac_sign", "Aries")
        aethyr = gov_profile.get("aethyr", "")
        title = gov_profile.get("title", "")
        essence = gov_profile.get("essence", "")

        # Extract knowledge base traditions
        knowledge_base = gov_profile.get("knowledge_base", {})
        traditions = self.extract_knowledge_base_traditions(knowledge_base)

        # Generate tradition traits
        tradition_traits = self.generate_tradition_traits(traditions, governor_name)

        # Extract unique descriptors with enhanced NLP
        profile_data = {
            'form_description': form_data.get("description", ""),
            'angelic_role': gov_profile.get("angelic_role", ""),
            'essence': essence,
            'geometry_reasoning': geometry_data.get("reasoning", ""),
            'color_reasoning': color_data.get("reasoning", "")
        }

        descriptors = self.enhanced_descriptor_extraction(profile_data)

        # Enhanced color interpretation
        primary_color = self.interpret_color_to_greyscale(
            color_data.get("primary", "white"),
            descriptors['color_influences']
        )
        secondary_color = self.interpret_color_to_greyscale(
            color_data.get("secondary", "grey"),
            descriptors['color_influences'][1:] if len(descriptors['color_influences']) > 1 else []
        )
        color_pattern = color_data.get("pattern", "shifting")

        geometry_patterns = geometry_data.get("patterns", ["geometric"])

        # Create distinctive head shape
        if descriptors['head_descriptors'] and len(descriptors['head_descriptors']) > 0:
            head_descriptors_str = ' '.join(descriptors['head_descriptors'][:3])
            head_shape = f"large {head_descriptors_str} head with unique {geometry_patterns[0] if geometry_patterns else 'geometric'} structure"
        else:
            form_name = form_data.get("name", "crystalline")
            head_shape = f"large {form_name} head with {geometry_patterns[0] if geometry_patterns else 'sacred'} patterns"

        # Create distinctive hair/appendage style
        if descriptors['appendage_style'] and len(descriptors['appendage_style']) > 0:
            appendage_influences = ' '.join(descriptors['appendage_style'][:2])
            hair_style = f"geometric appendages incorporating {', '.join(geometry_patterns)} patterns, styled with {appendage_influences} influences"
        else:
            hair_style = f"geometric appendages incorporating {', '.join(geometry_patterns)} patterns from sacred geometry symbolism"

        # Create distinctive motion quality
        if descriptors['motion_vibe'] and len(descriptors['motion_vibe']) > 0:
            motion_influences = ' '.join(descriptors['motion_vibe'][:2])
            motion_quality = f"suggesting stillness and motion through sharp, layered cut-outs with drawn depth, embodying {motion_influences}"
        else:
            motion_quality = "suggesting stillness and motion through sharp, layered cut-outs with drawn depth"

        # Generate tradition-enhanced outfit
        base_outfit = self.element_outfit_details.get(element, self.element_outfit_details["Air"])

        # Combine tradition clothing traits
        if tradition_traits["clothing"]:
            tradition_clothing = " fused with " + " and ".join(tradition_traits["clothing"][:2])
            enhanced_outfit_base = base_outfit["base"] + tradition_clothing
        else:
            enhanced_outfit_base = base_outfit["base"]

        # Combine tradition fabric traits
        if tradition_traits["fabrics"]:
            tradition_fabric = tradition_traits["fabrics"][0]
            enhanced_texture = f"{base_outfit['texture']}, incorporating {tradition_fabric}"
        else:
            enhanced_texture = base_outfit["texture"]

        # Generate tradition-enhanced accessories
        base_accessory = self.sephirot_accessories.get(sephirot, "geometric emblem")
        if tradition_traits["accessories"]:
            tradition_accessory = tradition_traits["accessories"][0]
            enhanced_accessory = f"{base_accessory} combined with {tradition_accessory}"
        else:
            enhanced_accessory = base_accessory

        pose_gesture = self.tarot_gesture_interpretations.get(tarot, "front-facing centered standing with contemplative gesture")
        sacred_geometry = geometry_patterns[0] if geometry_patterns else "Flower of Life"
        energy_type = descriptors['motion_vibe'][0] if descriptors['motion_vibe'] and len(descriptors['motion_vibe']) > 0 else "ethereal"
        magical_essence = base_outfit["magical_essence"]

        # Construct enhanced prompt with dynamic templating
        prompt = (
            f"A chibi-style character in greyscale construction paper cut-out aesthetic, "
            f"flat shapes with sharp edges and minimal shading, on transparent background. "
            f"The face is solid black with no features. "
            f"The body is in a {pose_gesture}, chibi proportions with {head_shape} "
            f"{motion_quality}. "
            f"Hair or {hair_style}. "
            f"Outfit is unique: {primary_color} and {secondary_color} {enhanced_outfit_base} with "
            f"{enhanced_texture}, elaborate with {color_pattern} {base_outfit['details']} "
            f"and {sacred_geometry} emblem on chest; texture flat with sharpie-style lines for depth. "
            f"Include subtle accessory like {enhanced_accessory} with {energy_type} spiraling energy emanations. "
            f"Environmental effect: sacred geometric field creating geometric aura patterns around the character "
            f"with subtle magical essence emanations like {magical_essence}. "
            f"Emulate construction paper layering style exactly, but make this visually unique based on "
            f"Governor {governor_name}'s profile: {title}, Aethyr {aethyr}, {element} element, "
            f"Tarot {tarot}, Sephirot {sephirot}, Zodiac {zodiac}, embodying the essence: "
            f"'{essence}' "
            f"Resolution 512x512, optimized for layering in Enochian Cyphers game and WebGL rendering with TAP hypertoken metadata embedding."
        )

        # Enhanced visual elements structure
        visual_elements = {
            "pose": pose_gesture,
            "head_shape": head_shape,
            "body_style": f"angular geometric body with {descriptors['primary_form_words'][0] if descriptors['primary_form_words'] and len(descriptors['primary_form_words']) > 0 else 'geometric'} facets, flattened with sharpie-like crease lines",
            "motion_quality": motion_quality,
            "hair_style": hair_style,
            "outfit": {
                "base": enhanced_outfit_base,
                "texture": enhanced_texture,
                "details": base_outfit["details"],
                "magical_essence": magical_essence
            },
            "accessory": enhanced_accessory,
            "primary_color": primary_color,
            "secondary_color": secondary_color,
            "color_pattern": color_pattern,
            "geometry_patterns": geometry_patterns,
            "sacred_geometry": sacred_geometry,
            "secondary_symbols": [f"{zodiac}_glyph", f"{element}_symbol"],
            "energy_signature": {
                "type": energy_type,
                "flow": f"spiraling with magical essence wisps"
            },
            "environment_effect": "sacred geometric field with faint aura lines",
            "element": element,
            "tarot": tarot,
            "sephirot": sephirot,
            "zodiac": zodiac,
            "unique_descriptors": descriptors,
            "tradition_traits": tradition_traits,
            "traditions_used": traditions
        }

        # Calculate distinctiveness score
        distinctiveness_score = self.calculate_distinctiveness_score(visual_elements)

        return {
            "governor_name": governor_name,
            "prompt": prompt,
            "visual_elements": visual_elements,
            "profile_data": {
                "title": title,
                "aethyr": aethyr,
                "element": element,
                "essence": essence,
                "angelic_role": gov_profile.get("angelic_role", ""),
                "form_description": form_data.get("description", ""),
                "color_reasoning": color_data.get("reasoning", ""),
                "geometry_reasoning": geometry_data.get("reasoning", ""),
                "knowledge_base": knowledge_base
            },
            "quality_metrics": {
                "distinctiveness_score": distinctiveness_score,
                "traditions_count": len(traditions),
                "unique_descriptors_count": sum(len(v) if isinstance(v, list) else 1 for v in descriptors.values())
            }
        }

    def load_governor_profile(self, governor_name: str) -> Dict:
        """Load governor profile with error handling"""
        profile_path = self.governor_profiles_dir / f"{governor_name}.json"
        try:
            with open(profile_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Profile not found: {governor_name}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON for {governor_name}: {e}")
            return None

    def generate_all_enhanced_prompts(self):
        """Generate all enhanced visual prompts with tradition traits"""
        profile_files = list(self.governor_profiles_dir.glob("*.json"))
        profile_files = [f for f in profile_files if f.name != "README.md"]

        print(f"Generating enhanced visual prompts for {len(profile_files)} governors...")

        generated_count = 0
        quality_scores = []

        for profile_file in sorted(profile_files):
            governor_name = profile_file.stem

            profile = self.load_governor_profile(governor_name)
            if not profile:
                continue

            prompt_data = self.generate_enhanced_prompt(profile)

            # Save enhanced prompt
            output_file = self.output_dir / f"{governor_name}_visual_prompt.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(prompt_data, f, indent=2, ensure_ascii=False)

            quality_scores.append(prompt_data["quality_metrics"]["distinctiveness_score"])
            generated_count += 1
            print(f"Enhanced: {governor_name} (Score: {prompt_data['quality_metrics']['distinctiveness_score']:.2f})")

        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        print(f"\nSuccessfully generated {generated_count} enhanced visual prompts")
        print(f"Average distinctiveness score: {avg_quality:.2f}")
        print(f"Enhanced files saved in: {self.output_dir}")

def main():
    """Main function"""
    generator = EnhancedVisualPromptGenerator()
    generator.generate_all_enhanced_prompts()

if __name__ == "__main__":
    main()

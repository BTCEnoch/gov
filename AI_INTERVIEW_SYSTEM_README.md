# 🎭 Enochian Cyphers AI Interview System

## Overview

This system conducts AI-mediated interviews with each of the 91 Governor Angels, where Claude AI role-plays as each governor to determine their visual manifestation aspects. Each governor draws from their complete profile, mystical correspondences, and knowledge base to answer structured interview questions about their visual appearance.

## 🏗️ Architecture

### Core Components

1. **`ai_interview_system.py`** - Main interview engine
2. **`run_ai_interviews.py`** - CLI interface for running interviews  
3. **`update_profiles_with_ai_results.py`** - Post-processing to update profiles
4. **Interview Templates** - Structured questions in `core/governors/profiler/interview/templates/`
5. **Governor Profiles** - Complete governor data in `core/governors/profiles/`

### Interview Process Flow

```
Governor Profile → AI Agent Role-Play → Structured Interview → Visual Aspects → Profile Update
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Ensure your `.env` file contains:
```bash
ANTHROPIC_API_KEY=your_anthropic_api_key_here
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022  # Optional, this is default
```

### 3. Test Configuration

```bash
python run_ai_interviews.py --dry-run
```

### 4. Run Interviews

**All 91 governors (full production run):**
```bash
python run_ai_interviews.py
```

**Test with first 5 governors:**
```bash
python run_ai_interviews.py --limit 5
```

**Specific governors only:**
```bash
python run_ai_interviews.py --governors "OCCODON,PASCOMB,VALGARS"
```

### 5. Update Profiles

```bash
python update_profiles_with_ai_results.py
```

## 📋 Command Reference

### Interview Runner Options

```bash
python run_ai_interviews.py [OPTIONS]

Options:
  --governors TEXT        Comma-separated governor names to interview
  --limit INTEGER         Limit number of governors (for testing)
  --concurrent INTEGER    Max concurrent interviews (default: 3)
  --output-dir TEXT       Output directory for results
  --verbose              Enable verbose logging
  --dry-run              Check configuration without running
```

### Profile Updater Options

```bash
python update_profiles_with_ai_results.py [OPTIONS]

Options:
  --results-dir TEXT     Directory with AI interview results
  --profiles-dir TEXT    Directory with governor profiles
  --summary-only         Only generate summary, don't update profiles
```

## 🎭 How the AI Interview Works

### 1. Governor Role-Play Setup

Each AI agent receives a comprehensive system prompt containing:

- **Core Identity**: Name, title, element, Aethyr, angelic role
- **Archetypal Correspondences**: Tarot, Sephirot, Zodiac associations  
- **Mystical Knowledge**: 18 tradition knowledge base access
- **Personality Traits**: Virtues, role archetype, polar traits
- **Essential Nature**: Unique essence and manifestation

### 2. Interview Questions

The AI answers structured questions across 5 categories:

- **Form & Manifestation**: Base form type, complexity, symmetry
- **Color & Light**: Primary colors, patterns, intensity
- **Sacred Geometry**: Geometric patterns, complexity, motion
- **Temporal Patterns**: Time cycles, flow, stability  
- **Energy Signatures**: Energy type, flow patterns, intensity

### 3. Response Format

Each governor provides detailed JSON responses with reasoning:

```json
{
  "visual_aspects": {
    "form": {
      "name": "organic",
      "description": "Manifests as organic patterns reflecting Water elemental nature"
    },
    "color": {
      "primary": "violet",
      "secondary": "azure",
      "pattern": "shifting", 
      "intensity": "subtle",
      "reasoning": "Violet represents spiritual transformation while azure reflects my Water element..."
    }
    // ... additional categories
  }
}
```

## 📊 Output Structure

### Interview Results Directory
```
data/ai_interview_results/
├── OCCODON_interview.json          # Individual results
├── PASCOMB_interview.json
├── ...
├── interview_summary.json          # Batch summary
└── visual_aspects_summary.json     # Analysis summary
```

### Updated Governor Profiles
```
core/governors/profiles/
├── OCCODON.json                    # Updated with visual_aspects
├── PASCOMB.json
└── ...
```

## ⚡ Performance & Rate Limits

### Anthropic API Limits
- **Claude 3.5 Sonnet**: ~50 requests/minute
- **Concurrent Limit**: Default 3 (adjustable with `--concurrent`)
- **Cost Estimate**: ~$15-30 for all 91 governors

### Timing Estimates
- **5 governors**: ~2-3 minutes
- **91 governors**: ~30-45 minutes (with rate limiting)

## 🔍 Quality Assurance

### Built-in Validation
- JSON response parsing with error handling
- Raw response preservation for debugging
- Success/failure tracking and reporting
- Automatic retry logic for failed interviews

### Manual Review Points
1. Check `interview_summary.json` for success rates
2. Review failed interviews in individual result files
3. Validate visual aspects make sense for each governor's nature
4. Ensure mystical correspondences are properly reflected

## 🛠️ Troubleshooting

### Common Issues

**API Key Not Found:**
```bash
❌ ERROR: ANTHROPIC_API_KEY not found in environment
```
Solution: Check your `.env` file contains the API key

**Rate Limit Errors:**
```bash
❌ Interview failed for GOVERNOR: Rate limit exceeded
```
Solution: Reduce `--concurrent` parameter or wait and retry

**JSON Parsing Errors:**
```bash
❌ JSON parsing failed for GOVERNOR: Invalid JSON
```
Solution: Check raw responses in result files, may need prompt adjustment

### Debug Mode

Run with verbose logging:
```bash
python run_ai_interviews.py --verbose --limit 1
```

## 🎯 Integration Points

### TAP Protocol Integration
Visual aspects can be converted to TAP hypertoken metadata:
```python
# Example integration
visual_aspects = governor_profile["visual_aspects"]
hypertoken_metadata = convert_visual_to_tap_metadata(visual_aspects)
```

### Game Asset Pipeline
Visual aspects provide specifications for:
- 3D model generation
- Texture and material properties  
- Animation and effect parameters
- Environmental interaction rules

### Bitcoin L1 Deployment
All generated visual aspects are deterministic and can be:
- Inscribed as Ordinals for immutable storage
- Referenced in TAP Protocol contracts
- Distributed via P2P networks

## 📈 Next Steps

1. **Run Full Interview Batch** - All 91 governors
2. **Quality Review** - Validate generated visual aspects
3. **TAP Integration** - Convert to hypertoken metadata
4. **Asset Generation** - Create game assets from specifications
5. **Testing** - Integrate with game engine and validate rendering

---

**🔮 Ready to interview the 91 Governor Angels and manifest their visual aspects through AI-mediated mystical dialogue!**

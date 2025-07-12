# Governor Interview System

The Governor Interview System is designed to facilitate the generation of visual aspects for Enochian Governors through a structured interview process. This system enables batch processing of multiple governors while maintaining consistency and drawing from established knowledge bases.

## System Components

### 1. BatchInterviewProcessor

The main orchestrator that manages the processing of multiple governors in parallel:

- Handles concurrent processing with configurable batch sizes
- Manages file I/O for loading profiles and saving results
- Coordinates between interview system and content processor

```python
processor = BatchInterviewProcessor(knowledge_base_path, max_concurrent=5)
results = await processor.process_governors(governors)
```

### 2. GovernorInterviewSystem

Conducts individual governor interviews and manages the question/response flow:

- Loads predefined interview questions
- Manages response collection
- Maps responses to visual templates

```python
interview = GovernorInterviewSystem(knowledge_base_path)
responses = interview.conduct_interview(governor)
```

### 3. ContentProcessor

Processes interview responses and generates final visual aspects:

- Maps responses to visual templates
- Applies sacred geometry patterns
- Generates environment effects
- Handles special properties

## Knowledge Base Structure

### 1. Interview Questions (`interview_questions.json`)

Defines the structure and flow of the interview:

```json
{
  "questions": [
    {
      "id": "form_type",
      "category": "form",
      "question": "What is the primary form?",
      "options": ["geometric", "organic", ...]
    }
  ]
}
```

### 2. Visual Templates (`visual_templates.json`)

Maps interview responses to visual aspects:

```json
{
  "templates": {
    "form_type": {
      "geometric": {
        "name": "Geometric Form",
        "description": "Sacred geometry structure"
      }
    }
  }
}
```

## Visual Aspects Schema

The system generates visual aspects following this structure:

```json
{
  "form": {
    "name": "Form Name",
    "description": "Form Description"
  },
  "color": "COLOR_NAME",
  "geometry": {
    "patterns": ["PATTERN1", "PATTERN2"],
    "complexity": 1-5
  },
  "environment": {
    "effect_type": 1-4,
    "radius": 0-3,
    "intensity": 1-4
  },
  "time_variations": 0-255,
  "energy_signature": 0-255,
  "symbol_set": 0-255,
  "light_shadow": 0-255,
  "special_properties": [0-255, 0-255, 0-255, 0-255]
}
```

## Usage Example

```python
# Initialize processor
processor = BatchInterviewProcessor(knowledge_base_path)

# Load governor profiles
governors = processor.load_governor_profiles(profiles_dir)

# Process governors
results = await processor.process_governors(governors)

# Save results
processor.save_results(results, output_dir)
```

## Integration Points

1. **Knowledge Base**
   - Sacred geometry patterns
   - Color correspondences
   - Form templates
   - Environmental effects

2. **Trait System**
   - Governor profiles
   - Mystical attributes
   - Visual traits schema

3. **File System**
   - Profile loading
   - Result saving
   - Template management

## Best Practices

1. **Interview Questions**
   - Keep questions focused and specific
   - Provide clear options
   - Include helpful descriptions

2. **Visual Templates**
   - Use established correspondences
   - Maintain consistency in mappings
   - Document special cases

3. **Batch Processing**
   - Monitor memory usage
   - Handle errors gracefully
   - Log important events

4. **Result Validation**
   - Verify required fields
   - Check value ranges
   - Validate relationships

## Error Handling

The system implements comprehensive error handling:

1. **File Operations**
   - Missing files
   - Invalid JSON
   - Permission issues

2. **Processing**
   - Invalid responses
   - Missing templates
   - Conversion errors

3. **Validation**
   - Schema validation
   - Value range checks
   - Relationship verification

## Logging

Important events are logged for monitoring and debugging:

```python
logger.info("Starting governor interview: %s", governor.id)
logger.error("Failed to load template: %s", e)
logger.debug("Processing response: %s", response)
```

## Testing

The system includes comprehensive tests:

1. **Unit Tests**
   - Individual components
   - Error handling
   - Edge cases

2. **Integration Tests**
   - End-to-end flows
   - File operations
   - Batch processing

3. **Template Tests**
   - Question validation
   - Template mapping
   - Value ranges 
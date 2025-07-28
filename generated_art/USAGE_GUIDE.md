# Visual Prompt Batch Generation Guide

This directory contains batch processing files for generating AI art for all 91 Governor Angels.

## Available Formats

### 1. Simple Text File (`batch_prompts_simple.txt`)
- One prompt per line
- Ready for copy-paste into AI art generators
- Best for manual processing

### 2. CSV File (`batch_prompts.csv`)
- Spreadsheet-compatible format
- Includes metadata (element, tarot, colors)
- Good for analysis and filtering

### 3. JSON File (`batch_prompts.json`)
- Structured data format
- Complete metadata included
- Best for API integration

## API Integration Scripts

### Stable Diffusion (Automatic1111 WebUI)
```bash
# Start Automatic1111 WebUI with API enabled
python webui.py --api

# Run batch generation
python stable_diffusion_batch.py
```

### DALL-E API
```bash
# Set API key
export OPENAI_API_KEY="your-api-key-here"

# Run batch generation
python dalle_batch.py
```

## Manual Generation Tips

### Recommended Settings
- **Resolution**: 512x512 (can upscale later)
- **Style**: Construction paper, flat design, minimal shading
- **Colors**: Greyscale only, avoid color prompts
- **Background**: Transparent or white
- **Negative Prompts**: "color, colored, rainbow, bright colors"

### Quality Control
- Ensure faces remain solid black with no features
- Verify chibi proportions are maintained
- Check that accessories match the governor's role
- Confirm transparent background for layering

## Batch Processing Workflow

1. **Choose Format**: Select appropriate batch file format
2. **Configure API**: Set up your preferred AI art service
3. **Run Generation**: Execute batch processing script
4. **Quality Check**: Review generated images
5. **Post-Process**: Resize, optimize, or enhance as needed
6. **Integration**: Import into game engine or application

## File Organization

Generated images should follow this naming convention:
- `[GOVERNOR_NAME]_art.png` (e.g., `ABRIOND_art.png`)
- Store in organized directories by element or aethyr
- Maintain metadata for game integration

## TAP Protocol Integration

For blockchain integration:
- Each image can be inscribed as a TAP Protocol asset
- Include visual prompt as metadata
- Link to governor profile data
- Enable evolutionary mechanics through on-chain updates

## Troubleshooting

### Common Issues
- **Color bleeding**: Add stronger negative prompts
- **Wrong proportions**: Emphasize "chibi" in prompt
- **Background issues**: Specify "transparent background"
- **Feature visibility**: Ensure "solid black face, no features"

### Quality Optimization
- Generate multiple variations per governor
- Use consistent seed values for reproducibility
- Apply post-processing for consistency
- Test layering compatibility in target engine

---

*Generated: 2025-01-28*
*Total Prompts: 91*
*System: Enochian Cyphers Visual Generation v1.0*

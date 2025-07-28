#!/usr/bin/env python3
"""
DALL-E API Batch Generation
Requires: pip install openai pillow
Set OPENAI_API_KEY environment variable
"""

import json
import os
import requests
from pathlib import Path
from openai import OpenAI

# Configuration
OUTPUT_DIR = Path("generated_art/dalle")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_image(prompt, filename):
    """Generate image using DALL-E API"""
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        
        # Download and save image
        image_url = response.data[0].url
        image_response = requests.get(image_url)
        
        if image_response.status_code == 200:
            output_path = OUTPUT_DIR / filename
            with open(output_path, 'wb') as f:
                f.write(image_response.content)
            print(f"Generated: {filename}")
            return True
        else:
            print(f"Failed to download {filename}")
            return False
            
    except Exception as e:
        print(f"Error generating {filename}: {e}")
        return False

def main():
    """Main batch generation function"""
    # Load batch prompts
    with open("batch_prompts.json", "r", encoding="utf-8") as f:
        batch_data = json.load(f)
    
    total = len(batch_data["prompts"])
    success_count = 0
    
    for i, prompt_entry in enumerate(batch_data["prompts"], 1):
        print(f"Processing {i}/{total}: {prompt_entry['id']}")
        
        if generate_image(prompt_entry["prompt"], prompt_entry["filename"]):
            success_count += 1
    
    print(f"\nCompleted: {success_count}/{total} images generated")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Stable Diffusion API Batch Generation
Requires: pip install requests pillow
"""

import json
import requests
import base64
from pathlib import Path
from PIL import Image
import io

# Configuration
API_URL = "http://127.0.0.1:7860"  # Default Automatic1111 WebUI
OUTPUT_DIR = Path("generated_art/stable_diffusion")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def generate_image(prompt, filename):
    """Generate image using Stable Diffusion API"""
    payload = {
        "prompt": prompt,
        "negative_prompt": "color, colored, rainbow, bright colors, saturated, vibrant",
        "width": 512,
        "height": 512,
        "steps": 20,
        "cfg_scale": 7,
        "sampler_name": "DPM++ 2M Karras",
        "batch_size": 1,
        "n_iter": 1,
        "seed": -1,
        "restore_faces": False,
        "tiling": False,
        "do_not_save_samples": False,
        "do_not_save_grid": False
    }
    
    try:
        response = requests.post(f"{API_URL}/sdapi/v1/txt2img", json=payload)
        response.raise_for_status()
        
        result = response.json()
        if 'images' in result and result['images']:
            # Decode base64 image
            image_data = base64.b64decode(result['images'][0])
            image = Image.open(io.BytesIO(image_data))
            
            # Save image
            output_path = OUTPUT_DIR / filename
            image.save(output_path, "PNG")
            print(f"Generated: {filename}")
            return True
        else:
            print(f"No image generated for {filename}")
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

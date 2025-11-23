import os
import zipfile
from pathlib import Path
import google.generativeai as genai
from PIL import Image
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env file")
genai.configure(api_key=GOOGLE_API_KEY)

# Set up paths
input_dir = Path("/workspaces/colab_test/pictures/input")
output_dir = Path("/workspaces/colab_test/pictures/output")
output_dir.mkdir(parents=True, exist_ok=True)

# Initialize Gemini model
model = genai.GenerativeModel('gemini-2.5-flash')

print("✅ Setup complete!")
print(f"Input directory: {input_dir}")
print(f"Output directory: {output_dir}")

def generate_caption(image_path):
    """Generate a caption for an image using Gemini Vision API."""
    try:
        img = Image.open(image_path)
        
        prompt = """Analyze this image of livapetersen and create a concise, structured caption for LoRA training.

Format the caption like these examples (but describe what you ACTUALLY see in THIS image):
"livapetersen, long blonde wavy hair, blue eyes, freckles, soft makeup, wearing tight white off-shoulder top, indoors, natural light"
"livapetersen, blonde ponytail, blue eyes, freckles, natural makeup, wearing shiny metallic blue swimsuit, sitting on chair, purple background lighting"
"livapetersen, long blonde hair, blue eyes, freckles, rosy cheeks, wearing red bodysuit, indoors, purple background"

STRUCTURE (describe what you see, maintaining consistency):
1. Start with "livapetersen" followed by a comma
2. Hair description (style, color, length - be accurate to what you see)
3. Eye color (if visible)
4. Facial features (freckles, makeup, expression)
5. Clothing with "wearing" (be specific)
6. Pose or position if notable
7. Setting/location and lighting

RULES:
- Use SHORT comma-separated phrases, NO full sentences
- Be consistent with the person's features across all images
- Keep it under 25 words after "livapetersen,"
- Describe what you ACTUALLY see in the image

Create the caption for this image:"""
        
        response = model.generate_content([prompt, img])
        caption = response.text.strip()
        
        # Clean up the caption
        caption = caption.replace('"', '').replace("'", '')
        
        # Ensure caption starts with "livapetersen"
        if not caption.lower().startswith("livapetersen"):
            caption = f"livapetersen, {caption}"
        
        return caption
    
    except Exception as e:
        print(f"Error processing {image_path}: {str(e)}")
        return None

print("✅ Caption generation function ready!")

# Process all images and generate captions
image_files = sorted([f for f in input_dir.glob("*.jpeg") if f.is_file()])
print(f"\nFound {len(image_files)} images to process\n")

processed_files = []

for idx, image_path in enumerate(image_files, 1):
    print(f"Processing {idx}/{len(image_files)}: {image_path.name}")
    
    # Generate caption
    caption = generate_caption(image_path)
    
    if caption:
        # Create matching .txt file with same base name
        txt_filename = image_path.stem + ".txt"  # e.g., livapetersen_0001.txt
        txt_path = output_dir / txt_filename
        
        # Write caption to file
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(caption)
        
        processed_files.append(txt_path)
        print(f"✅ Created: {txt_filename}")
        print(f"   Caption: {caption[:80]}...")
    else:
        print(f"❌ Failed to process {image_path.name}")
    
    print()
    
    # Small delay to avoid rate limiting
    time.sleep(1)

print(f"\n✅ Processed {len(processed_files)}/{len(image_files)} images successfully!")

# Create a zip file with images and captions paired together
zip_path = Path("/workspaces/colab_test/livapetersen_training_data.zip")

print("\nCreating training data zip with images and captions...")
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for image_path in sorted(image_files):
        # Add the image
        zipf.write(image_path, image_path.name)
        print(f"Added: {image_path.name}")
        
        # Add matching caption file
        caption_path = output_dir / f"{image_path.stem}.txt"
        if caption_path.exists():
            zipf.write(caption_path, caption_path.name)
            print(f"Added: {caption_path.name}")
        else:
            print(f"⚠️  Warning: No caption found for {image_path.name}")

print(f"\n✅ Created training data zip: {zip_path}")
print(f"📦 Contains {len(image_files)} images and their captions")
print(f"\nYou can download it from: {zip_path}")

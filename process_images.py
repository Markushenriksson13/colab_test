import os
import zipfile
from pathlib import Path
import google.generativeai as genai
from PIL import Image
import time

# Configure Gemini API
GOOGLE_API_KEY = "AIzaSyC7G9LAbM4eXHv2xhdu3NGN_DacRFuSmlA"
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
        
        prompt = """Analyze this image and create a detailed caption for LoRA training. 
        Start the caption with "livapetersen" followed by a comma, then describe:
        - The person's appearance, pose, and expression
        - Clothing and styling details
        - Background and setting
        - Lighting and mood
        - Any notable features
        
        Format: livapetersen, [detailed description]
        Keep it concise but descriptive (1-2 sentences)."""
        
        response = model.generate_content([prompt, img])
        caption = response.text.strip()
        
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

# Create a zip file with all the caption files
zip_path = Path("/workspaces/colab_test/livapetersen_captions.zip")

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for txt_file in sorted(output_dir.glob("*.txt")):
        # Add file to zip with just the filename (no path)
        zipf.write(txt_file, txt_file.name)
        print(f"Added to zip: {txt_file.name}")

print(f"\n✅ Created zip file: {zip_path}")
print(f"📦 Zip contains {len(list(output_dir.glob('*.txt')))} caption files")
print(f"\nYou can download it from: {zip_path}")

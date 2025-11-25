import os
import shutil
from pathlib import Path
import google.generativeai as genai
from PIL import Image
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path="/workspaces/colab_test/.env")

# Configure Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env file")
genai.configure(api_key=GOOGLE_API_KEY)

# Set up paths
script_dir = Path(__file__).parent
input_dir = script_dir / "input"
output_dir = script_dir / "output"
output_dir.mkdir(parents=True, exist_ok=True)

# Initialize Gemini model
model = genai.GenerativeModel('gemini-2.5-flash')

print("✅ Setup complete!")
print(f"Input directory: {input_dir}")
print(f"Output directory: {output_dir}")

def generate_detailed_prompt(image_path, max_retries=3):
    """Generate a detailed text-to-image prompt for an image using Gemini Vision API."""
    for attempt in range(max_retries):
        try:
            img = Image.open(image_path)
        
            prompt = """Analyze this image and create a concise, hyper-realistic text-to-image prompt.

Write the prompt in this exact style - a flowing paragraph, descriptive but not overly long:

Example style (THIS LENGTH):
"A hyper-realistic selfie shot on an iPhone, close-up angle of a beautiful young woman lying down on a fuzzy surface outdoors. She has long dark brown hair, striking green eyes, and natural skin texture with light freckles on her nose. She is resting her head on her hand and looking directly at the camera. She is wearing a yellow and blue floral lace bikini top and silver hoop earrings. Bright natural sunlight, blue sky, green trees, and a modern white building structure in the background. High contrast, summer vibes, raw photo, unedited look."

Your description should include (keep it concise):
- Camera/shot type and angle (e.g., "selfie shot on an iPhone, close-up angle")
- Subject (beautiful young woman/man)
- Main pose/position
- Hair: color, length, basic style
- Eyes: color
- Key skin details (texture, freckles if prominent)
- Main facial expression and direction of gaze
- Clothing with key colors and style (be specific but brief)
- Notable accessories
- Setting and main background elements
- Lighting type
- Overall mood and photo quality (e.g., "raw photo, unedited look, summer vibes")

Keep it around 4-6 sentences. Be specific about colors and details but avoid excessive adjectives. Match the example length.

Create the prompt now:"""
        
            response = model.generate_content([prompt, img])
            description = response.text.strip()
        
            # Clean up the description
            description = description.replace('"', '').replace("'", '')
        
            return description
        
        except Exception as e:
            if "429" in str(e) or "quota" in str(e).lower():
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 15  # 15, 30, 45 seconds
                    print(f"⚠️  Rate limit hit. Waiting {wait_time} seconds before retry {attempt + 2}/{max_retries}...")
                    time.sleep(wait_time)
                    continue
            print(f"Error processing {image_path}: {str(e)}")
            return None
    
    return None

print("✅ Prompt generation function ready!")

# Process all images
image_extensions = ['.jpeg', '.jpg', '.png', '.webp']
image_files = sorted([f for f in input_dir.iterdir() 
                     if f.is_file() and f.suffix.lower() in image_extensions])

print(f"\nFound {len(image_files)} images to process\n")

if not image_files:
    print("❌ No images found in input directory!")
    exit(1)

processed_count = 0

for idx, image_path in enumerate(image_files, 1):
    print(f"Processing {idx}/{len(image_files)}: {image_path.name}")
    
    # Generate detailed prompt
    description = generate_detailed_prompt(image_path)
    
    if description:
        # Copy image with new name
        new_image_name = f"image_{idx}{image_path.suffix}"
        new_image_path = output_dir / new_image_name
        shutil.copy2(image_path, new_image_path)
        
        # Create matching .txt file
        txt_filename = f"image_{idx}.txt"
        txt_path = output_dir / txt_filename
        
        # Write description to file
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(description)
        
        processed_count += 1
        print(f"✅ Created: {new_image_name}")
        print(f"✅ Created: {txt_filename}")
        print(f"   Prompt preview: {description[:100]}...")
    else:
        print(f"❌ Failed to process {image_path.name}")
    
    print()
    
    # Longer delay to avoid rate limiting (free tier has strict limits)
    time.sleep(3)

print(f"\n✅ Processed {processed_count}/{len(image_files)} images successfully!")
print(f"📁 Output saved to: {output_dir}")

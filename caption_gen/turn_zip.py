import zipfile
from pathlib import Path
from datetime import datetime

# Set up paths
script_dir = Path(__file__).parent
output_dir = script_dir / "output"
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
zip_path = script_dir / f"training_data_{timestamp}.zip"

print("Creating training data zip file...")
print(f"Source directory: {output_dir}")
print()

# Get all files from output directory
all_files = sorted(output_dir.iterdir())
image_files = [f for f in all_files if f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp']]
text_files = [f for f in all_files if f.suffix == '.txt']

if not image_files:
    print("❌ No images found in output directory!")
    exit(1)

print(f"Found {len(image_files)} images and {len(text_files)} text files")
print()

# Create zip file with images and captions paired together
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    # Process files in pairs (image_1.jpg + image_1.txt, etc.)
    for i in range(1, len(image_files) + 1):
        # Find matching image and text files
        image_file = None
        text_file = None
        
        for img in image_files:
            if img.stem == f"image_{i}":
                image_file = img
                break
        
        for txt in text_files:
            if txt.stem == f"image_{i}":
                text_file = txt
                break
        
        # Add image if found
        if image_file:
            zipf.write(image_file, image_file.name)
            print(f"Added: {image_file.name}")
        
        # Add matching text file if found
        if text_file:
            zipf.write(text_file, text_file.name)
            print(f"Added: {text_file.name}")
        
        if not image_file and not text_file:
            break

print(f"\n✅ Created training data zip: {zip_path.name}")
print(f"📦 Contains {len(image_files)} images and {len(text_files)} text files")
print(f"📁 Location: {zip_path}")
print(f"\nYou can download it by right-clicking the file in the Explorer!")

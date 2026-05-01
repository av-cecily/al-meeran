import os
import re

frontend_dir = r'C:\Users\Administrator\Desktop\al-meeran\frontend'

def update_paths(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update scripts: src="js/..." -> src="static/js/..."
    # Only if it doesn't already have static/ or http
    content = re.sub(r'src="(?!(static/|http|https|/))([^"]*\.js)"', r'src="static/\2"', content)
    
    # Update links: href="css/..." -> href="static/css/..."
    content = re.sub(r'href="(?!(static/|http|https|/))([^"]*\.css)"', r'href="static/\2"', content)

    # Update images: src="assets/..." -> src="static/assets/..."
    content = re.sub(r'src="(?!(static/|http|https|/))([^"]*\.(jpg|jpeg|png|gif|webp|svg))"', r'src="static/\2"', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

# Walk through frontend directory
for root, dirs, files in os.walk(frontend_dir):
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            print(f"Updating {file_path}")
            update_paths(file_path)

print("Done.")

import os
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# Movie data (same as your list)
movies_data = [
    {"id": 1, "title": "Space Journey", "poster_url": "https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?auto=format&fit=crop&w=800&q=80"},
    {"id": 2, "title": "Romance in Rome", "poster_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=800&q=80"},
    {"id": 3, "title": "AI Uprising", "poster_url": "https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?auto=format&fit=crop&w=800&q=80"},
    {"id": 4, "title": "Comedy Campus", "poster_url": "https://images.unsplash.com/photo-1497034825429-c343d7c6a68f?auto=format&fit=crop&w=800&q=80"},
    {"id": 5, "title": "Lost in Time", "poster_url": "https://images.unsplash.com/photo-1478720568477-152d9b164e26?auto=format&fit=crop&w=800&q=80"},
    {"id": 6, "title": "Family Ties", "poster_url": "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?auto=format&fit=crop&w=800&q=80"},
    {"id": 7, "title": "Stand-Up Night", "poster_url": "https://images.unsplash.com/photo-1534410531701-5f9f5d3a5fcb?auto=format&fit=crop&w=800&q=80"},
    {"id": 8, "title": "Heist High", "poster_url": "https://images.unsplash.com/photo-1524985069026-dd778a71c7b4?auto=format&fit=crop&w=800&q=80"},
    {"id": 9, "title": "Quiet River", "poster_url": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=800&q=80"},
    {"id": 10, "title": "Midnight Runner", "poster_url": "https://images.unsplash.com/photo-1502877338535-766e1452684a?auto=format&fit=crop&w=800&q=80"},
]

# Create folder
os.makedirs("posters", exist_ok=True)

# Download posters
for movie in movies_data:
    title = movie["title"].replace(" ", "_")
    filename = f"posters/{title}.jpg"
    try:
        print(f"Downloading {movie['title']}...")
        response = requests.get(movie["poster_url"], timeout=10)
        image = Image.open(BytesIO(response.content))
        image.save(filename)
    except Exception as e:
        print(f"Failed to download {movie['title']}: {e}")

# Create default poster (Netflix-style)
width, height = 800, 1200
gradient = Image.new("RGB", (width, height), color="#141414")
draw = ImageDraw.Draw(gradient)

# Dark red gradient
for y in range(height):
    r = int(20 + (100 * y / height))
    g = int(0 + (10 * y / height))
    b = int(0 + (10 * y / height))
    draw.line([(0, y), (width, y)], fill=(r, g, b))

# Add "No Poster Available" text
try:
    font = ImageFont.truetype("arial.ttf", 48)
except:
    font = ImageFont.load_default()

text = "No Poster Available"
text_width, text_height = draw.textsize(text, font=font)
draw.text(((width - text_width) / 2, (height - text_height) / 2),
          text, font=font, fill=(255, 255, 255))

gradient.save("posters/default_poster.jpg")
print("\n✅ All posters downloaded successfully!")
print("🖼️ Default poster created at posters/default_poster.jpg")

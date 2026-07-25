import os
import requests

ASSETS_DIR = "assets/pieces"

# Using standard Wikipedia chess pieces (SVG converted to PNG for pygame ease)
# I'll use a github repo that hosts these standard images as pngs.
PIECES = ["wp", "wr", "wn", "wb", "wq", "wk", "bp", "br", "bn", "bb", "bq", "bk"]
BASE_URL = "https://raw.githubusercontent.com/lichess-org/lila/master/public/piece/cburnett/{}.svg"
# Pygame CE can load SVG directly if we have the right build, but let's see. 
# Oh wait, pygame-ce supports SVG loading out of the box in recent versions!
# If it doesn't work, we can fallback to drawing circles.

def fetch_pieces():
    if not os.path.exists(ASSETS_DIR):
        os.makedirs(ASSETS_DIR)
        
    for piece in PIECES:
        # Lichess piece names mapping: wp -> wP, wk -> wK (color lowercase, piece uppercase)
        color = piece[0]
        p_type = piece[1].upper()
        lichess_name = f"{color}{p_type}"
        url = BASE_URL.format(lichess_name)
        
        filepath = os.path.join(ASSETS_DIR, f"{piece}.svg")
        if not os.path.exists(filepath):
            print(f"Downloading {piece}...")
            response = requests.get(url)
            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    f.write(response.content)
            else:
                print(f"Failed to download {piece}")
                
    print("Done fetching assets.")

if __name__ == "__main__":
    fetch_pieces()

import os
import requests

themes = ["cburnett", "california", "spatial", "fantasy"]
pieces = ["wK", "wQ", "wR", "wB", "wN", "wP", "bK", "bQ", "bR", "bB", "bN", "bP"]

for theme in themes:
    os.makedirs(f"assets/{theme}", exist_ok=True)
    for piece in pieces:
        url = f"https://raw.githubusercontent.com/lichess-org/lila/master/public/piece/{theme}/{piece}.svg"
        path = f"assets/{theme}/{piece}.svg"
        if not os.path.exists(path):
            print(f"Downloading {theme}/{piece}.svg")
            try:
                r = requests.get(url)
                if r.status_code == 200:
                    with open(path, "wb") as f:
                        f.write(r.content)
                else:
                    print(f"Failed to fetch {url} (Code: {r.status_code})")
            except Exception as e:
                print(f"Error {theme}/{piece}: {e}")
print("Done!")

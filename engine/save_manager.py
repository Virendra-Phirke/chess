import json
import os

SAVE_FILE = "saves/save.json"

def save_game(move_log):
    if not os.path.exists("saves"):
        os.makedirs("saves")
        
    move_ids = [m.move_id for m in move_log]
    
    with open(SAVE_FILE, "w") as f:
        json.dump({"moves": move_ids}, f)
        
def load_game():
    if not os.path.exists(SAVE_FILE):
        return None
    with open(SAVE_FILE, "r") as f:
        data = json.load(f)
        return data.get("moves", [])

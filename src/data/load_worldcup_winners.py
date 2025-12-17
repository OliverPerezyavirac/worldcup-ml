import pandas as pd
from src.data.normalize_teams import normalize_country
from src.data.load_json import load_json

def load_worldcup_winners():
    data = load_json("data/raw/worldcupcham/champworldcup.json")

    rows = []

    for item in data:
        rows.append({
            "country": normalize_country(item["country"]),
            "year": item["year"],
            "target": item["target"]
        })
    
    return pd.DataFrame(rows)
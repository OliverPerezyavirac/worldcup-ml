import pandas as pd
from src.data.load_json import load_json
from src.data.normalize_teams import normalize_country

# Functions to load qualifiers from different confederations
def load_conmebol():
    data = load_json("data/raw/clasification/conmebolqualifiers.json")
    df = pd.DataFrame(data)
    df["country"] = df["pais"].apply(normalize_country)

    return df[[
        "country","posicion","pts", "dg"
    ]].assign(confederation="CONMEBOL")

def load_uefa():
    data = load_json("data/raw/clasification/uefaqualifiers.json")
    
    rows = []
    for group in data.values():
        for team in group:
            rows.append({
                "country": normalize_country(team["pais"]),
                "posicion": team["posicion"],
                "pts": team["pts"],
                "dg": team["dg"],
                "confederation": "UEFA"
            })
    return pd.DataFrame(rows)

def load_concacaf():
    data = load_json("data/raw/clasification/concacafqualifiers.json")
    
    rows = []
    for group in data.values():
        for team in group:
            rows.append({
                "country": normalize_country(team["pais"]),
                "posicion": team["posicion"],
                "pts": team["pts"],
                "dg": team["dg"],
                "confederation": "CONCACAF"
            })

    return pd.DataFrame(rows)

def load_caf():
    data = load_json("data/raw/clasification/cafqualifiers.json")
    
    rows = []
    for group in data.values():
        for team in group:
            rows.append({
                "country": normalize_country(team["pais"]),
                "posicion": team["posicion"],
                "pts": team["pts"],
                "dg": team["dg"],
                "confederation": "CAF"
            })
    return pd.DataFrame(rows)

def load_afc():
    data = load_json("data/raw/clasification/afcqualifiers.json")
    
    rows = []
    for group in data.values():
        for team in group:
            rows.append({
                "country": normalize_country(team["pais"]),
                "posicion": team["posicion"],
                "pts": team["pts"],
                "dg": team["dg"],
                "confederation": "AFC"
            })
    return pd.DataFrame(rows)

# Consolidated function to load all qualifiers
def load_all_qualifiers():
    dfs = [
        load_conmebol(),
        load_uefa(),
        load_concacaf(),
        load_caf(),
        load_afc()
    ]

    df = pd.concat(dfs, ignore_index=True)

    return df.rename( columns = {
        "posicion": "qualifier_Position",
        "pts": "qualifier_Points",
        "dg": "qualifier_Goal_Difference"
    })
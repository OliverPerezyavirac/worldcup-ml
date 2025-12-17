import re
from collections import defaultdict
from src.data.load_json import load_json
from src.data.normalize_teams import normalize_country
import pandas as pd

def parse_score(result: str):
    match = re.match(r"(\d+)-(\d+)", result)
    if not match:
        return None, None, None
    
    g1, g2 = int(match.group(1)), int(match.group(2))

    penalties = re.search(r"\((\d+)-(\d+) penales\)", result)
    pen_winner = None
    if penalties:
        p1, p2 = int(penalties.group(1)), int(penalties.group(2))
        pen_winner = 1 if p1 > p2 else 2

    return g1, g2, pen_winner

def compute_worldcup_stats():
    matches = load_json("data/raw/worldcup/worldcup2022.json")

    stats = defaultdict(lambda: {
        "matches": 0,
        "goals_for": 0,
        "goals_against": 0,
        "finals": 0,
        "titles": 0
    })

    for m in matches:

        home = normalize_country(m["local"])
        away = normalize_country(m["visitante"])
        g_home, g_away, pen_winner = parse_score(m["resultado"])

        if g_home is None:
            continue

        stats[home]["matches"] += 1
        stats[away]["matches"] += 1

        stats[home]["goals_for"] += g_home
        stats[home]["goals_against"] += g_away

        stats[away]["goals_for"] += g_away
        stats[away]["goals_against"] += g_home

        if m["ronda"] == "Final":
            stats[home]["finals"] += 1
            stats[away]["finals"] += 1

            if g_home > g_away or pen_winner == 1:
                stats[home]["titles"] += 1
            elif g_away > g_home or pen_winner == 2:
                stats[away]["titles"] += 1

    return stats

def worldcup_stats_df():
    stats = compute_worldcup_stats()
    df = pd.DataFrame.from_dict(stats, orient="index").reset_index()
    df.rename(columns={"index": "country"}, inplace=True)

    df["goals_avg"] = df["goals_for"] / df["matches"]
    return df

import pandas as pd
from src.data.load_json import load_json
from src.data.normalize_teams import normalize_country
from src.features.worldcup_stats import worldcup_stats_df
from src.features.qualifiers import load_all_qualifiers

# Fifa rankings
ranking = load_json("data/raw/fifaranking/fifaranking.json")
df_ranking = pd.DataFrame(ranking)
df_ranking["country"] = df_ranking["pais"].apply(normalize_country)

df_ranking = df_ranking[[
    "country", "posicion", "puntos", "variacion"    
]].rename(columns={
    "posicion": "fifa_rank",
    "puntos": "fifa_points",
    "variacion": "fifa_variation"
})

# World Cup Hosts
hosts = load_json("data/raw/worldcuphosts/worldcuphosts.json")
df_hosts = pd.DataFrame(hosts)
df_hosts["country"] = df_hosts["pais"].apply(normalize_country)
df_hosts["is_host"] = 1

df_hosts = df_hosts[[
    "country", "is_host" ]]

# Qualifiers
df_qualifiers = load_all_qualifiers()

df = df_ranking.merge(df_hosts, on="country", how="left")
df = df.merge(df_qualifiers, on="country", how="left")

df = df.merge(
    df_qualifiers,
    on="country",
    how="left"
)

df.fillna({
    "qualifier_Points": 0,
    "qualifier_Position": 0,
    "qualifier_Goal_Difference": 0,
    "confederation": "UNKNOWN"
}, inplace=True)

df = df.drop(columns=[
    "conmebol_points",
    "conmebol_goal_difference"
], errors='ignore')

print(df.head())
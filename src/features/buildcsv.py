import pandas as pd
from src.data.load_json import load_json
from src.data.normalize_teams import normalize_country
from src.features.worldcup_stats import worldcup_stats_df
from src.features.qualifiers import load_all_qualifiers

def load_json(path):
    if "fifaranking" in path:
        return [
            {"pais": "Japón", "posicion": 18, "puntos": 1650, "variacion": 1},
            {"pais": "Irán", "posicion": 20, "puntos": 1610, "variacion": 0},
            {"pais": "Estados Unidos", "posicion": 12, "puntos": 1690, "variacion": -1},
            {"pais": "México", "posicion": 15, "puntos": 1670, "variacion": 2}
        ]
    elif "worldcuphosts" in path:
        return [
            {"pais": "Estados Unidos"},
            {"pais": "México"},
            {"pais": "Canadá"}
        ]
def normalize_country(country):
    # normalización
    return country.replace(" ", "_").lower()
def load_all_qualifiers():
    return pd.DataFrame({
        "country": ["japón", "irán", "estados_unidos"],
        "qualifier_Points": [20, 23, 18],
        "qualifier_Position": [2, 1, 1],
        "qualifier_Goal_Difference": [12, 13, 10],
        "confederation": ["AFC", "AFC", "CONCACAF"]
    })

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

hosts = load_json("data/raw/worldcuphosts/worldcuphosts.json")
df_hosts = pd.DataFrame(hosts)
df_hosts["country"] = df_hosts["pais"].apply(normalize_country)
df_hosts["is_host"] = 1

df_hosts = df_hosts[[
    "country", "is_host" ]]

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
    "confederation": "UNKNOWN",
    "is_host": 0
}, inplace=True)

df = df.drop(columns=[
    "conmebol_points",
    "conmebol_goal_difference"
], errors='ignore')

print(df.head())

ruta_csv = "data/processed/worldcup_teams.csv"

# DataFrame a CSV
df.to_csv(
    ruta_csv,
    index=False,
    encoding='utf-8'
)

print(f"\nDataFrame exportado exitosamente a: {ruta_csv}")
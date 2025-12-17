import pandas as pd
import os
from src.data.load_json import load_json
from src.data.normalize_teams import normalize_country
from src.features.worldcup_stats import worldcup_stats_df
from src.features.qualifiers import load_all_qualifiers
from src.data.load_worldcup_winners import load_worldcup_winners

#FIFA Rankings
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

#Qualifiers
df_qualifiers = load_all_qualifiers()
df = df_ranking.merge(df_qualifiers, on="country", how="left")

df.fillna({
    "qualifier_Points": 0,
    "qualifier_Position": 0,
    "qualifier_Goal_Difference": 0,
    "confederation": "UNKNOWN"
}, inplace=True)

HOST_CONFEDERATION_MAP = {
    "eeuu": "CONCACAF",
    "canada": "CONCACAF",
    "mexico": "CONCACAF",
}

df['confederation'] = df.apply(
    lambda row: HOST_CONFEDERATION_MAP.get(row['country'].lower(), row['confederation']),
    axis=1
)

def expand_by_year(df, years):
    dfs = []
    for year in years:
        df_year = df.copy()
        df_year["year"] = year
        dfs.append(df_year)
    return pd.concat(dfs, ignore_index=True)

years = [year for year in range(1930, 2027, 4) if year not in [1942, 1946]]
df = expand_by_year(df, years)

hosts_historical = load_json("data/raw/worldcuphosts/worldcuphosts.json")
df_hosts = pd.DataFrame(hosts_historical)
df_hosts["country"] = df_hosts["country"].apply(normalize_country)
df_hosts["is_host"] = 1

hosts_2026 = load_json("data/raw/worldcuphosts/worldcuphosts2026.json")
for host in hosts_2026:
    country_normali = normalize_country(host["pais"])
    df_hosts = pd.concat([
        df_hosts,
        pd.DataFrame([{
            "year": 2026,
            "country": country_normali,
            "is_host": 1
        }])
    ], ignore_index=True)

df_hosts["year"] = df_hosts["year"].astype(int)
df["year"] = df["year"].astype(int)

df = df.merge(
    df_hosts[["country", "year", "is_host"]],
    on = ["country", "year"],
    how = "left"
)

df["is_host"] = df["is_host"].fillna(0).astype(int)
df["auto_qualify"] = df["is_host"]

winners = load_worldcup_winners()

df = df.merge(
    winners[["country", "year", "target"]],
    on=["country", "year"],
    how="left"
)

df["target"] = df["target"].fillna(0).astype(int)
df["is_champion"] = df["target"]


output_path = "data/processed/worldcup_dataset.csv"

output_dir = os.path.dirname(output_path)
if output_dir and not os.path.exists(output_dir):
    os.makedirs(output_dir, exist_ok=True)

df.to_csv(output_path, index=False, encoding='utf-8')

print("-" * 30)
print(f"PROCESO FINALIZADO")
print(f"Archivo guardado en: {output_path}")
print(f"Dimensiones del dataset: {df.shape}")
print("-" * 30)
print(df.head())
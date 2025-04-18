# Batuhan Baydar 32165 - DSA210
import pandas as pd, pathlib, json, time
from tqdm import tqdm
from helpers import tmdb_keywords

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW  = ROOT / "data" / "raw"
PROC = ROOT / "data" / "processed"
RAW.mkdir(parents=True, exist_ok=True)
PROC.mkdir(parents=True, exist_ok=True)

### 6.1 Oscars core CSV #######################################################
osc_url = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-02-18/oscars.csv"
osc_path = RAW / "oscars.csv"
if not osc_path.exists():
    import requests, shutil
    r = requests.get(osc_url, stream=True, timeout=60)
    with open(osc_path, "wb") as f: shutil.copyfileobj(r.raw, f)

osc = (
    pd.read_csv(osc_path)
    .loc[lambda d: d["year_ceremony"] >= 1929]
    .assign(film=lambda d: d["film"].str.strip())
)

### 6.2 Bechdel JSON ##########################################################
bech_url = "https://bechdeltest.com/api/v1/getAllMovies"
bech_path = RAW / "bechdel.json"
if not bech_path.exists():
    import requests, json
    data = requests.get(bech_url, timeout=60).json()
    json.dump(data, open(bech_path, "w"))

bech = (
    pd.read_json(bech_path)
    .rename(columns={"title": "film", "rating": "bechdel_rating"})
    .assign(bechdel_pass=lambda d: d["bechdel_rating"] >= 3)
    .drop_duplicates(subset=["film"])
)[["film", "bechdel_pass"]]

### 6.3 TMDB keywords #########################################################
political_words = {
    "politics", "political", "civil rights", "revolution",
    "war", "activism", "racism", "feminism", "colonial"
}

rows = []
for _, row in tqdm(osc[["film", "year_ceremony"]].drop_duplicates().iterrows(),
                   total=len(osc["film"].unique())):
    kws = tmdb_keywords(row["film"], row["year_ceremony"])
    rows.append({
        "film": row["film"],
        "political_theme": bool(set(kws) & political_words)
    })
    time.sleep(0.25)   # gentle rate limit
tmdb_df = pd.DataFrame(rows)

### 6.4 Merge & save ##########################################################
df = (
    osc.merge(bech, on="film", how="left")
       .merge(tmdb_df, on="film", how="left")
)

df.to_parquet(PROC / "oscar_enriched.parquet", index=False)
print("✅ Saved", PROC / "oscar_enriched.parquet")


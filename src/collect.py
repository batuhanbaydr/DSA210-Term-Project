# Batuhan Baydar 32165 - DSA210
import pathlib, json, requests, pandas as pd, re, unicodedata
from helpers import tmdb_keywords_and_genres

ROOT   = pathlib.Path(__file__).resolve().parents[1]
RAW    = ROOT / "data" / "raw"
PROC   = ROOT / "data" / "processed"
RAW.mkdir(parents=True, exist_ok=True)
PROC.mkdir(parents=True, exist_ok=True)

# Kaggle
xl_path = RAW / "academy_awards.xlsx"
if not xl_path.exists():
    raise FileNotFoundError(
        f"{xl_path} not found. Download it from Kaggle and place here."
    )

osc = pd.read_excel(xl_path)
osc = (
    osc.assign(film=lambda d: d["film"].astype(str).str.strip(), winner=lambda d: d["winner"].astype(bool))
)

# Bechdel
bech_file = RAW / "bechdel.json"
if not bech_file.exists():
    url = "https://bechdeltest.com/api/v1/getAllMovies"
    json.dump(requests.get(url, timeout=60).json(), open(bech_file, "w"))

bech = pd.read_json(bech_file)
norm = lambda t: re.sub(r"\s+", " ", re.sub(r"[^A-Za-z0-9 ]+", " ", unicodedata.normalize("NFKD", str(t)))).strip().lower()

osc["title_key"]  = osc["film"].apply(norm)
bech["title_key"] = bech["title"].apply(norm)
bech["bechdel_pass"] = bech["rating"] >= 3
osc = osc.merge(bech[["title_key", "bechdel_pass"]], on="title_key", how="left")

# Political Theme

KEYWORD_HITS = {
    "politics", "political", "civil rights", "revolution", "activism", "racism", "equality", "feminism", "colonialism", "propaganda", "campaign", "trans", "transexual", "transgender", "black rights", "lgbt", "gay theme", "diversity", "inclusion", "social justice", "gender identity", "non-binary", "intersectionality", "patriarchy", "white privilege", "systemic racism", "queer", "pride", "gender equality", "minority rights", "social movement", "identity politics", "anti-racism", "gender studies", "cultural appropriation", "allyship", "microaggressions", "equity", "social change", "progressive", "woke", "social commentary", "rebellion"
}
GENHITS = {} # Decided not to do this because of irrelevant results

osc["political_theme"] = False
mask = osc["year_ceremony"] >= 2000
for idx, row in osc[mask].iterrows():
    kw, gen = tmdb_keywords_and_genres(row.film, int(row.year_ceremony))
    osc.at[idx, "political_theme"] = bool(set(kw) & KEYHITS or set(gen) & GENHITS)

out = PROC / "oscars_plus_bechdel_pol.parquet"
osc.to_parquet(out, index=False)
print("It's saved", out, "— rows:", len(osc))

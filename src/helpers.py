# Batuhan Baydar 32165 - DSA210
import os, requests, time
from dotenv import load_dotenv
load_dotenv()

TMDB_KEY = os.getenv("TMDB_API_KEY")
session = requests.Session()

def tmdb_keywords(title, year):
    """Return a list of keyword strings for the first TMDB hit."""
    q = session.get(
        "https://api.themoviedb.org/3/search/movie",
        params={"api_key": TMDB_KEY, "query": title, "year": year},
        timeout=30,
    ).json()
    if not q["results"]:
        return []
    movie_id = q["results"][0]["id"]
    kw = session.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}/keywords",
        params={"api_key": TMDB_KEY},
        timeout=30,
    ).json()
    return [k["name"].lower() for k in kw.get("keywords", [])]


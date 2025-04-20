# Batuhan Baydar 32165 - DSA210


#Small helper for talking to the TMDB API.
import os, requests, time, functools
from dotenv import load_dotenv

load_dotenv()                       
TMDB_KEY = os.getenv("TMDB_API_KEY", "")
_SESSION = requests.Session()

def tmdb_keywords_and_genres(title: str, year: int | None):

# Ask TMDB for keywords + genres of the first movie match.
#   Parameters
#   ----------
#   title : str   movie title
#   year  : int or None   release year (can be None to ignore)

#   Returns
#   -------
#   (list[str], list[str])   keywords, genres – both lower‑case

    if not TMDB_KEY or not title:
        return [], []  # key missing → we skip

     # find the movie id
    q = _SESSION.get("https://api.themoviedb.org/3/search/movie", params={"api_key": TMDB_KEY, "query": title, "year": year}, timeout=30,).json()

    if not q["results"]:
        return [], []

    movie_id = q["results"][0]["id"]

    # fetch keywords
    kw_json = _SESSION.get(f"https://api.themoviedb.org/3/movie/{movie_id}/keywords", params={"api_key": TMDB_KEY}, timeout=30,).json()

    # fetch genres
    meta_json = _SESSION.get(f"https://api.themoviedb.org/3/movie/{movie_id}",params={"api_key": TMDB_KEY, "append_to_response": "external_ids"},timeout=30,).json()

    # be polite – 10 calls / second max
    time.sleep(0.1)                 
    keywords = [k["name"].lower() for k in kw_json.get("keywords", [])]
    genres   = [g["name"].lower() for g in meta_json.get("genres", [])]

    return keywords, genres    

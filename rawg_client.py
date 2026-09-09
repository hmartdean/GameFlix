import streamlit as st
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load api key from local secrets file
API_KEY = st.secrets["RAWG_API_KEY"]
BASE_URL = "https://api.rawg.io/api"


def get_popular_games(page_size: int = 40):
    """Fetches a list of highly rated and popular games from the RAWG API."""
    api_key = API_KEY
    url = f"{BASE_URL}/games"
    params = {
        "key": api_key,
        "page_size": page_size,
        "ordering": "-metacritic"
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
    except Exception as e:
        st.error(f"Error loading games catalog: {e}")
        return []


def get_game_details(game_id):
    url_details = f"{BASE_URL}/games/{game_id}"
    res_details = requests.get(url_details, params={"key": API_KEY})
    if res_details.status_code != 200:
        return None

    data = res_details.json()

    # Fetch game trailer if available
    url_movies = f"{BASE_URL}/games/{game_id}/movies"
    res_movies = requests.get(url_movies, params={"key": API_KEY})
    trailer_url = None

    if res_movies.status_code == 200:
        movies = res_movies.json().get("results", [])
        if movies:
            trailer_url = movies[0].get("data", {}).get("max")

    return {
        "id": data.get("id"),
        "name": data.get("name"),
        "description": data.get("description_raw") or "Sin descripción disponible.",
        "genres": [g["name"] for g in data.get("genres", [])],
        "platforms": [p["platform"]["name"] for p in data.get("platforms", [])],
        "released": data.get("released", "Desconocida"),
        "rating": data.get("rating", 0.0),
        "metacritic": data.get("metacritic"),
        "image": data.get("background_image"),
        "trailer": trailer_url
    }

@st.cache_data(ttl=3600, show_spinner=False)
def search_game_by_name(game_name: str) -> dict | None:
    """Searches for a game by title in RAWG and caches the result."""
    url = f"{BASE_URL}/games"
    params = {
        "key": API_KEY,
        "search": game_name,
        "page_size": 1,
        "search_precise": True
    }
    try:
        response = requests.get(
            url,
            params=params,
            timeout=5
        )
        response.raise_for_status()
        results = response.json().get("results", [])

        if not results:
            return None
        game = results[0]
        return {
            "id": game.get("id"),
            "name": game.get("name"),
            "background_image": game.get("background_image"),
            "rating": game.get("rating", 0.0),
            "metacritic": game.get("metacritic")
        }
    except requests.RequestException:
        return None


def search_games_parallel(game_names: list[str]) -> list[dict]:
    """Search multiple games in RAWG concurrently."""

    if not game_names:
        return []

    results = []

    # Maximum 6 simultaneous RAWG requests
    max_workers = min(6, len(game_names))

    with ThreadPoolExecutor(max_workers=max_workers) as executor:

        future_to_title = {
            executor.submit(search_game_by_name, title): title
            for title in game_names
        }

        for future in as_completed(future_to_title):
            try:
                game = future.result()

                if game:
                    results.append(game)

            except Exception:
                continue

    # Restore Gemini's original recommendation order
    games_by_name = {
        game["name"].lower(): game
        for game in results
        if game.get("name")
    }

    ordered_results = []

    for title in game_names:
        title_lower = title.lower()

        if title_lower in games_by_name:
            ordered_results.append(games_by_name[title_lower])

    return ordered_results
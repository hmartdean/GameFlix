import streamlit as st
import requests

# Lee la clave de forma segura sin exponerla en el codigo
API_KEY = st.secrets["RAWG_API_KEY"]
BASE_URL = "https://api.rawg.io/api"


def get_popular_games(page_size=40):
    """Devuelve los juegos mas valorados."""
    url = f"{BASE_URL}/games"
    params = {
        "key": API_KEY,
        "page_size": page_size,
        "ordering": "-metacritic"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])
    print(f"Error al obtener populares: {response.status_code}")
    return []


def get_game_details(game_id):
    """Devuelve detalles, generos y trailer de un juego."""
    url_details = f"{BASE_URL}/games/{game_id}"
    res_details = requests.get(url_details, params={"key": API_KEY})
    if res_details.status_code != 200:
        return None

    data = res_details.json()

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
        "released": data.get("released"),
        "rating": data.get("rating"),
        "trailer": trailer_url
    }
import base64
import streamlit as st
import rawg_client

st.set_page_config(
    page_title="GameFlix",
    page_icon="🎮",
    layout="wide"
)

# Cargar imagen local y pasarla a base64 para que el navegador la lea
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        return None

fondo_b64 = get_base64_image("fondo.jpg")
fondo_css = f"url('data:image/jpeg;base64,{fondo_b64}')" if fondo_b64 else "none"

# Estilos visuales
st.markdown(f"""
<style>
    .stApp {{
        background-color: #111215;
        background-image: 
            linear-gradient(
                to bottom,
                rgba(17, 18, 21, 0.80) 0%,
                rgba(17, 18, 21, 0.92) 50%,
                rgba(17, 18, 21, 0.98) 100%
            ),
            {fondo_css};
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: #ffffff;
    }}

    /* Animacion para las caratulas */
    div[data-testid="stImage"] img {{
        border-radius: 8px;
        transition: transform 0.25s ease, filter 0.25s ease, box-shadow 0.25s ease;
        cursor: pointer;
    }}

    div[data-testid="stImage"] img:hover {{
        transform: scale(0.96);
        filter: brightness(1.12);
        box-shadow: 0 4px 15px rgba(229, 9, 20, 0.35);
    }}

    div[data-testid="stImage"] img:active {{
        transform: scale(0.93);
    }}

    .score-badge {{
        background-color: #e50914;
        color: white;
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: bold;
        font-size: 0.85rem;
    }}

    /* Boton rojo */
    div.stButton > button {{
        background-color: #e50914;
        color: white;
        border: none;
        border-radius: 4px;
        font-weight: bold;
        width: 100%;
        margin-top: 5px;
        transition: transform 0.15s ease, background-color 0.15s ease;
    }}

    div.stButton > button:hover {{
        background-color: #b80710;
        color: white;
        transform: scale(0.98);
    }}
</style>
""", unsafe_allow_html=True)

# Guardar en cache 1 hora para no saturar la API
@st.cache_data(ttl=3600)
def cargar_catalogo():
    return rawg_client.get_popular_games(page_size=40)

# Header
st.markdown("<h1 style='color: #e50914; margin-bottom: 0;'>GAMEFLIX</h1>", unsafe_allow_html=True)
st.caption("Catálogo de los 40 títulos mejor valorados en la historia")

juegos = cargar_catalogo()

# Imagen por defecto por si algun juego viene sin foto
IMAGEN_DEFAULT = "https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=600&q=80"

# Grid de 4 columnas
if juegos:
    cols = st.columns(4)
    for index, juego in enumerate(juegos):
        col_actual = cols[index % 4]
        with col_actual:
            img_url = juego.get("background_image") or IMAGEN_DEFAULT
            st.image(img_url, width="stretch")

            nombre = juego.get("name", "Desconocido")
            rating = juego.get("rating", 0.0)
            st.markdown(f"**{nombre}**")
            st.markdown(f"<span class='score-badge'>★ {rating} / 5</span>", unsafe_allow_html=True)

            st.button("Ver detalles", key=f"btn_{juego['id']}")
            st.write("")
else:
    st.warning("No se pudieron cargar los juegos. Revisa la conexion o la API Key.")
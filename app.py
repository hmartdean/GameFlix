import streamlit as st
import rawg_client

st.set_page_config(
    page_title="GameFlix",
    page_icon="🎮",
    layout="wide"
)

# Lightweight Netflix dark theme
st.markdown("""
<style>
    .stApp {
        background-color: #111215;
        color: #ffffff;
    }

    div[data-testid="stImage"] img {
        border-radius: 8px;
        transition: transform 0.25s ease;
    }

    div[data-testid="stImage"] img:hover {
        transform: scale(0.97);
    }

    .score-badge {
        background-color: #e50914;
        color: white;
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: bold;
        font-size: 0.85rem;
    }

    div.stButton > button {
        background-color: #e50914;
        color: white;
        border: none;
        border-radius: 4px;
        font-weight: bold;
        width: 100%;
        margin-top: 5px;
    }

    div.stButton > button:hover {
        background-color: #b80710;
        color: white;
    }
</style>
""", unsafe_allow_html=True)


# Cache catalog response for 1 hour
@st.cache_data(ttl=3600)
def cargar_catalogo():
    return rawg_client.get_popular_games(page_size=40)


# Wide detail modal dialog
@st.dialog("Detalles del juego", width="large")
def mostrar_modal_detalle(game_id):
    with st.spinner("Cargando ficha técnica..."):
        detalle = rawg_client.get_game_details(game_id)

    if not detalle:
        st.error("No se pudo cargar la información de este juego.")
        return

    # Video trailer fallback to banner image
    if detalle.get("trailer"):
        st.video(detalle["trailer"])
    elif detalle.get("image"):
        st.image(detalle["image"], use_container_width=True)

    st.markdown(f"<h2 style='color: #e50914; margin-top: 10px;'>{detalle['name']}</h2>", unsafe_allow_html=True)

    # Score and release metadata row
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.markdown(f"⭐ **Puntuación:** {detalle['rating']} / 5")
    with m_col2:
        meta = detalle.get("metacritic") or "N/A"
        st.markdown(f"🏆 **Metacritic:** <span class='score-badge'>{meta}</span>", unsafe_allow_html=True)
    with m_col3:
        st.markdown(f"📅 **Lanzamiento:** {detalle['released']}")

    st.divider()

    # Two-column layout: synopsis on left, technical specs on right
    c_desc, c_specs = st.columns([2, 1])
    with c_desc:
        st.markdown("**Sinopsis**")
        st.markdown(f"<div style='max-height: 250px; overflow-y: auto; line-height: 1.6; color: #f1f1f1; background-color: #1a1c22; padding: 12px; border-radius: 6px;'>{detalle['description']}</div>", unsafe_allow_html=True)

    with c_specs:
        st.markdown("**Géneros**")
        generos = detalle.get("genres", [])
        if generos:
            generos_html = " ".join([f"<span style='background-color: #e50914; color: #ffffff; padding: 3px 8px; border-radius: 4px; font-size: 0.8rem; margin: 3px; display: inline-block;'>{g}</span>" for g in generos])
            st.markdown(generos_html, unsafe_allow_html=True)
        else:
            st.caption("No especificado")

        st.markdown("<br>**Plataformas**", unsafe_allow_html=True)
        plataformas = detalle.get("platforms", [])
        st.caption(", ".join(plataformas[:6]) if plataformas else "No especificadas")


# App title and header
st.markdown("<h1 style='color: #e50914;'>GAMEFLIX</h1>", unsafe_allow_html=True)
st.caption("Catálogo de los 40 títulos mejor valorados")

juegos = cargar_catalogo()

IMAGEN_DEFAULT = "https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=600&q=80"

# Render responsive 4-column cards
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

            if st.button("Ver detalles", key=f"btn_{juego['id']}"):
                mostrar_modal_detalle(juego["id"])
            st.write("")
else:
    st.warning("No se pudieron cargar los juegos. Revisa que secrets.toml tenga RAWG_API_KEY correcta.")
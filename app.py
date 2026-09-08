import streamlit as st
import rawg_client
from rawg_client import search_game_by_name
from gemini_client import recommend_games_with_gemini

st.set_page_config(
    page_title="GameFlix",
    page_icon="🎮",
    layout="wide"
)

# Lightweight Netflix dark theme
st.markdown("""
<style>
    /* Global app container & readable font weights */
    .stApp {
        background-color: #111215;
        color: #ffffff;
        font-weight: 500;
        -webkit-font-smoothing: antialiased;
    }

    /* Make all general paragraphs, labels, and spans bolder and sharper */
    p, span, label, div {
        font-weight: 500;
    }

    /* Subtitles and captions */
    .stCaption, [data-testid="stCaptionContainer"] {
        color: #d1d5db !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }

    /* Card hover interactions */
    div[data-testid="stImage"] img {
        border-radius: 8px;
        transition: transform 0.25s ease;
    }

    div[data-testid="stImage"] img:hover {
        transform: scale(0.97);
    }

    /* Prominent score badge */
    .score-badge {
        background-color: #e50914;
        color: #ffffff;
        padding: 3px 9px;
        border-radius: 4px;
        font-weight: 700;
        font-size: 0.88rem;
        letter-spacing: 0.3px;
    }

    /* Netflix-themed red action buttons */
    div.stButton > button {
        background-color: #e50914;
        color: #ffffff;
        border: none;
        border-radius: 4px;
        font-weight: 700;
        font-size: 0.95rem;
        width: 100%;
        margin-top: 5px;
        letter-spacing: 0.4px;
    }

    div.stButton > button:hover {
        background-color: #b80710;
        color: #ffffff;
    }

    /* YouTube link button inside dialog */
    div[data-testid="stLinkButton"] a {
        background-color: #1e2025;
        color: #ff3b30 !important;
        border: 1.5px solid #e50914;
        border-radius: 6px;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        padding: 0.5rem 1.2rem;
        transition: all 0.2s ease-in-out;
        margin-top: 8px;
        margin-bottom: 8px;
    }

    div[data-testid="stLinkButton"] a:hover {
        background-color: #e50914;
        color: #ffffff !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 14px rgba(229, 9, 20, 0.45);
    }
</style>
""", unsafe_allow_html=True)


# Cache catalog response for 1 hour to reduce API requests
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

    # Video trailer fallback to banner image with styled YouTube link button
    if detalle.get("trailer"):
        st.video(detalle["trailer"])
    elif detalle.get("image"):
        st.image(detalle["image"], width="stretch")
        query_yt = f"{detalle['name']} official trailer".replace(" ", "+")
        st.link_button("▶  Ver tráiler oficial en YouTube", f"https://www.youtube.com/results?search_query={query_yt}")

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
        st.markdown(
            f"<div style='max-height: 250px; overflow-y: auto; line-height: 1.7; color: #ffffff; font-weight: 500; font-size: 0.95rem; background-color: #1a1c22; padding: 14px; border-radius: 6px; border: 1px solid #2d3139;'>{detalle['description']}</div>",
            unsafe_allow_html=True
        )
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

# Natural language AI search input
prompt_usuario = st.text_input(
    "🔍 ¿Qué te apetece jugar hoy?",
    placeholder="Ej: 'Juegos de detectives oscuros con estética retro' o 'Aventuras relajantes de granja'..."
)

IMAGEN_DEFAULT = "https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=600&q=80"

# Conditional data flow: AI recommendations vs popular default catalog
if prompt_usuario:
    with st.spinner("🤖 Gemini está analizando tu petición y buscando los mejores títulos..."):
        titulos_recomendados = recommend_games_with_gemini(prompt_usuario)

    if titulos_recomendados:
        st.caption(f"Recomendaciones inteligentes de Gemini ({len(titulos_recomendados)} títulos encontrados)")
        juegos_mostrar = []
        for titulo in titulos_recomendados:
            ficha = search_game_by_name(titulo)
            if ficha:
                juegos_mostrar.append(ficha)
    else:
        st.warning("No encontramos títulos que encajen exactamente con esa descripción. Prueba con otra.")
        juegos_mostrar = []
else:
    st.caption("Catálogo de los títulos más populares")
    juegos_mostrar = cargar_catalogo()

# Responsive 4-column game card grid
if juegos_mostrar:
    cols = st.columns(4)
    for index, juego in enumerate(juegos_mostrar):
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
    if not prompt_usuario:
        st.warning("No se pudieron cargar los juegos. Revisa que secrets.toml tenga RAWG_API_KEY correcta.")
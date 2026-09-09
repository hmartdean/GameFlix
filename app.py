import base64
import streamlit as st
import rawg_client
from gemini_client import recommend_games_with_gemini
from rawg_client import search_game_by_name

# Configure page layout and metadata
st.set_page_config(
    page_title="GameFlix",
    page_icon="🎮",
    layout="wide"
)

# Convert local image to base64 for background injection
def get_base64_image(image_path: str) -> str:
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

background_b64 = get_base64_image("fondo.jpg")

# Global UI styling
st.markdown(f"""
<style>

.stApp {{
    background:
        linear-gradient(
            rgba(15, 16, 20, 0.88),
            rgba(15, 16, 20, 0.95)
        ),
        url("data:image/jpeg;base64,{background_b64}")
        no-repeat center center fixed !important;

    background-size: cover !important;
    color: #ffffff;
    -webkit-font-smoothing: antialiased;
}}

header[data-testid="stHeader"],
.stMainBlockContainer {{
    background: transparent !important;
}}

.stCaption,
[data-testid="stCaptionContainer"] {{
    color: #d1d5db !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
}}

div[data-testid="stImage"] img {{
    border-radius: 8px;
    transition: transform 0.25s ease;
}}

div[data-testid="stImage"] img:hover {{
    transform: scale(0.97);
}}

.score-badge {{
    background-color: #e50914;
    color: #ffffff;
    padding: 3px 9px;
    border-radius: 4px;
    font-weight: 700;
    font-size: 0.88rem;
    letter-spacing: 0.3px;
}}

div.stButton > button {{
    background-color: #e50914;
    color: #ffffff;
    border: none;
    border-radius: 4px;
    font-weight: 700;
    font-size: 0.95rem;
    width: 100%;
    margin-top: 5px;
    letter-spacing: 0.4px;
    transition: all 0.2s ease;
}}

div.stButton > button:hover {{
    background-color: #b80710;
    color: #ffffff;
    transform: translateY(-1px);
    box-shadow: 0 4px 14px rgba(229, 9, 20, 0.35);
}}

div[data-testid="stLinkButton"] a {{
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
}}

div[data-testid="stLinkButton"] a:hover {{
    background-color: #e50914;
    color: #ffffff !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 14px rgba(229, 9, 20, 0.45);
}}

/* AI search status badge */
.gameflix-ai-status {{
    display: flex;
    align-items: center;
    gap: 8px;
    margin-top: 5px;
    margin-bottom: 7px;
    color: #737b89;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 1.2px;
    text-transform: uppercase;
}}

.gameflix-ai-dot {{
    width: 7px;
    height: 7px;
    background: #39ff88;
    border-radius: 50%;
    box-shadow: 0 0 7px rgba(57, 255, 136, 0.9);
    animation: gameflixPulse 1.8s infinite;
}}

@keyframes gameflixPulse {{
    0%, 100% {{
        opacity: 1;
        transform: scale(1);
    }}
    50% {{
        opacity: 0.35;
        transform: scale(0.75);
    }}
}}

/* Search input styling */
div[data-testid="stTextInput"] {{
    margin-top: 0px !important;
    margin-bottom: 0px !important;
}}

div[data-testid="stTextInput"] label {{
    color: #c7cbd3 !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    margin-bottom: 8px !important;
}}

div[data-testid="stTextInput"] > div,
div[data-testid="stTextInput"] div[data-baseweb="base-input"],
div[data-testid="stTextInput"] div[data-baseweb="input"] {{
    position: relative !important;
    background: rgba(14, 17, 23, 0.95) !important;
    border: 1px solid rgba(229, 9, 20, 0.45) !important;
    border-radius: 12px !important;
    box-shadow:
        0 0 0 1px rgba(255, 255, 255, 0.02),
        0 8px 30px rgba(0, 0, 0, 0.5),
        inset 0 0 15px rgba(0, 0, 0, 0.4) !important;
    transition: all 0.25s ease !important;
    overflow: hidden !important;
}}

div[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within {{
    border-color: #e50914 !important;
    box-shadow:
        0 0 0 1px rgba(229, 9, 20, 0.5),
        0 0 20px rgba(229, 9, 20, 0.35),
        0 8px 30px rgba(0, 0, 0, 0.6) !important;
    transform: translateY(-1px);
}}

div[data-testid="stTextInput"] input {{
    background: transparent !important;
    color: #111111 !important;
    -webkit-text-fill-color: #111111 !important;
    caret-color: #e50914 !important;
    border: none !important;
    outline: none !important;
    font-size: 0.98rem !important;
    font-weight: 600 !important;
    padding: 13px 18px 13px 44px !important;
}}

div[data-testid="stTextInput"] input:focus {{
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}}

div[data-testid="stTextInput"] input::placeholder {{
    color: #6b7280 !important;
    opacity: 1 !important;
}}

div[data-testid="stTextInput"] > div::before {{
    content: "✦";
    position: absolute;
    left: 16px;
    top: 50%;
    transform: translateY(-50%);
    color: #e50914;
    font-size: 1.1rem;
    font-weight: 900;
    text-shadow: 0 0 8px rgba(229, 9, 20, 0.8);
    z-index: 5;
    pointer-events: none;
}}

/* Red Netflix Form Submit Button */
div[data-testid="stFormSubmitButton"] {{
    margin-top: 28px !important;
}}

div[data-testid="stFormSubmitButton"] > button {{
    background: linear-gradient(135deg, #e50914 0%, #b80710 100%) !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    border: 1px solid #ff2a35 !important;
    border-radius: 12px !important;
    font-size: 0.95rem !important;
    font-weight: 800 !important;
    letter-spacing: 1px !important;
    padding: 12px 18px !important;
    box-shadow: 0 4px 18px rgba(229, 9, 20, 0.45) !important;
    transition: all 0.25s ease !important;
}}

div[data-testid="stFormSubmitButton"] > button:hover {{
    background: linear-gradient(135deg, #ff1a26 0%, #d40813 100%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 25px rgba(229, 9, 20, 0.65) !important;
}}

div[data-testid="stFormSubmitButton"] > button:active {{
    transform: translateY(0px) !important;
}}

</style>
""", unsafe_allow_html=True)

# Cache catalog response for 1 hour to reduce API requests
@st.cache_data(ttl=3600)
def load_popular_catalog():
    return rawg_client.get_popular_games(page_size=40)

# Wide detail modal dialog
@st.dialog("Game Details", width="large")
def show_detail_modal(game_id: int):
    with st.spinner("Loading game details..."):
        details = rawg_client.get_game_details(game_id)

    if not details:
        st.error("Could not load information for this game.")
        return

    # Video trailer fallback to banner image with styled YouTube link button
    if details.get("trailer"):
        st.video(details["trailer"])
    elif details.get("image"):
        st.image(details["image"], width="stretch")
        query_yt = f"{details['name']} official trailer".replace(" ", "+")
        st.link_button("▶  Watch official trailer on YouTube", f"https://www.youtube.com/results?search_query={query_yt}")

    st.markdown(f"<h2 style='color: #e50914; margin-top: 10px;'>{details['name']}</h2>", unsafe_allow_html=True)

    # Score and release metadata row
    col_rating, col_meta, col_release = st.columns(3)
    with col_rating:
        st.markdown(f"⭐ **Rating:** {details['rating']} / 5")
    with col_meta:
        meta_score = details.get("metacritic") or "N/A"
        st.markdown(f"🏆 **Metacritic:** <span class='score-badge'>{meta_score}</span>", unsafe_allow_html=True)
    with col_release:
        st.markdown(f"📅 **Released:** {details['released']}")

    st.divider()

    # Two-column layout: synopsis on left, technical specs on right
    col_synopsis, col_specs = st.columns([2, 1])
    with col_synopsis:
        st.markdown("**Synopsis**")
        st.markdown(
            f"<div style='max-height: 250px; overflow-y: auto; line-height: 1.7; color: #ffffff; font-weight: 500; font-size: 0.95rem; background-color: #1a1c22; padding: 14px; border-radius: 6px; border: 1px solid #2d3139;'>{details['description']}</div>",
            unsafe_allow_html=True
        )
    with col_specs:
        st.markdown("**Genres**")
        genres = details.get("genres", [])
        if genres:
            genres_html = " ".join([f"<span style='background-color: #e50914; color: #ffffff; padding: 3px 8px; border-radius: 4px; font-size: 0.8rem; margin: 3px; display: inline-block;'>{g}</span>" for g in genres])
            st.markdown(genres_html, unsafe_allow_html=True)
        else:
            st.caption("Not specified")

        st.markdown("<br>**Platforms**", unsafe_allow_html=True)
        platforms = details.get("platforms", [])
        st.caption(", ".join(platforms[:6]) if platforms else "Not specified")


# App title and header
st.markdown("<h1 style='color: #e50914;'>GAMEFLIX</h1>", unsafe_allow_html=True)

# Natural language AI search input
st.markdown("""
<div class="gameflix-ai-status">
    <span class="gameflix-ai-dot"></span>
    GAMEFLIX AI · ONLINE RECOMMENDATION SYSTEM
</div>
""", unsafe_allow_html=True)

with st.form("gameflix_search", clear_on_submit=False):
    col_search, col_button = st.columns([7, 1.15], gap="small")

    with col_search:
        user_prompt = st.text_input(
            "What would you like to play today?",
            placeholder="Describe your next adventure... "
                        "e.g. dark detectives, open world, "
                        "retro psychological horror",
            label_visibility="visible"
        )

    with col_button:
        submit_search = st.form_submit_button(
            "✦ EXPLORE",
            use_container_width=True
        )

DEFAULT_IMAGE_URL = "https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=600&q=80"

# Conditional data flow: AI recommendations vs popular default catalog
if submit_search and user_prompt.strip():
    with st.spinner("🤖 Gemini is analyzing your request and searching for the best titles..."):
        recommended_titles = recommend_games_with_gemini(
            user_prompt.strip()
        )

    if recommended_titles:
        st.caption(
            f"Intelligent recommendations from Gemini "
            f"({len(recommended_titles)} titles found)"
        )
        games_to_display = []

        for title in recommended_titles:
            game_card = search_game_by_name(title)
            if game_card:
                games_to_display.append(game_card)

    else:
        st.warning(
            "We could not find titles that closely match "
            "that description. Try another one."
        )
        games_to_display = []

else:
    st.caption("Most popular games catalog")
    games_to_display = load_popular_catalog()

# Responsive 4-column game card grid
if games_to_display:
    columns = st.columns(4)
    for index, game in enumerate(games_to_display):
        current_column = columns[index % 4]
        with current_column:
            image_url = game.get("background_image") or DEFAULT_IMAGE_URL
            st.image(image_url, width="stretch")

            game_name = game.get("name", "Unknown")
            rating = game.get("rating", 0.0)
            st.markdown(f"**{game_name}**")
            st.markdown(f"<span class='score-badge'>★ {rating} / 5</span>", unsafe_allow_html=True)

            if st.button("View details", key=f"btn_{game['id']}"):
                show_detail_modal(game["id"])
            st.write("")
else:
    if not user_prompt:
        st.warning("Could not load games. Please check that secrets.toml contains a valid RAWG_API_KEY.")
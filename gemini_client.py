import json
import streamlit as st
from google import genai
from google.genai import types


def get_gemini_client():
    """Initializes and returns the official Gemini client using the API key stored in Streamlit secrets."""
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .streamlit/secrets.toml")
    return genai.Client(api_key=api_key)


def recommend_games_with_gemini(user_prompt: str, min_count: int = 2, max_count: int = 8) -> list[str]:
    """Recommends between min_count and max_count game titles prioritizing relevance and accuracy."""
    try:
        client = get_gemini_client()

        system_instruction = (
            "You are an expert video game recommender for a Netflix-styled gaming platform. "
            "Your highest priority is RELEVANCE and ACCURACY over quantity. "
            f"Suggest between {min_count} and {max_count} real, existing video games "
            "that strictly match the user's request. "
            "If the topic is very specific or niche, return only the titles that genuinely fit "
            "(even if it is only 2 or 3). "
            "Under no circumstances should you invent titles or fill the list with unrelated games. "
            "Return only official international commercial titles so they can be accurately queried "
            "in an external database (RAWG API)."
        )

        prompt = f"User preference: '{user_prompt}'."

        # Enforce structured JSON output to guarantee a clean list of strings
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.3,  # Lower temperature to reduce hallucinations and ensure precision
                response_mime_type="application/json",
                response_schema={
                    "type": "ARRAY",
                    "items": {
                        "type": "STRING"
                    }
                }
            )
        )

        titles = json.loads(response.text)
        return titles if isinstance(titles, list) else []

    except Exception as e:
        st.error(f"Error querying Gemini API: {e}")
        return []
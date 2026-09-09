# 🎬 GameFlix — AI-Powered Video Game Discovery

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://gameflix.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modern, responsive video game recommendation platform featuring a Netflix-inspired UI. GameFlix leverages Google Gemini to interpret natural language gaming requests and combines it with RAWG's database for rich game metadata, ratings, and video trailers.

🌐 **Live Demo:** [https://gameflix.streamlit.app](https://gameflix.streamlit.app)

---

## ✨ Features

- **Natural Language Search:** Describe the kind of game or mood you want (e.g., *"dark detective psychological horror"* or *"chill open-world building"*), and Gemini delivers tailored recommendations.
- **Dynamic Catalog:** Displays top-rated video games ranked by Metacritic score by default.
- **Interactive Game Dialogs:** Detailed modal views containing game synopsis, release dates, platforms, Metacritic ratings, and embedded video trailers.
- **Netflix-Style Visual Design:** Custom CSS styling built on top of Streamlit with dark aesthetics, modern cards, and responsive grids.
- **Optimized Data Fetching:** Concurrent requests using `ThreadPoolExecutor` to retrieve metadata quickly without blocking the user interface.

---

## 🛠️ Tech Stack

- **Frontend / Framework:** [Streamlit](https://streamlit.io/)
- **Large Language Model:** [Google Gemini API](https://ai.google.dev/)
- **Game Data & Media:** [RAWG Video Games Database API](https://rawg.io/apidocs)
- **Networking & Concurrency:** `requests`, `concurrent.futures.ThreadPoolExecutor`
- **Styling:** Custom CSS injected via `st.markdown`

---

## 🚀 Getting Started Locally

### Prerequisites

- Python 3.10 or higher installed.
- API Key from [RAWG](https://rawg.io/apidocs).
- API Key from [Google AI Studio](https://aistudio.google.com/).

### Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/hmartdean/GameFlix.git](https://github.com/hmartdean/GameFlix.git)
   cd GameFlix
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # macOS / Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment credentials:**
   Copy the example configuration file:
   ```bash
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   ```
   Open `.streamlit/secrets.toml` and add your keys:
   ```toml
   RAWG_API_KEY = "your_actual_rawg_api_key"
   GEMINI_API_KEY = "your_actual_gemini_api_key"
   ```

5. **Run the application:**
   ```bash
   streamlit run app.py
   ```

---

## 🏛️ Project Architecture

```text
GameFlix/
├── .streamlit/
│   ├── secrets.toml.example   # Template for local development keys
│   └── config.toml            # Optional Streamlit theme configuration
├── app.py                     # Main application entrypoint and UI orchestration
├── gemini_client.py           # NLP extraction and recommendation logic
├── rawg_client.py             # RAWG REST API client and data fetching
├── requirements.txt           # Production dependencies
└── README.md                  # Project documentation and showcase
```

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

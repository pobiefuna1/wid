
# WID Trailblazer Zones 🗺️🚶‍♀️

This is the official web app for the **WID Walking Group** in Edmonton, Alberta.  
It helps walkers and residents locate which of the 10 *Trailblazer Zones* any given address falls into—based on major road boundaries and neighborhood clusters.

🌐 Live app: [https://widwalk.streamlit.app](https://widwalk.streamlit.app)

---

## 🔍 What It Does

- Accepts any Edmonton address
- Uses OpenCage geocoding to retrieve coordinates
- Matches those coordinates against zone boundaries
- Returns a human-readable **zone name** and **location description** (e.g., “Callingwood, Lymburn, Aldergrove”)

---

## 📦 Project Structure

```
wid_app.py           # Main Streamlit interface
widzone.py           # Core logic: geocoding + zone detection
wid_logo_web_ready/  # Branding assets (transparent + WebP logo)
```

---

## 🧠 How Zones Are Defined

Zones are mapped using bounding boxes (latitude/longitude ranges).  
Each zone corresponds to a set of neighborhoods and major roads—like “97 St to 124 St, 111 Ave to River Valley” for **Heart Trail Zone**.

Full zone info is stored in a dictionary: `ZONE_INFO` inside `widzone.py`.

---

## 🗝️ Setup (for local development)

1. Clone this repo  
2. Install dependencies:

```bash
pip install streamlit opencage
```

3. Set your OpenCage API key in `widzone.py`:
```python
API_KEY = "your-api-key-here"
```

4. Run the app:
```bash
streamlit run wid_app.py
```

---

## 📄 License & Acknowledgements

This project was built by **Peter C. M. Obiefuna** in collaboration with the WID community.  
It is offered in the spirit of shared health, connection, and belonging.

&copy; 2025 WID Walking Group – All rights reserved.

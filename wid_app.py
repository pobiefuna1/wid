import streamlit as st
from pathlib import Path
from widzone import WidTrailblazer

# --- Config ---
API_KEY = "3dc65113cf8e4f10a2802af5cb630947"  # Set your OpenCage API key here
trail = WidTrailblazer(API_KEY)

# --- Page setup ---
st.set_page_config(page_title="WID Zone Checker", page_icon="🗺️")

# --- Logo ---

logo_path = Path(__file__).parent / "wid_logo_web_ready" / "wid_logo_transparent.png"
if logo_path.exists():
    st.image(str(logo_path), width=180)

# --- UI ---
st.title("🚶‍♀️ WID Trailblazer Zone Checker")
st.write("Enter any Edmonton address to find its walking zone.")

address = st.text_input("📍 Address", placeholder="e.g., 124 Street NW & 111 Avenue NW, Edmonton")

if address:
    if address.startswith("?"):
        command = address.strip().lower()

        if command == "?zones":
            st.markdown("### 🗺️ Current WID Trailblazer Zones:")
            for z in trail.zones:
                st.markdown(f"- **{z}**: {trail.describe(z)}")
        else:
            st.warning("Unknown command.")
    else:
        try:
            zone, location, (lat, lon) = trail.lookup_address(address)
            st.success(f"✅ This address belongs to **{zone}**.")
            st.markdown(f"**Location:** {location}")
        except Exception as e:
            st.error("❌ Unable to locate that address. Please check spelling or try a nearby intersection.")
            st.code(str(e))


# --- Footer ---
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; font-size: 0.9em;'>
        For walking tips and community support, visit:
        <a href="https://widwalk.com/" target="_blank" style="color:#00cc66;">widwalk.com</a>
    </div>
    <div style='text-align: center; font-size: 0.8em; color: gray; margin-top: 6px;'>
        © 2025 Peter Obiefuna, Arizen Corporation
    </div>
    """,
    unsafe_allow_html=True
)

import streamlit as st
from pathlib import Path
from widzone import get_zone_from_address, get_coordinates

# Page config
st.set_page_config(page_title="WID Zone Checker", page_icon="🗺️")

# Optional: display logo if available
logo_path = Path(__file__).parent / "wid_logo_web_ready" / "wid_logo_transparent.png"
if logo_path.exists():
    st.image(str(logo_path), width=180)

# Title and intro
st.title("🚶‍♀️ WID Trailblazer Zone Checker")
st.write("Enter any Edmonton address to find its walking zone.")

# Address input field
address = st.text_input("📍 Address", placeholder="e.g., 124 Street NW & 111 Avenue NW, Edmonton")

# Address lookup logic
if address:
    try:
        zone = get_zone_from_address(address)
        lat, lon = get_coordinates(address)

        st.success(f"✅ This address belongs to **{zone}**.")
        from widzone import ZONE_INFO
        st.markdown(f"**Location:** {ZONE_INFO.get(zone, 'Unknown')}")

    except Exception as e:
        st.error("❌ Unable to locate that address. Please check spelling or try a nearby intersection.")
        st.code(str(e))

# Footer
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

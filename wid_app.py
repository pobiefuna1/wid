import streamlit as st
from pathlib import Path
from widzone import WidTrailblazer

# --- Config ---
API_KEY = "3dc65113cf8e4f10a2802af5cb630947"  # Set your OpenCage API key here
trail = WidTrailblazer(API_KEY)

# --- Page setup ---
st.set_page_config(page_title="WID Zone", page_icon="🗺️")

# --- Logo ---

logo_path = Path(__file__).parent / "wid_logo_web_ready" / "wid_logo_transparent.png"
if logo_path.exists():
    st.image(str(logo_path), width=180)

# --- UI ---
st.markdown("""
<h2 style='text-align: center; font-size: 1.8em;'>
🚶‍♀️ WID Trailblazer Zone
</h2>
""", unsafe_allow_html=True)
st.write("Enter any Edmonton address to find its walking zone.")

address = st.text_input("📍 Address", placeholder="e.g., 124 Street NW & 111 Avenue NW, Edmonton")

if address:
    if address.startswith("?"):
        command_parts = address.strip().split(maxsplit=1)
        command = command_parts[0].lower()
        arg = command_parts[1] if len(command_parts) > 1 else ""

        if command == "?zones":
            st.markdown("### 🗺️ Current WID Trailblazer Zones:")
            for z in trail.zones:
                st.markdown(f"- **{z}**: {trail.describe(z)}")

        elif command == "?coords" and arg:
            try:
                lat, lon = trail.get_coordinates(arg)
                st.info(f"📍 **Coordinates:** {lat:.5f}, {lon:.5f}")
            except Exception as e:
                st.error("❌ Could not resolve address.")
                st.code(str(e))

        elif command == "?trace" and arg:
            try:
                lat, lon = trail.get_coordinates(arg)
                zone = trail.get_zone(lat, lon)
                st.info(f"📍 **lat:** {lat:.6f}, **lon:** {lon:.6f}\n🧭 **Zone:** {zone}")
            except Exception as e:
                st.error("❌ Trace failed.")
                st.code(str(e))

        elif command == "?whoami" and arg:
            try:
                zone, location, _ = trail.lookup_address(arg)
                st.success(f"📍 This address falls within **{zone}**, covering: {location}")
            except Exception as e:
                st.error("❌ Could not locate address.")
                st.code(str(e))

        elif command in ["?help", "?"]:
            st.markdown("""
### 🛠️ WID Zone Checker Command Help

You can use the following commands:

- `?zones` — List all defined zone names and descriptions  
- `?coords <address>` — Show latitude/longitude for an address  
- `?trace <address>` — Show how a zone was resolved (match type + lat/lon)  
- `?whoami <address>` — Friendly summary of zone + location  
- `?help` or `?` — Display this help menu
""")

        else:
            st.warning("❓ Unknown command. Type `?` or `?help` to see options.")
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


import streamlit as st
from widzone import get_zone_from_address, get_coordinates

st.set_page_config(page_title="WID Zone Checker", page_icon="🗺️")

st.title("🚶‍♀️ WID Trailblazer Zone Checker")
st.write("Enter any Edmonton address to find its walking zone.")

address = st.text_input("📍 Address", placeholder="e.g., 124 Street NW & 111 Avenue NW, Edmonton")

if address:
    try:
        zone = get_zone_from_address(address)
        lat, lon = get_coordinates(address)

        st.success(f"✅ This address belongs to **{zone}**.")
        st.markdown(f"**Coordinates:** {lat:.5f}, {lon:.5f}")

    except Exception as e:
        st.error("❌ Unable to locate that address. Please check spelling or try a nearby intersection.")
        st.code(str(e))


from opencage.geocoder import OpenCageGeocode

# Replace with your actual OpenCage API key
API_KEY = "3dc65113cf8e4f10a2802af5cb630947"
geocoder = OpenCageGeocode(API_KEY)

ZONE_INFO = {
    "Heart Trail Zone": "97 St to 124 St, 111 Ave to River Valley (Downtown, Oliver, Rossdale)",
    "Northern Steps Zone": "97 St to 121 St, 127 Ave to 111 Ave (Kingsway, Alberta Ave, NAIT)",
    "River Rise Zone": "34 St to 50 St, 153 Ave to 118 Ave (Clareview, Beverly, Highlands)",
    "Trail West Zone": "124 St to 149 St, 107 Ave to 124 Ave (Glenora, Westmount)",
    "Valley Weave Zone": "75 St to 91 St, 98 Ave to 82 Ave (Strathearn, Bonnie Doon)",
    "Southwalk Zone": "66 St to 91 St, 34 Ave to 23 Ave (Millwoods North)",
    "Whitemud Path Zone": "119 St to 142 St, 23 Ave to Whitemud Dr (Riverbend, Brookside)",
    "Lakeside Loop Zone": "97 St to 127 St, 153 Ave to Henday (Lake District)",
    "Southridge Zone": "111 St to 119 St, 23 Ave to Henday (Twin Brooks, Heritage)",
    "Westfield Trail Zone": "170 St to 215 St, Whitemud to 87 Ave (Callingwood, Lymburn, Aldergrove)",
    "Unmapped Zone": "Not within current trail boundaries",
}



def get_coordinates(address):
    # Clean and normalize input for OpenCage
    cleaned = f"{address}, Edmonton, AB, Canada"
    result = geocoder.geocode(cleaned)
    if result and len(result):
        lat = result[0]['geometry']['lat']
        lon = result[0]['geometry']['lng']
        return lat, lon
    else:
        raise ValueError(f"Could not geocode: {cleaned}")

def get_zone_from_address(address):
    lat, lon = get_coordinates(address)

    # 1. Heart Trail Zone
    if 53.542 <= lat <= 53.570 and -113.521 <= lon <= -113.496:
        return "Heart Trail Zone"

    # 2. Northern Steps Zone
    elif 53.570 < lat <= 53.595 and -113.521 <= lon <= -113.500:
        return "Northern Steps Zone"

    # 3. River Rise Zone
    elif 53.570 <= lat <= 53.630 and -113.410 <= lon <= -113.370:
        return "River Rise Zone"

    # 4. Trail West Zone
    elif 53.550 <= lat <= 53.580 and -113.560 <= lon <= -113.530:
        return "Trail West Zone"

    # 5. Valley Weave Zone
    elif 53.520 <= lat <= 53.540 and -113.460 <= lon <= -113.430:
        return "Valley Weave Zone"

    # 6. Southwalk Zone
    elif 53.450 <= lat <= 53.480 and -113.430 <= lon <= -113.410:
        return "Southwalk Zone"

    # 7. Whitemud Path Zone
    elif 53.470 <= lat <= 53.500 and -113.590 <= lon <= -113.520:
        return "Whitemud Path Zone"

    # 8. Lakeside Loop Zone
    elif 53.610 <= lat <= 53.640 and -113.540 <= lon <= -113.490:
        return "Lakeside Loop Zone"

    # 9. Southridge Zone
    elif 53.430 <= lat <= 53.460 and -113.600 <= lon <= -113.510:
        return "Southridge Zone"

    # 10. Westfield Trail Zone (expanded north to include lat 53.532)
    elif 53.500 <= lat <= 53.540 and -113.700 <= lon <= -113.580:
        return "Westfield Trail Zone"

    else:
        import streamlit as st
        st.warning(f"Unmapped Zone → lat: {lat:.6f}, lon: {lon:.6f}")
        return "Unmapped Zone"

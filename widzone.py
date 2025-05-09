import streamlit as st
from opencage.geocoder import OpenCageGeocode

from geopy.geocoders import Nominatim

# Mobile-friendly layout and title
st.set_page_config(layout="centered")
st.image("icae_logo.png", width=120)

# Set your OpenCage API key
API_KEY = "3dc65113cf8e4f10a2802af5cb630947"
geocoder = OpenCageGeocode(API_KEY)
EDMONTON_LAT = 53.5461
EDMONTON_LON = -113.4938
EDMONTON_CENTER = (53.5461, -113.4938)  # Approximate city center

# Within 150 Km radius 
OUTER_LIMITS = 150

# Predefined WID zone bounding boxes (manually estimated)
WID_ZONES = {
    "Heart Trail Zone":      {"lat_min": 53.532, "lat_max": 53.550, "lon_min": -113.537, "lon_max": -113.514},
    "Northern Steps Zone":   {"lat_min": 53.564, "lat_max": 53.582, "lon_min": -113.540, "lon_max": -113.514},
    "River Rise Zone":       {"lat_min": 53.562, "lat_max": 53.625, "lon_min": -113.410, "lon_max": -113.339},
    "Stroll & Summit Zone":  {"lat_min": 53.582, "lat_max": 53.645, "lon_min": -113.564, "lon_max": -113.540},
    "Sunset Trail Zone":     {"lat_min": 53.512, "lat_max": 53.550, "lon_min": -113.612, "lon_max": -113.537},
    "Prairie Pathways Zone": {"lat_min": 53.408, "lat_max": 53.512, "lon_min": -113.630, "lon_max": -113.612},
    "Ravine Roots Zone":     {"lat_min": 53.515, "lat_max": 53.530, "lon_min": -113.506, "lon_max": -113.465},
    "Mill Mile Zone":        {"lat_min": 53.408, "lat_max": 53.512, "lon_min": -113.455, "lon_max": -113.408},
    "Golden Stride Zone":    {"lat_min": 53.510, "lat_max": 53.525, "lon_min": -113.478, "lon_max": -113.408},
    "East Horizon Zone":     {"lat_min": 53.562, "lat_max": 53.625, "lon_min": -113.339, "lon_max": -113.295},
}
# Geocode function using OpenCage
def geocode_address(address):
    results = geocoder.geocode(address)
    if results and len(results) > 0:
        lat = results[0]['geometry']['lat']
        lon = results[0]['geometry']['lng']
        formatted = results[0]['formatted']
        return formatted, lat, lon
    else:
        return None, None, None
        
# Address cleaner
def clean_address(raw):
    replacements = {
        r'\bSt\b': 'Street',
        r'\bStr\b': 'Street',
        r'\bRd\b': 'Road',
        r'\bAve\b': 'Avenue',
        r'\bBlvd\b': 'Boulevard',
        r'\bDr\b': 'Drive',
        r'\bCt\b': 'Court',
        r'\bCres\b': 'Crescent',
        r'\bPl\b': 'Place',
        r'\bTer\b': 'Terrace',
        r'\bNW\b': 'NW',
        r'\bSW\b': 'SW',
        r'\bNE\b': 'NE',
        r'\bSE\b': 'SE'
    }
    for pattern, replacement in replacements.items():
        raw = re.sub(pattern, replacement, raw, flags=re.IGNORECASE)
    return raw.strip()
    

def get_coordinates(address):
    geolocator = Nominatim(user_agent="wid-zone-locator")
    location = geolocator.geocode(address)
    if not location:
        raise ValueError("Could not geocode address")
    return location.latitude, location.longitude

def get_zone_from_address(address):
    lat, lon = get_coordinates(address)
    for zone, bounds in WID_ZONES.items():
        if (bounds["lat_min"] <= lat <= bounds["lat_max"] and
            bounds["lon_min"] <= lon <= bounds["lon_max"]):
            return zone
    return "Unknown Zone"

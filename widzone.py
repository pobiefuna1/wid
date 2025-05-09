
from opencage.geocoder import OpenCageGeocode

# Replace with your actual OpenCage API key
API_KEY = "3dc65113cf8e4f10a2802af5cb630947"
geocoder = OpenCageGeocode(API_KEY)

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

    # 9. Southridge Zone (expanded westward)
    elif 53.430 <= lat <= 53.460 and -113.600 <= lon <= -113.510:
        return "Southridge Zone"

    # 10. Westfield Trail Zone (expanded westward to include 190 St)
    elif 53.500 <= lat <= 53.520 and -113.700 <= lon <= -113.590:
        return "Westfield Trail Zone"

    else:
        return "Unmapped Zone"

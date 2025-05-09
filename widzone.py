from opencage.geocoder import OpenCageGeocode

class WidTrailblazer:
    def __init__(self, api_key):
        self.geocoder = OpenCageGeocode(api_key)
        self.zones = self._load_zones()
        self.ZONE_INFO = {
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

    def get_coordinates(self, address):
        cleaned = f"{address}, Edmonton, AB, Canada"
        result = self.geocoder.geocode(cleaned)
        if result and len(result):
            lat = result[0]['geometry']['lat']
            lon = result[0]['geometry']['lng']
            return lat, lon
        else:
            raise ValueError(f"Could not geocode: {cleaned}")

    def get_zone(self, lat, lon):
        margin = 0.002  # Safe margin (~200m)

        # Deterministic evaluation order — central/dense zones first
        ordered_zones = [
            "Heart Trail Zone",
            "Northern Steps Zone",
            "Trail West Zone",
            "Valley Weave Zone",
            "Southwalk Zone",
            "Whitemud Path Zone",
            "Lakeside Loop Zone",
            "River Rise Zone",
            "Southridge Zone",
            "Westfield Trail Zone"
        ]

        for name in ordered_zones:
            bounds = self.zones.get(name)
            if ((bounds["lat_min"] - margin) <= lat <= (bounds["lat_max"] + margin) and
                (bounds["lon_min"] - margin) <= lon <= (bounds["lon_max"] + margin)):
                return name

    self._log_unmapped(lat, lon)
    return "Unmapped Zone"

    def _log_unmapped(self, lat, lon):
        print(f"[UNMAPPED] lat={lat:.6f}, lon={lon:.6f}")
        for name, b in self.zones.items():
            lat_match = b["lat_min"] <= lat <= b["lat_max"]
            lon_match = b["lon_min"] <= lon <= b["lon_max"]
            print(f"→ {name}: lat_match={lat_match}, lon_match={lon_match}")

    def _load_zones(self):
        return {
            "Heart Trail Zone": {"lat_min": 53.542, "lat_max": 53.570, "lon_min": -113.521, "lon_max": -113.496},
            "Northern Steps Zone": {"lat_min": 53.570, "lat_max": 53.595, "lon_min": -113.521, "lon_max": -113.500},
            "River Rise Zone": {"lat_min": 53.570, "lat_max": 53.630, "lon_min": -113.410, "lon_max": -113.370},
            "Trail West Zone": {"lat_min": 53.550, "lat_max": 53.580, "lon_min": -113.560, "lon_max": -113.530},
            "Valley Weave Zone": {"lat_min": 53.520, "lat_max": 53.540, "lon_min": -113.460, "lon_max": -113.430},
            "Southwalk Zone": {"lat_min": 53.450, "lat_max": 53.480, "lon_min": -113.430, "lon_max": -113.410},
            "Whitemud Path Zone": {"lat_min": 53.470, "lat_max": 53.500, "lon_min": -113.590, "lon_max": -113.520},
            "Lakeside Loop Zone": {"lat_min": 53.610, "lat_max": 53.640, "lon_min": -113.540, "lon_max": -113.490},
            "Southridge Zone": {"lat_min": 53.430, "lat_max": 53.460, "lon_min": -113.600, "lon_max": -113.510},
            "Westfield Trail Zone": {"lat_min": 53.500, "lat_max": 53.540, "lon_min": -113.700, "lon_max": -113.580},
        }

    def describe(self, zone_name):
        return self.ZONE_INFO.get(zone_name, "Unknown location.")

    def lookup_address(self, address):
        lat, lon = self.get_coordinates(address)
        zone = self.get_zone(lat, lon)
        description = self.describe(zone)
        return zone, description, (lat, lon)

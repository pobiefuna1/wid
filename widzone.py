
from opencage.geocoder import OpenCageGeocode
from math import radians, sin, cos, sqrt, atan2

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
            
            if self._distance_from_edmonton(lat, lon) > 50:
                raise ValueError(f"Address resolved too far from Edmonton center: {lat:.5f}, {lon:.5f}")
            
            return lat, lon
        else:
            raise ValueError(f"Could not geocode: {cleaned}")

    def _distance_from_edmonton(self, lat, lon):
        # Edmonton reference point
        lat0, lon0 = 53.5461, -113.4938
        R = 6371  # Earth radius in km

        dlat = radians(lat - lat0)
        dlon = radians(lon - lon0)
        a = sin(dlat/2)**2 + cos(radians(lat0)) * cos(radians(lat)) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c

    def get_zone(self, lat, lon):
        for name, bounds in self.zones.items():
            if (bounds["lat_min"] <= lat <= bounds["lat_max"] and
                bounds["lon_min"] <= lon <= bounds["lon_max"]):
                return name

        for name, b in self.zones.items():
            if lat > b["lat_max"] and b["lon_min"] <= lon <= b["lon_max"]:
                return name
            elif lat < b["lat_min"] and b["lon_min"] <= lon <= b["lon_max"]:
                return name
            elif lon < b["lon_min"] and b["lat_min"] <= lat <= b["lat_max"]:
                return name
            elif lon > b["lon_max"] and b["lat_min"] <= lat <= b["lat_max"]:
                return name

        def center(bounds): return ((bounds["lat_min"] + bounds["lat_max"]) / 2,
                                    (bounds["lon_min"] + bounds["lon_max"]) / 2)
        def distance(c): return abs(c[0] - lat) + abs(c[1] - lon)
        closest = min(self.zones.items(), key=lambda z: distance(center(z[1])))
        return closest[0]

    def describe(self, zone_name):
        return self.ZONE_INFO.get(zone_name, "Unknown location.")

    def lookup_address(self, address):
        lat, lon = self.get_coordinates(address)
        zone = self.get_zone(lat, lon)
        description = self.describe(zone)
        return zone, description, (lat, lon)

    def _load_zones(self):
        return {
            "Westfield Trail Zone": {
                "lat_min": 53.430, "lat_max": 53.550,
                "lon_min": -113.600, "lon_max": -113.580
            },
            "Southridge Zone": {
                "lat_min": 53.430, "lat_max": 53.470,
                "lon_min": -113.750, "lon_max": -113.600
            },
            "Whitemud Path Zone": {
                "lat_min": 53.470, "lat_max": 53.500,
                "lon_min": -113.600, "lon_max": -113.540
            },
            "Heart Trail Zone": {
                "lat_min": 53.500, "lat_max": 53.540,
                "lon_min": -113.600, "lon_max": -113.540
            },
            "Trail West Zone": {
                "lat_min": 53.540, "lat_max": 53.570,
                "lon_min": -113.600, "lon_max": -113.540
            },
            "Northern Steps Zone": {
                "lat_min": 53.570, "lat_max": 53.610,
                "lon_min": -113.600, "lon_max": -113.540
            },
            "Lakeside Loop Zone": {
                "lat_min": 53.610, "lat_max": 53.650,
                "lon_min": -113.600, "lon_max": -113.540
            },
            "Valley Weave Zone": {
                "lat_min": 53.500, "lat_max": 53.540,
                "lon_min": -113.540, "lon_max": -113.460
            },
            "Southwalk Zone": {
                "lat_min": 53.430, "lat_max": 53.500,
                "lon_min": -113.540, "lon_max": -113.460
            },
            "River Rise Zone": {
                "lat_min": 53.500, "lat_max": 53.650,
                "lon_min": -113.460, "lon_max": -113.360
            }
        }

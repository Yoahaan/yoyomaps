#this script will take the name of a place and return the latitude and longitude

from geopy.geocoders import Nominatim

def get_lat_lon(place_name):
    geolocator = Nominatim(user_agent="geo_locator")
    location = geolocator.geocode(place_name)
    
    if location:
        return {"latitude": location.latitude, "longitude": location.longitude}
    else:
        return {"error": "Location not found"}

    

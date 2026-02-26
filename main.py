import json
import urllib.request, urllib.parse
import ssl
import math
import folium

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

serviceurl = "http://py4e-data.dr-chuck.net/opengeo?"

def get_coordonées(location):
    params = dict()
    params['q'] = location
    url = serviceurl + urllib.parse.urlencode(params)

    data = urllib.request.urlopen(url, context=ctx).read().decode()
    term = json.loads(data)
    
    if not term["features"]:
        print("Location not found!")
        return None, None, None
    else:
        lat = term["features"][0]["properties"]["lat"]
        lon = term["features"][0]["properties"]["lon"]
        plus_code = term["features"][0]["properties"]["plus_code"]

    return lat, lon, plus_code


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # rayon de la Terre en km

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    distance = R * c
    return distance


# Adresse 1
loc1 = input("Enter first location: ").strip()
lat1, lon1, code1 = get_coordonées(loc1)

print("\nLocation 1:")
print("Plus code:", code1)
print("Latitude:", lat1)
print("Longitude:", lon1)

# Adresse 2
loc2 = input("\nEnter second location: ").strip()
lat2, lon2, code2 = get_coordonées(loc2)

print("\nLocation 2:")
print("Plus code:", code2)
print("Latitude:", lat2)
print("Longitude:", lon2)

# Distance
distance = haversine(lat1, lon1, lat2, lon2)
d = round(distance, 2)
print(f"\nDistance between locations: {d} km, {d*0.621371:.2f} miles")

#centre de la carte = milieu entre deux point
centre_lat = (lat1 + lat2) / 2
centre_lon = (lon1 + lon2) / 2

#creation du carte
m = folium.Map(location=[centre_lat, centre_lon], zoom_start=7)

#point 1
folium.Marker(
    [lat1, lon1],
    popup="location 1",
).add_to(m)

#point 2
folium.Marker(
    [lat2, lon2],
    popup="location 2",
).add_to(m)

#ligne entre deux
folium.PolyLine(
    locations=[[lat1, lon1], [lat2, lon2]],
).add_to(m)

#sauvegarder la carte
m.save("Map.html")
print("\nCarte sauvegardée sous 'Map.html'")
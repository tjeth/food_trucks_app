from flask import Flask, render_template, send_file, request, jsonify
import requests
import threading
import json
import time
from werkzeug.contrib.cache import SimpleCache
from math import radians, cos, sin, asin, sqrt

app = Flask(__name__)

# Google Maps API
API_KEY = 'AIzaSyCFPJGIIcbIUmbIitqx2chf5pqdYHGTqsI'
# Key: item address, Value: location item
no_latlong_cache = SimpleCache() 
# Background thread for refreshing locations
refresh_thread = threading.Thread()

# Refresh JSON file containing locations every 24 hours
def refresh_locations():
  print "Refreshing cache"

  # Run once per day
  t = threading.Timer(86400.0, refresh_locations)
  
  # Allows you to interrupt program cleanly
  t.daemon = True
  t.start()

  # Request to food trucks data API
  response = requests.get('http://data.sfgov.org/resource/rqzj-sfat.json').content

  data = json.loads(response)

  locations = []
  no_latlong = []

  build_locations_lists(data, locations, no_latlong)
  geocode_no_latlong_locations(locations, no_latlong)

  f = open('food_truck_data.json','w')
  json.dump(locations, f, indent=0)
  f.close()


# Build locations list with relevant data for views
# Add to a list for geocoding if does not have latlong
def build_locations_lists(data, locations, no_latlong):
  id_count = 1

  for x in range(0, len(data)):
    item = data[x]
    if (item['status'] == 'APPROVED'):
      if ('location' not in item and 'address' in item):
        # Found only address, so add to list for geocoding later
        item['id'] = id_count
        no_latlong.append(item)
      elif ('location' in item and 'address' in item): 
        # Found with location and address
        locations.append({ 'lat' : item['location']['latitude'], \
            'lng' : item['location']['longitude'], \
            'applicant' : item['applicant'], \
            'address' : item['address'], \
            'fooditems' : item['fooditems'],
            'id' : id_count })
      elif ('location' in item and 'address' not in item): 
        # Has latlong but no address
        locations.append({ 'lat' : item['location']['latitude'], \
            'lng' : item['location']['longitude'], \
            'applicant' : item['applicant'], \
            'address' : 'No Address', \
            'fooditems' : item['fooditems'],
            'id' : id_count })
      else:
        print 'Truck does not have latlong or address!\n{}'.format(str(item))
      id_count += 1


# Geocode the locations with no latlongs using Google Maps API
# Use cache to speed things up on subsequent iterations
# Finally, add item to locations list
def geocode_no_latlong_locations(locations, no_latlong):
  for x in range(0, len(no_latlong)):
    item = no_latlong[x]
    cache_key = item['address']
    cache_item = no_latlong_cache.get(cache_key)

    if (cache_item):
      locations.append(cache_item)
    else:
      resp_data = googleMapsGeocode(item['address'] + ', San Francisco')

      geo_loc = resp_data['results'][0]['geometry']['location']
      location_item = { 'lat' : geo_loc['lat'], \
          'lng' : geo_loc['lng'],\
          'applicant' : item['applicant'],\
          'address' : item['address'],\
          'fooditems' : item['fooditems'],
          'id' : item['id']}
      locations.append(location_item)
      no_latlong_cache.set(cache_key, location_item, timeout=30*24*60) #30 day timeout


# Function for refreshing locations on a separate thread
def execute_refresh_locations():
  global refresh_thread
  # Start the timer loop that runs every 24 hours
  refresh_thread = threading.Thread(target=refresh_locations)
  refresh_thread.daemon = True
  refresh_thread.start()


# Execute refreshing locations in a separate thread 
execute_refresh_locations()


# Helper function, Haversine formula for calculating distance b/w two points on sphere
# Source: http://stackoverflow.com/a/4913653
def haversine(lon1, lat1, lon2, lat2):
  """
  Calculate the great circle distance between two points 
  on the earth (specified in decimal degrees)
  """
  # convert decimal degrees to radians 
  lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

  # haversine formula 
  dlon = lon2 - lon1 
  dlat = lat2 - lat1 
  a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
  c = 2 * asin(sqrt(a)) 

  # 6367 km is the radius of the Earth
  km = 6367 * c
  return km 


# Helper function for Google Maps geocoding
def googleMapsGeocode(addr):
  payload = {'address': addr, 'key': API_KEY}
  resp = requests.get('https://maps.googleapis.com/maps/api/geocode/json', \
    params=payload).content
  return json.loads(resp)


@app.route("/")
def index():
  return render_template('index.html')


@app.route("/food_truck_locations")
def food_truck_locations():
  return send_file('food_truck_data.json')


@app.route("/address_search")
def address_search():
  resp_data = googleMapsGeocode(request.args.get("address"))

  if len(resp_data['results']) != 0:
    formatted_address = resp_data['results'][0]["formatted_address"]

    # Make sure address is in San Francisco
    if "San Francisco" in formatted_address:
      geo_loc = resp_data['results'][0]['geometry']['location']

      lat1 = float(geo_loc['lat'])
      lng1 = float(geo_loc['lng'])

      search_latlong = {'lat': lat1, 'lng': lng1}

      within_mile = []
      json_data = open('food_truck_data.json')
      data = json.load(json_data)
      for location in data:
        lat2 = float(location['lat'])
        lng2 = float(location['lng'])

        haversine_distance = haversine(lng1, lat1, lng2, lat2)

        if (haversine_distance < 1.0): # Less than one kilometer away
          within_mile.append(location)

      json_data.close()
      return jsonify(search_address=search_latlong, results=within_mile)
    else:
      return "Please input a San Francisco address!"
  return "No address search results"

if __name__ == "__main__":
  app.run(debug=True)

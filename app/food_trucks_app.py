from flask import Flask, render_template
import requests
import threading
import json
import time
from werkzeug.contrib.cache import SimpleCache

app = Flask(__name__)

API_KEY = 'AIzaSyCFPJGIIcbIUmbIitqx2chf5pqdYHGTqsI'
no_latlong_cache = SimpleCache() #Key: item address, Value: location item

def refresh_cache():
  print "Refreshing cache"

  # Run once per day
  t = threading.Timer(86400.0, refresh_cache)
  #t = threading.Timer(10.0, refresh_cache)
  
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
  for x in range(0, len(data)):
    item = data[x]
    if (item['status'] == 'APPROVED'):
      if ('location' not in item and 'address' in item):
        no_latlong.append(item)
      elif ('location' in item and 'address' in item): 
        # Found with location and address
        locations.append({ 'lat' : item['location']['latitude'], \
            'lng' : item['location']['longitude'], \
            'applicant' : item['applicant'], \
            'address' : item['address'], \
            'fooditems' : item['fooditems'] })
      elif ('location' in item and 'address' not in item): 
        # Has latlong but no address
        locations.append({ 'lat' : item['location']['latitude'], \
            'lng' : item['location']['longitude'], \
            'applicant' : item['applicant'], \
            'address' : 'No Address', \
            'fooditems' : item['fooditems'] })
      else:
        print 'Truck does not have latlong or address!\n{}'.format(str(item))

  print len(locations)
  print len(no_latlong)


# Geocode the locations with no latlongs using Google Maps API
# Use cache to speed things up on subsequent iterations
# Finally, add item to locations list
def geocode_no_latlong_locations(locations, no_latlong):
  for x in range(0, len(no_latlong)):
    item = no_latlong[x]
    cache_key = item['address']
    cache_item = no_latlong_cache.get(cache_key)
    print cache_item
    if (cache_item):
      print "HELLO WORLD"
      locations.append(cache_item)
    else:
      addr = item['address'] + ', San Francisco'
      payload = {'address': addr, 'key': API_KEY}
      resp = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params=payload).content
      resp_data = json.loads(resp)

      geo_loc = resp_data['results'][0]['geometry']['location']
      location_item = { 'lat' : geo_loc['lat'], \
          'lng' : geo_loc['lng'],\
          'applicant' : item['applicant'],\
          'address' : item['address'],\
          'fooditems' : item['fooditems'] }
      locations.append(location_item)
      no_latlong_cache.set(cache_key, location_item, timeout=30*24*60) #30 day timeout

  print len(locations) 


# Start the timer loop that runs every 24 hours
refresh_cache()


@app.route("/")
def hello():
  return render_template('index.html')

if __name__ == "__main__":
  app.run(debug=True)

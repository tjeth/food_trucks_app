from flask import Flask, render_template
import requests
import threading
import json

app = Flask(__name__)

#TODO: Problem killing the server process with Ctrl-C if you use this 
def refresh_cache():
  # Run once per day
  #threading.Timer(86400.0, refresh_cache).start()
  data = requests.get('http://data.sfgov.org/resource/rqzj-sfat.json').content
  f = open('food_truck_data.json','w')
  f.write(data)
  f.close()

#refresh_cache()

@app.route("/")
def hello():
  json_data = open('food_truck_data.json')
  data = json.load(json_data)

  locations = []
  no_latlong = []

  # Build locations list with relevant data for views
  # Add to a list for geolocation if does not have latlong
  for x in range(0, len(data)):
    if (data[x]['status'] == 'APPROVED'):
      if ('location' not in data[x] and 'address' in data[x]):
        no_latlong.append(data[x])
      elif ('location' in data[x] and 'address' in data[x]): 
        # Found with location and address
        locations.append({ 'lat' : data[x]['location']['latitude'], \
            'lng' : data[x]['location']['longitude'], \
            'applicant' : data[x]['applicant'], \
            'address' : data[x]['address'], \
            'fooditems' : data[x]['fooditems'] })
      elif ('location' in data[x] and 'address' not in data[x]): 
        # Has latlong but no address
        locations.append({ 'lat' : data[x]['location']['latitude'], \
            'lng' : data[x]['location']['longitude'], \
            'applicant' : data[x]['applicant'], 
            'address' : 'No Address', \
            'fooditems' : data[x]['fooditems'] })
      else:
        print 'Truck does not have latlong or address!\n{}'.format(str(data[x]))

  print len(locations)
  print len(no_latlong)

  return render_template('index.html')

if __name__ == "__main__":
  app.run(debug=True)

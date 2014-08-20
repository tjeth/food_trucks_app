Food Trucks App 
====================

### Application Link
* http://food-trucks-app.herokuapp.com

### Backend
* Uses Python and the Flask (http://flask.pocoo.org/) framework
* Queries SF food trucks data (https://data.sfgov.org/Economy-and-Community/Mobile-Food-Facility-Permit/rqzj-sfat?) and does data parsing
* Geocodes using Google Maps API the addresses of data points that do not have latlongs
* Caches the geocoded latlongs using SimpleCache 
* Queries the data source every 24 hours in a separate thread
* Search functionality uses the Haversine formula to calculate distance from address entered for each item in data set, only returning locations within 1km
* Data stored in JSON file because it is relatively static and would need to refresh from scratch after re-querying data source

### API
* Name: /food_truck_locations; Method: GET; Required Params: None; Description: Returns all the food truck locations.
* Name: /address_search; Method: GET; Required Params: address (string); Description: Returns all food truck locations within 1km radius of input address

### Frontend
* Uses Backbone.js (http://backbonejs.org/), application is a single page app
* Uses Backbone.GoogleMaps library (https://github.com/eschwartz/backbone.googlemaps) and Google Maps to render pins from data source
* Uses Backgrid.js (http://backgridjs.com/) for the data table 
* Backbone models retrieve data from the server

### Testing
* Using Python's coverage library and running the food_truck_tests.py test suite, the backend has 94% code coverage

### Main Files of Interest
* food_trucks_app.py (Backend server file)
* food_truck_tests.py (Backend tests)
* static/food_trucks.js (Backbone Javascript models, collections, and views)
* static/food_trucks.css (Application CSS)
* templates/index.html (Application HTML template)

### Things Could Have Added With More Time
* Clicking on GoogleMaps Marker highlights the specific row in the Table (currently has id so you can look up in the table manually)
* Show user's geolocation on the map
* Frontend unit testing with Jasmine
* Additional styling to make app look nicer




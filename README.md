Food Trucks App 
====================

### Backend
* Uses Python and the Flask (http://flask.pocoo.org/) framework
* Queries SF food trucks data (https://data.sfgov.org/Economy-and-Community/Mobile-Food-Facility-Permit/rqzj-sfat?) and does data parsing
* Geocodes using Google Maps API the addresses of data points that do not have latlongs
* Caches the geocoded latlongs using SimpleCache 
* Queries the data source every 24 hours in a separate thread
* Search functionality uses the Haversine formula to calculate distance from address entered for each item in data set, only returning locations within 1km

*** Frontend
* Uses Backbone.js, application is a single page app
* Uses Backbone.GoogleMaps library and Google Maps to render pins from data source
* Uses Backgrid.js for the data table 
* Backbone models retrieve data from the server

*** Things Could Have Added With More Time
* Clicking on GoogleMaps Marker highlights the specific row in the Table (currently has id so you can look up in the table manually)
* Show user's geolocation on the map
* Additional styling to make app look nicer



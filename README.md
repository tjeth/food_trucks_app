Food Trucks App 
====================

### Backend
* Uses Python and the Flask (http://flask.pocoo.org/) framework
* Queries SF food trucks data (https://data.sfgov.org/Economy-and-Community/Mobile-Food-Facility-Permit/rqzj-sfat?) and does data parsing
* Geocodes using Google Maps API the addresses of data points that do not have latlongs
* Caches the geocoded latlongs using SimpleCache 
* Queries the data source every 24 hours in a separate thread



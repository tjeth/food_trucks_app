$(document).ready(function() {
  console.log("Inside beginning of food_truck.js");

  var map = new google.maps.Map($('#map-canvas')[0], {
      center: new google.maps.LatLng(37.7833, -122.4167),
      zoom: 14,
      mapTypeId: google.maps.MapTypeId.ROADMAP
  });

  var markerCollectionView;

  // Food Truck Location Model (model for Backgrid table)
  var TruckLocation = Backbone.Model.extend({

    // Default attributes for the TruckLocation item.
    defaults: function() {
      return {
        truck_name: "Truck name",
        address: "Street address",
        food_items: "Food items"
      };
    }

  });


  // Food Truck Location Collection
  // ---------------

  var TruckLocationsList = Backbone.Collection.extend({

    // Reference to this collection's model.
    model: Backbone.GoogleMaps.Location,

    url: '/food_truck_locations',

    parse: function(response) {
      console.log("Parsing response from server");
      var i;
      for (i = 0; i < response.length; i++) {
          var truckObject = {};
          truckObject["title"] = response[i]["applicant"];
          truckObject["lat"] = response[i]["lat"];
          truckObject["lng"] = response[i]["lng"];
          this.push(truckObject);
      }
      return this.models;
    }

  });

  // Create our global collection of **TruckLocations**.
  var TruckLocations = new TruckLocationsList();

  // Fetch location data from the server
  TruckLocations.fetch({
    success: function(response, xhr) {
      console.log("Inside TruckLocations.fetch success callback");
      var places = new Backbone.GoogleMaps.LocationCollection(
        response.models);

      // Render Markers
      markerCollectionView = new Backbone.GoogleMaps.MarkerCollectionView({
        collection: places,
        map: map
      });

      markerCollectionView.render();
    },
    error: function (errorResponse) {
      console.log(errorResponse);
    }
  });

});

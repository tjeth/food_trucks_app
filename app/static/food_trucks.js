$(document).ready(function() {
  console.log("Inside beginning of food_truck.js");

  /* Google Maps related code */

  // Initialize the map
  var map = new google.maps.Map($('#map-canvas')[0], {
    center: new google.maps.LatLng(37.7833, -122.4167),
    zoom: 12,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  });


  // Handle to the Google Maps marker collection
  var markerCollectionView;


  // Food Truck Location Collection 
  // Populated by data from the server
  var TruckLocationsList = Backbone.Collection.extend({
    // Reference to this collection's model.
    model: Backbone.GoogleMaps.Location,

    url: '/food_truck_locations',

    parse: function(response) {
      console.log("Parsing response from server");
      return parseDataForMap(response);
    }

  });


  // Create our global collection of TruckLocations
  var TruckLocations = new TruckLocationsList();


  // Fetch location data from the server
  TruckLocations.fetch({
    success: function(response, xhr) {
      console.log("Inside TruckLocations.fetch success callback");
      drawPins(response.models);
    },
    error: function (errorResponse) {
      console.log(errorResponse);
    }
  });



  /* Address search related code */

  // View for searching trucks near the specified address
  AddressSearchView = Backbone.View.extend({
    initialize: function(){
      this.render();
    },

    render: function(){
      var template = _.template( $("#address_search_template").html(), {} );
      this.$el.html( template );
    },

    events: {
      "click input[type=button]": "performSearch"
    },

    // Performs search by making a request to the server and then parsing data
    performSearch: function( event ){
      console.log( "Search for " + $("#address_search_input").val() );

      var address = $("#address_search_input").val();
      $.get( "/address_search", { 'address': address }, function( data ) {
        console.log("Inside success of address_search");
        console.log(data);

        // TODO: Make this modular?
        // Do parsing on the server side, take a parameter
        console.log("Parsing response from server");
        var locations = data['results'];
        var truck_list = parseDataForMap(locations);

        var table_truck_list = parseDataForTable(locations);

        var pt = new google.maps.LatLng(data['search_address']['lat'], 
          data['search_address']['lng']);
        map.setCenter(pt);
        map.setZoom(15);

        drawPins(truck_list);

        drawGrid(table_truck_list);
      })
      .fail(function() {
        console.log( "GET request to address_search failed" );
      });
    }
  });

  // Create the address search view
  var address_search_view = new AddressSearchView({ el: $("#address_search_container") });


  // Helper function for drawing pins on the map
  function drawPins(data) {
    var places = new Backbone.GoogleMaps.LocationCollection(data);

    // Delete markers if there were previous markers on the map
    if (markerCollectionView) {
      markerCollectionView.closeChildren();
    }

    // Render Markers
    markerCollectionView = new Backbone.GoogleMaps.MarkerCollectionView({
      collection: places,
      map: map
    });
    markerCollectionView.render();
  }




  /* Data Table (backgrid.js) related code */

  // Handle to grid object
  var grid; 


  // Food Truck Location Model (model for Backgrid table)
  var TruckLocationTable = Backbone.Model.extend({
    defaults: function() {
      return {
        id: "Id",
        truck_name: "Truck name",
        address: "Street address",
        food_items: "Food items"
      };
    }
  });


  // Truck Location Collection (for Backgrid table)
  var TruckLocationsListTable = Backbone.Collection.extend({
    model: TruckLocationTable,

    url: "/food_truck_locations",

    parse: function(response) {
      console.log("Parsing response from server");
      var table_truck_list = parseDataForTable(response);
      return table_truck_list;
    }

  });


  // Create Collection
  var TruckLocationsTable = new TruckLocationsListTable();


  // Create columns for Backgrid table
  var columns = [{
      name: "id", // The key of the model attribute
      label: "ID", 
      editable: false, 
      cell: Backgrid.IntegerCell.extend({
        orderSeparator: ''
      }),
      direction: "descending"
    }, {
      name: "truck_name",
      label: "Truck Name",
      cell: "string", 
      editable: false
    }, {
      name: "address",
      label: "Address",
      cell: "string", 
      editable: false
    }, {
      name: "food_items",
      label: "Food Items",
      cell: "string", 
      editable: false
  }];


  // Fetch some countries from the url
  TruckLocationsTable.fetch({
    reset: true,
    success: function(response, xhr) {
      console.log("Inside TruckLocationsTable.fetch success callback");
      drawGrid(response.models);
    },
    error: function (errorResponse) {
      console.log(errorResponse);
    }
  });


  // Helper function to draw the backgrid grid 
  function drawGrid(data) {
    var table_locations = new TruckLocationsListTable(data);

    if (grid) {
      grid.remove();
    }

    grid = new Backgrid.Grid({
      columns: columns,
      collection: table_locations
    });

    // Render the grid and attach the root to your HTML document
    $("#backgrid_table").append(grid.render().el);
  }




  /* Data parsing helper functions */

  // Helper function for parsing data for use with Google Maps markers
  function parseDataForMap(response) {
    var truck_list = [];

    var i;
    for (i = 0; i < response.length; i++) {
      var truck_object = {};
      truck_object["title"] = response[i]["applicant"];
      truck_object["lat"] = response[i]["lat"];
      truck_object["lng"] = response[i]["lng"];
      truck_list.push(truck_object);
    }

    return truck_list;
  }


  // Helper function for parsing data for use backgrid data table
  function parseDataForTable(response) {
    var table_truck_list = [];

    var i;
    for (i = 0; i < response.length; i++) {
      var table_truck_object = {};
      table_truck_object["id"] = response[i]["id"];
      table_truck_object["truck_name"] = response[i]["applicant"];
      table_truck_object["address"] = response[i]["address"];
      table_truck_object["food_items"] = response[i]["fooditems"];
      table_truck_list.push(table_truck_object);
    }

    // Sort items by id ascending
    table_truck_list.sort(function(a, b){return a['id'] - b['id']});

    return table_truck_list;
  }
});

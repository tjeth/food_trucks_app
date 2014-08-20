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


describe('TruckLocationTable model', function() {

  describe('when instantiated', function() {
    
    it('should exhibit attributes', function() {

      var truck_location_table = new TruckLocationTable({
        id: "123124",
        truck_name: "El Senor",
        address: "400 Valencia, San Francisco",
        food_items: "Mexican food"
      });
      expect(truck_location_table.get('truck_name'))
        .toEqual('El Senor');
    });
    
  });
  
});


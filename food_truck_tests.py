import unittest
import os
import tempfile
import food_trucks_app
import json

class FoodTrucksTestCase(unittest.TestCase):
  def setUp(self):
    self.app = food_trucks_app.app.test_client()

  # Route tests
  def test_index(self):
    rv = self.app.get('/')
    assert 'San Francisco Food Trucks Locator' in rv.data

  def test_address_search(self):
    rv = self.app.get('/address_search?address=2101%2003RD%20ST,%20San%20Francisco')
    assert 'results' in rv.data

  def test_address_search_non_sf_results(self):
    rv = self.app.get('/address_search?address=asdf')
    assert 'Please input a San Francisco address' in rv.data

  def test_address_search_no_results(self):
    rv = self.app.get('/address_search?address=ajsdfl;aksjdfl;akjsd;f')
    assert 'No address search results' in rv.data

  def test_food_truck_locations(self):
    rv = self.app.get('/food_truck_locations')
    assert 'applicant' in rv.data and len(rv.data) != 0


  # Helper function tests
  def test_google_maps_geocode(self):
    rv = food_trucks_app.googleMapsGeocode("625 Bush St.")
    assert 'results' in rv and len(rv) != 0

  def test_haversine(self):
    rv = food_trucks_app.haversine(-122.407606, 37.7900289, -122.4325852, 37.7909516)
    assert 2.1960026881513364 == rv

  def test_data_existence(self):
    f = open('food_truck_data.json')
    data = json.load(f)
    f.close()
    assert len(data) != 0


if __name__ == '__main__':
  unittest.main()
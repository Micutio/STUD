"""
Module for retrieving and displaying the geographic location of the International Space Station.

Requires:
    geopy

Updates:
    18-12-2016: Initial draft of ISS location service as separate class
"""

# TODO: Add timestamp (of local time) to location output, if not above ocean.

import os
import traceback
import time
import requests
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from geopy.exc import GeocoderUnavailable


__author__ = 'Michael Wagner'

cycle_time = 15

class IssLocation:

    def __init__(self):
        self.geolocator = None
        self.iss_lat = None
        self.iss_lon = None
        self.data_dict = None
        self.url = 'http://api.open-notify.org/iss-now.json'

    def init_geolocator(self):
        self.geolocator =  Nominatim()

    def set_iss_loc(self):
        # Get json data with current location of ISS
        # Use additional headers to avoid caching
        headers = {'Cache-Control', 'max-age=0'}
        _buf = requests.get(self.url)
        self.data_dict = _buf.json()
        # print(data_dict)
        self.iss_lat = self.data_dict['iss_position']['latitude']
        self.iss_lon = self.data_dict['iss_position']['longitude']

    def set_iss_loc_alternative(self):
        """
        Alternative method for retrieving.
        Used for debugging a problem with faulty JSON retrieval.
        """
        import urllib.request
        import json
        req = urllib.request.Request(self.url)
        req.add_header('Cache-Control', 'max-age=0')
        with urllib.request.urlopen(req) as response:
            # print(response.info())
            self.data_dict = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
            self.iss_lat = self.data_dict['iss_position']['latitude']
            self.iss_lon = self.data_dict['iss_position']['longitude']

    def get_location_for_coords(self):
        location = self.geolocator.reverse(self.iss_lat + ', ' + self.iss_lon)
        # print(location.raw)
        return location.address

    def start_service(self):
        try:
            while True:
                # TODO: Handle errors when geocoder unavailable
                try:
                    self.set_iss_loc()
                    # self.set_iss_loc_alternative()
                    loc = self.get_location_for_coords()
                    print('ISS location >>> lat: {0}, lon: {1}'.format(self.iss_lat, self.iss_lon))
                    if loc is not None:
                        print('below: {0}'.format(loc))
                except GeocoderTimedOut as e:
                    print('Error: geocoder timeout. Retry in {} sec...'.format(cycle_time))
                    # traceback.print_exc()
                except GeocoderUnavailable as e:
                    print('Error: geocoder unavailable. Retry in {} sec...'.format(cycle_time))
                except OSError as e:
                    print('Error: network connection interrupt. Retry in {} sec...'.format(cycle_time))
                time.sleep(cycle_time)
        except KeyboardInterrupt:
            print("\n")
            print("terminating service")

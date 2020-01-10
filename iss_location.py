"""
Module for retrieving and displaying the geographic location of the International Space Station.

Requires:
    geopy

Updates:
    18-12-2016: Initial draft of ISS location service as separate class
"""

# TODO: Add timestamp (of local time) to location output, if not above ocean.

import os
import sys
import traceback
import time
import requests
from collections import defaultdict
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
        self.geolocator = Nominatim()

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
            self.data_dict = json.loads(response.read().decode(
                response.info().get_param('charset') or 'utf-8'))
            self.iss_lat = self.data_dict['iss_position']['latitude']
            self.iss_lon = self.data_dict['iss_position']['longitude']

    def get_location_for_coords(self):
        location = self.geolocator.reverse(self.iss_lat + ', ' + self.iss_lon)
        # print(location.raw)
        return location.address

    def run_service(self):
        try:
            err_printer = ErrorPrinter()
            while True:
                try:
                    self.set_iss_loc()
                    # self.set_iss_loc_alternative()
                    loc = self.get_location_for_coords()
                    err_printer.reset()
                    print('ISS location >>> lat: {0}, lon: {1}'.format(
                        self.iss_lat, self.iss_lon))
                    if loc is not None:
                        print('             >>> {0}'.format(loc))
                except GeocoderTimedOut as e:
                    err_printer.handle('network timeout')
                except GeocoderUnavailable as e:
                    err_printer.handle('network unavailable')
                except OSError as e:
                    err_printer.handle('connection interrupt')
                time.sleep(cycle_time)
        except KeyboardInterrupt:
            print("\n")
            print("terminating service")


class ErrorPrinter:

    def __init__(self):
        self.errs = defaultdict(int)
        self.blank = " " * 80

    def reset(self):
        if len(self.errs) > 0:
            print()
        self.errs.clear()

    def handle(self, reason):
        sys.stdout.write('\r' + self.blank)

        self.errs[reason] += 1
        if len(self.errs) == 1:
            count = self.errs[reason]
            if count <= 1:
                sys.stdout.write(
                    '\r       Error >>> {0}. Retry in {1} sec...'.format(reason, cycle_time))
            else:
                sys.stdout.write('\r       Error >>> {0} (x{1}). Retry in {2} sec...'.format(
                    reason, count, cycle_time))
        else:
            sys.stdout.write(
                '\r       Error >>> Multiple issues. Retry in {} sec...'.format(cycle_time))
        sys.stdout.flush()

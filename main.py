"""
Main module of S.T.U.D.
This application continually displays live telemetry from space.
Updates:
    16-12-16: Display location of ISS (lat, lon)
"""

import json
import urllib
import time
from geopy.geocoders import Nominatim

__author__ = 'Michael Wagner'


def startup():
    print('>>> S.T.U.D. - Space Telemetry')


def get_iss_loc():
    # Get json data with current location of ISS
    url = 'http://api.open-notify.org/iss-now.json'
    data = urllib.request.urlopen(url).read().decode()
    data_dict = json.loads(data)
    # print(data_dict)
    return data_dict['iss_position']['latitude'], data_dict['iss_position']['longitude']


def get_location_for_coords(lat, lon):
    geolocator = Nominatim()
    location = geolocator.reverse(lat + ', ' + lon)
    # print(location.raw)
    return location.address


if __name__ == '__main__':
    startup()
    while True:
        iss_lat, iss_lon = get_iss_loc()
        iss_add = get_location_for_coords(iss_lat, iss_lon)
        output = 'ISS location >>> Lat: {0}, Lon: {1}\n'\
                 'approximate to {2}'.format(iss_lat, iss_lon, iss_add)
        print(output)
        time.sleep(30)

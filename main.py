"""
Main module of S.T.U.D.
This application continually displays live telemetry from space.
Updates:
    16-12-16: Display location of ISS (lat, lon)
"""

import json
import urllib
import time
import traceback
from geopy.geocoders import Nominatim

__author__ = 'Michael Wagner'


def startup():
    print('>>> S.T.U.D. - Space Telemetry')

def init_geolocator():
    return Nominatim()

def get_iss_loc():
    # Get json data with current location of ISS
    url = 'http://api.open-notify.org/iss-now.json'
    data = urllib.request.urlopen(url).read().decode()
    data_dict = json.loads(data)
    # print(data_dict)
    return data_dict['iss_position']['latitude'], data_dict['iss_position']['longitude']


def get_location_for_coords(lat, lon, geolocator):
    location = geolocator.reverse(lat + ', ' + lon)
    # print(location.raw)
    return location.address


if __name__ == '__main__':
    startup()
    geolocator = init_geolocator()
    while True:
        try:
            # TODO: handle errors when geocoder unavailable
            iss_lat, iss_lon = get_iss_loc()
            iss_add = get_location_for_coords(iss_lat, iss_lon, geolocator)
            
            # TODO: Only print the second line when iss_add not None!
            print('ISS location >>> Lat: {0}, Lon: {1}'.format(iss_lat, iss_lon))
            if iss_add is not None:
                print('above: {0}'.format(iss_add))

        except:
            print('Error: Service currently unavailable. Trying again later')
            traceback.print_exc()
        time.sleep(30)

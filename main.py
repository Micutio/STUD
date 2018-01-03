"""
Main module of S.T.U.D.
This application continually displays live telemetry from space.
Updates:
    16-12-16: Display location of ISS (lat, lon)
"""

from iss_location import IssLocation

__author__ = 'Michael Wagner'


def startup():
    print('S.T.U.D. - Space Telemetry Utility Display')


if __name__ == '__main__':
    startup()

    # Start the only service we have right now.
    issLoc = IssLocation()
    issLoc.init_geolocator()
    issLoc.start_service()

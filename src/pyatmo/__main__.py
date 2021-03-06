from .auth import ClientAuth
from .camera import CameraData
from .exceptions import NoDevice
from .public_data import PublicData
from .thermostat import HomeData
from .weather_station import WeatherStationData


def main():
    import sys

    try:
        import os

        if (
            os.environ["CLIENT_ID"]
            and os.environ["CLIENT_SECRET"]
            and os.environ["USERNAME"]
            and os.environ["PASSWORD"]
        ):
            CLIENT_ID = os.environ["CLIENT_ID"]
            CLIENT_SECRET = os.environ["CLIENT_SECRET"]
            USERNAME = os.environ["USERNAME"]
            PASSWORD = os.environ["PASSWORD"]
    except KeyError:
        sys.stderr.write(
            "No credentials passed to pyatmo.py (client_id, client_secret, username, password)\n"
        )
        sys.exit(1)

    authorization = ClientAuth(
        clientId=CLIENT_ID,
        clientSecret=CLIENT_SECRET,
        username=USERNAME,
        password=PASSWORD,
        scope=(
            "read_station read_camera access_camera read_thermostat "
            "write_thermostat read_presence access_presence read_homecoach "
            "read_smokedetector"
        ),
    )

    try:
        WeatherStationData(authorization)
    except NoDevice:
        if sys.stdout.isatty():
            print("pyatmo.py : warning, no weather station available for testing")

    try:
        CameraData(authorization)
    except NoDevice:
        if sys.stdout.isatty():
            print("pyatmo.py : warning, no camera available for testing")

    try:
        HomeData(authorization)
    except NoDevice:
        if sys.stdout.isatty():
            print("pyatmo.py : warning, no thermostat available for testing")

    PublicData(authorization)

    # If we reach this line, all is OK

    # If launched interactively, display OK message
    if sys.stdout.isatty():
        print("pyatmo: OK")

    sys.exit(0)


if __name__ == "__main__":
    main()

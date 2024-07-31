from json import dumps
from numpy import arange
from random import choice
from time import sleep

import paho.mqtt.client as mqtt


def _create_connection():
    client = mqtt.Client()
    client.connect("172.28.42.208", 1883)
    client.loop_start()
    return client


def main():
    client = _create_connection()

    batts = list(range(89, 102))
    temps = list(range(19, 32))
    humids = list(range(29, 42))
    secs = list(arange(0.4, 1.5, 0.2))
    stations = ['A', 'B', 'C']

    try:
        while True:
            iot_data = {
                'BAT': choice(batts),
                'TEMP': choice(temps),
                'HUMID': choice(humids),
            }

            station = choice(stations)
            client.publish('UPB/' + station, dumps(iot_data))
            print(f'Station {station} published:\n{dumps(iot_data, indent=4)}\n')

            sleep(choice(secs))

    except KeyboardInterrupt:
        print("Exiting gracefully due to KeyboardInterrupt.")
    except Exception as e:
        # Log other exceptions
        print(f"Error in main loop: {str(e)}")

    finally:
        client.disconnect()
        client.loop_stop()


if __name__ == "__main__":
    main()

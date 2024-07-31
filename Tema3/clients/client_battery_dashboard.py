from json import dumps
from numpy import arange
from random import choice
from time import sleep

import paho.mqtt.client as mqtt


def _create_connection():
    try:
        client = mqtt.Client()
        client.connect("172.28.42.208", 1883)
        client.loop_start()
        return client
    except Exception as e:
        print(f"Error creating MQTT connection: {str(e)}")
        raise

def main():
    try:
        client = _create_connection()

        batts = list(range(89, 102))
        hums = list(range(19, 32))
        tcs = list(range(29, 42))
        secs = list(arange(0.4, 1.7, 0.2))
        stations = ['Gas', 'Mongo']

        while True:
            iot_data = {
                'BAT': choice(batts),
                'HUM': choice(hums),
                'TC': choice(tcs),
            }

            station = choice(stations)
            client.publish('UPB/' + station, dumps(iot_data))
            print(f'Station {station} published:\n{dumps(iot_data, indent=4)}\n')

            sleep(choice(secs))

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("Exiting gracefully due to KeyboardInterrupt.")
    except Exception as e:
        # Log other exceptions
        print(f"Error in main loop: {str(e)}")

    finally:
        client.disconnect()
        client.loop_stop()


if __name__ == "__main__":
    main()

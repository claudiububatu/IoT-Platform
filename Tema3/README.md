@COPYRIGHTS: Bubatu Claudiu-Mihai, 343C5
-----------------------------------------------------------------------------

						Homework 3 - Microservices


## Running

Firstly, we have to run the command docker swarm init if we haven`t
initialized it yet.

To create the server image (the only component of the application that is not
an image from hub.docker.com) and run the application, you can use the run.sh
script. After the server image has been created, the application can be
started with the command docker stack deploy -c stack.yml sprc3.
The application can be stopped using the command docker stack rm sprc3.


## Structure
The application contains the 4 components specified in the statement:

- eclipse-mosquitto broker
- arbitrator implemented in the src/server.py file
- InfluxDB database
- database visualization utility, Grafana

## Broker
I used the eclipse-mosquitto image because I was already familiar with it
from the MQTT lab. The broker exposes port 1883.

## Arbitrator
It is both a client of the broker and a server for the database. It subscribes
to all broker topics (#), retrieves messages sent by clients, and inserts them
into the database. 

## Data Persistence
I had to mount 2 local volumes for the Grafana and InfluxDB services. Therefore,
when the command docker stack rm sprc3 is run, and later,
docker stack deploy -c stack.yml sprc3, the previously entered data will be preserved.

## Grafana
The dashboards are configured in the grafana-provisioning folder.
Login credentials are specified in the stack.yml`s environment field.

## Testing
To test the application through the dashboards provided by Grafana, you can use
the client defined in clients/test_client.py. It adds the metrics BAT, HUM,
and TEMP from the location "UPB" with random values from an interval for each
metric. The stations are also random values from the set {"A", "B", "C"}.

## Bibliography
[1] https://hub.docker.com/
[2] https://www.youtube.com/watch?v=QGG_76OmRnA&t=51s
[3] https://www.youtube.com/watch?v=0CpHwszFjUY
[4] https://www.youtube.com/watch?v=NGv7LeCaPtc
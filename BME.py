from bme280 import BME280
from smbus import SMBus
from ISSStreamer.Streamer import Streamer
import time
import sys

# --------- User Settings ---------
BUCKET_NAME = "BME280"
BUCKET_KEY = "6HEACAJWCQNW"
ACCESS_KEY = "ist_cE0zFD5C1Y5DSKWsSGxIBcTRIOVqPO_x"
MINUTES_BETWEEN_SENSEHAT_READS = 0.1
# ---------------------------------

streamer = Streamer(bucket_name=BUCKET_NAME, bucket_key=BUCKET_KEY, access_key=ACCESS_KEY)

bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)

while True:

	# Read sensors
	temp_c = bme280.get_temperature()
	humidity = bme280.get_humidity()
	pressure_mb = bme280.get_pressure()
	
	#Format data
	pressure_in = 0.03937008*(pressure_mb)
	pressure_in = float("{0:.2f}".format(pressure_in))
	humidity = float("{0:.2f}".format(humidity))
	
	#Stream data
	streamer.log("Temperature " +  "(C): ", temp_c)
	streamer.log("Humidity " + "%: ", humidity)
	streamer.log("Pressure "+"(IN) ", pressure_in)
	
	streamer.flush()
	time.sleep(60*MINUTES_BETWEEN_SENSEHAT_READS)
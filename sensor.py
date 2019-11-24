from bme280 import BME280
from smbus import SMBus
from ISStreamer.Streamer import Streamer
import time
import sys
from pms5003 import PMS5003

# --------- User Settings ---------
BUCKET_NAME = "BME280"
BUCKET_KEY = "6HEACAJWCQNW"
ACCESS_KEY = "ist_cE0zFD5C1Y5DSKWsSGxIBcTRIOVqPO_x"
# ---------------------------------

streamer = Streamer(bucket_name=BUCKET_NAME, bucket_key=BUCKET_KEY, access_key=ACCESS_KEY)

bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)
pms5003 = PMS5003()

while True:

	# Read sensors
	temp_c = bme280.get_temperature()
	humidity = bme280.get_humidity()
	pressure_mb = bme280.get_pressure()
	readings = pms5003.read()
	
	#Format data
	pressure_in = 0.03937008*(pressure_mb)
	pressure_in = float("{0:.2f}".format(pressure_in))
	humidity = float("{0:.2f}".format(humidity))
	pm1 = (readings.pm_ug_per_m3(1.0))
	pm25 = (readings.pm_ug_per_m3(2.5))
	pm10 = (readings.pm_ug_per_m3(10))
	
	#Stream data
	streamer.log("Temperature " +  "(C): ", temp_c)
	streamer.log("Humidity " + "%: ", humidity)
	streamer.log("Pressure "+"(IN) ", pressure_in)
	streamer.log("PM1.0 "+ "(ug/m3 ", pm1)
	streamer.log("PM2.5 "+ "(ug/m3 ", pm25)
	streamer.log("PM10.0 "+ "(ug/m3 ", pm10)
	
	streamer.flush()
	time.sleep(1)
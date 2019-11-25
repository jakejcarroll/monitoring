from bme280 import BME280
from smbus import SMBus
from ISStreamer.Streamer import Streamer
import time
import sys
from pms5003 import PMS5003
from enviroplus import gas
from subprocess import PIPE, Popen, check_output

# --------- User Settings ---------
BUCKET_NAME = "BME280"
BUCKET_KEY = "6HEACAJWCQNW"
ACCESS_KEY = "ist_cE0zFD5C1Y5DSKWsSGxIBcTRIOVqPO_x"
# ---------------------------------

streamer = Streamer(bucket_name=BUCKET_NAME, bucket_key=BUCKET_KEY, access_key=ACCESS_KEY)

bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)
pms5003 = PMS5003()

    # Get CPU temperature to use for compensation
def get_cpu_temperature():
	process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE, universal_newlines=True)
	output, _error = process.communicate()
	output = output.decode()
	return float(output[output.index('=') + 1:output.rindex("'")])

	

while True:

	cpu_temp = get_cpu_temperature()
	factor = 1
	cpu_temps = [get_cpu_temperature()] * 5

	# Read sensors
	temp = bme280.get_temperature()
	humidity = bme280.get_humidity()
	pressure_mb = bme280.get_pressure()
	readings = pms5003.read()
	readings_gas = gas.read_all()
	
	# Get the temperature of the CPU for compensation
	#def get_cpu_temperature():
    	#with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
        	#temp = f.read()
       	 	#temp = int(temp) / 1000.0
  	  		#return temp
    
    # Tuning factor for compensation. Decrease this number to adjust the
	# temperature down, and increase to adjust up
	
	#factor = 0.8

	#cpu_temps = [get_cpu_temperature()] * 5
	
	#Format data
	pressure_in = 0.03937008*(pressure_mb)
	pressure_in = float("{0:.2f}".format(pressure_in))
	humidity = float("{0:.2f}".format(humidity))
	temp_c = float("{0:.1f}".format(temp))
	pm1 = (readings.pm_ug_per_m3(1.0))
	pm25 = (readings.pm_ug_per_m3(2.5))
	pm10 = (readings.pm_ug_per_m3(10))
	gas_reducing = (readings_gas.reducing)
	gas_oxidising = (readings_gas.oxidising)
	gas_nh3 = (readings_gas.nh3)
	
    
    #Smooth out with some averaging to decrease jitter
	cpu_temps = cpu_temps[1:] + [cpu_temp]
	avg_cpu_temp = sum(cpu_temps) / float(len(cpu_temps))
	raw_temp = bme280.get_temperature()
	comp_temp = raw_temp - ((avg_cpu_temp - raw_temp) / factor)
	comp_temp = float("{0:.1f}".format(comp_temp))
	
	
	#Stream data
	streamer.log("Temperature " +  "(C): ", temp_c)
	streamer.log("Compensated Temperature " +  "(C): ", comp_temp)
	streamer.log("Humidity " + "%: ", humidity)
	streamer.log("Pressure "+"(IN) ", pressure_in)
	streamer.log("PM1.0 "+ "(ug/m3) ", pm1)
	streamer.log("PM2.5 "+ "(ug/m3) ", pm25)
	streamer.log("PM10.0 "+ "(ug/m3) ", pm10)
	streamer.log("Oxidising Gas", gas_oxidising)
	streamer.log("Reducing Gas", gas_reducing)
	streamer.log("NH3 Gas", gas_nh3)
	
	streamer.flush()
	time.sleep(1)
from prometheus_client import start_http_server, Summary, Gauge
import configparser
import os
import time
import sys
import nest


# Gauges
g = {
  'is_online': Gauge('nest_thermostat_is_online', 'Device connection status with the Nest service', ['structure', 'device']),
  'has_leaf': Gauge('nest_thermostat_has_leaf', 'Displayed when the thermostat is set to an energy-saving temperature', ['structure', 'device']),
  'target_temp': Gauge('nest_thermostat_target_temp', 'Desired temperature, in half degrees Celsius (0.5°C)', ['structure', 'device']),
  'current_temp': Gauge('nest_thermostat_current_temp', 'Temperature, measured at the device, in half degrees Celsius (0.5°C)', ['structure', 'device']),
  'humidity': Gauge('nest_thermostat_humidity', 'Humidity, in percent (%) format, measured at the device, rounded to the nearest 5%', ['structure', 'device']),
  'state': Gauge('nest_thermostat_state', 'Indicates whether HVAC system is actively heating, cooling or is off. Use this value to indicate HVAC activity state', ['structure', 'device']),
  'mode': Gauge('nest_thermostat_mode', 'Indicates HVAC system heating/cooling modes, like Heat•Cool for systems with heating and cooling capacity, or Eco Temperatures for energy savings', ['structure', 'device']),
  'time_to_target': Gauge('nest_thermostat_time_to_target', 'The time, in minutes, that it will take for the structure to reach the target temperature', ['structure', 'device']),
  
}

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
# Decorate function with metric.
@REQUEST_TIME.time()
def polling(napi):
    print("%s - Polling!" % time.time())

    for structure in napi.structures:
        for device in structure.thermostats:
            g['is_online'].labels(structure.name, device.name).set(device.online)
            g['has_leaf'].labels(structure.name, device.name).set(device.has_leaf)
            g['target_temp'].labels(structure.name, device.name).set(device.target)
            g['current_temp'].labels(structure.name, device.name).set(device.temperature)
            g['humidity'].labels(structure.name, device.name).set(device.humidity)
            g['state'].labels(structure.name, device.name).set((0 if device.hvac_state == "off" else 1))
            g['mode'].labels(structure.name, device.name).set((0 if device.mode == "off" else 1))
            g['time_to_target'].labels(structure.name, device.name).set(''.join(x for x in device.time_to_target if x.isdigit()))


if __name__ == '__main__':
    c = configparser.ConfigParser()
    c.read(os.path.join(os.path.abspath(os.path.dirname(__file__)),'settings.ini'))

    # Setup Nest account
    start_time = time.time()

    napi = nest.Nest(client_id=c['nest']['client_id'], client_secret=c['nest']['client_secret'], access_token_cache_file=os.path.join(os.path.abspath(os.path.dirname(__file__)),c['nest']['access_token_cache_file']))
    
    resp_time = time.time() - start_time
    sys.stderr.write("Nest API: %0.3fs\n" % resp_time)

    if napi.authorization_required:
      print("Go to " + napi.authorize_url + " to authorize, then enter PIN below")
      if sys.version_info[0] < 3:
        pin = raw_input("PIN: ")
      else:
        pin = input("PIN: ")
      napi.request_token(pin)

    # Start up the server to expose the metrics.
    listen_port = c['general']['port']
    start_http_server(int(listen_port))
    sys.stdout.write("Listening on port " + listen_port + "...\n")
    
    while True:
        polling(napi)
        time.sleep(int(c['general']['polling_interval']))

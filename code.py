import ipaddress
import ssl
import wifi
import socketpool
import adafruit_requests
import time
from adafruit_magtag.magtag import MagTag
import adafruit_minimqtt.adafruit_minimqtt as MQTT
from secrets import secrets
# URLs to fetch from
magtag = MagTag(

)
HA_STATES_ENDPOINT_ROOT = "http://YOUR_HA_IP:8123/api/states/"
MQTT_SERVER = "YOUR_MQTT_SERVER"
MQTT_PORT=1883
BATT_MQTT_TOPIC = secrets["BATT_MQTT_TOPIC"]
TIME_BETWEEN_REFRESHES_SEC = secrets["TIME_BETWEEN_REFRESHES_SEC"] # 1200 sec = 20min / 300 sec = 5 min

use_live = True #Live means we load via APIs, not live means we mock data (wifi errors).

errorstring = ""
wifi_channel = "66"
wifi_rssi = "-99"
location = secrets.get("timezone", None)
TIME_URL = "https://io.adafruit.com/api/v2/%s/integrations/time/strftime?x-aio-key=%s&tz=%s" % (secrets["aio_username"], secrets["aio_key"], location)
TIME_URL += "&fmt=%25Y-%25m-%25d+%25H%3A%25M%3A%25S.%25L+%25j+%25u+%25z+%25Z"

headers = { "Authorization": "Bearer " + secrets["ha_api_token"]};
batt = "%s" % round(float(magtag.peripherals.battery),1)
if use_live:
  try:
    wifi.radio.connect(ssid= secrets["ssid"],
                       password=secrets["password"],
                       channel=secrets["wifi_channel_force"],
    )   
    pool = socketpool.SocketPool(wifi.radio)
    wifi_rssi = wifi.radio.ap_info.rssi
    wifi_channel = wifi.radio.ap_info.channel 
    requests = adafruit_requests.Session(pool, ssl.create_default_context())

    response          = requests.get(HA_STATES_ENDPOINT_ROOT + "sensor.netatmo_outdoor",headers=headers)
    outdoor_temp      = round(float(response.json()["state"]),1)

    response          = requests.get(HA_STATES_ENDPOINT_ROOT + "sensor.netatmo_magamistuba",headers=headers)
    magamistuba_temp  = round(float(response.json()["state"]),1)
  
    response          = requests.get(HA_STATES_ENDPOINT_ROOT + "sensor.netatmo_allkorrus",headers=headers)
    allkorrus_temp    = round(float(response.json()["state"]),1)

    response          = requests.get(HA_STATES_ENDPOINT_ROOT + "sensor.brigitta_tuba_temperature",headers=headers)
    brigittatuba_temp = round(float(response.json()["state"]),1)
 
    response          = requests.get(HA_STATES_ENDPOINT_ROOT + "sensor.tarmo_tuba_temperature",headers=headers)
    kontorituba_temp  = round(float(response.json()["state"]),1)

    response          = requests.get(HA_STATES_ENDPOINT_ROOT + "sensor.power_meter_active_power",headers=headers)
    grid_input_kW        = round(float(response.json()["state"])/1000,1)

    response          = requests.get(HA_STATES_ENDPOINT_ROOT + "sensor.inverter_active_power",headers=headers)
    solar_output_kW        = round(float(response.json()["state"])/1000,1)
    #get time when we updated
    response = requests.get(TIME_URL)
    updated_at = response.text[11:16]
    #updated_at = " "

    #Send battery parameters
    mqtt_client = MQTT.MQTT(
      broker=MQTT_SERVER,
      port=MQTT_PORT,
      #username="",  #do not define if you don't have them, it passes as empty string and resulting in ERRCONNRESET
      #password="",
      socket_pool=pool,
      is_ssl=False,
      #ssl_context=ssl.create_default_context(),
    )


    mqtt_client.connect()
    mqtt_client.publish(BATT_MQTT_TOPIC, batt, True) #Retain to True
    mqtt_client.disconnect() 


  #except ConnectionError:
  #  magtag.exit_and_deep_sleep(5) #retry
  except Exception as e:
    est = str(e)
    #print(" ", est)
    magtag.set_text(est, 0, True); #Refresh screen with last
    magtag.exit_and_deep_sleep(15) #retry
  
else:
  outdoor_temp = round(float("-5"),1)
  magamistuba_temp = round(float("21.29"),1)
  allkorrus_temp = round(float("23.55"),1)
  brigittatuba_temp = round(float("21.22"),1)
  kontorituba_temp = round(float("19.54"),1)
  grid_input_kW      = round(float("-2725")/1000,1)
  solar_output_kW    = round(float("1500")/1000,1)
  ha_last_update = "2016-05-30T21:50:30.529465+00:00"
  updated_at = ha_last_update[11:16] # string from 11 to 16

# ÕUES
magtag.add_text(
    #text_font="/fonts/epilogue18.bdf",
    text_position=(10, 15), text_scale=2,
) 
magtag.set_text("Oues:          " + str(outdoor_temp) + " C", 0, False);

# ALLKORRUS
magtag.add_text(
    #text_font="/fonts/epilogue18.bdf",
    text_position=(10, 35), text_scale=2,
) 
magtag.set_text("Allkorrus:     " + str(allkorrus_temp) + " C", 1, False); 

# MAGAMISTUBA
magtag.add_text(
    #text_font="/fonts/epilogue18.bdf",
    text_position=(10, 55), text_scale=2,
) 
magtag.set_text("Magamistuba:   " + str(magamistuba_temp) + " C", 2, False); 

# Brigitta tuba
magtag.add_text(
    #text_font="/fonts/epilogue18.bdf",
    text_position=(10, 75), text_scale=2,
) 
magtag.set_text("Brigitta tuba: " + str(brigittatuba_temp) + " C", 3, False); 

# Kontor
magtag.add_text(
    #text_font="/fonts/epilogue18.bdf",
    text_position=(10, 95), text_scale=2,
) 
magtag.set_text("Kontorituba:   " + str(kontorituba_temp) + " C", 4, False); #Refresh screen with last

# Kontor
magtag.add_text(
    #text_font="/fonts/epilogue18.bdf",
    text_position=(10, 115), text_scale=2,
) 
magtag.set_text("" + str(grid_input_kW) + " | " + str(solar_output_kW) + " kW", 5, False); #Refresh screen with last



# Last updated and batt
magtag.add_text(
    #text_font="/fonts/epilogue18.bdf",
    text_position=(190, 118), text_scale=1,
) 
magtag.set_text(updated_at +" "+ batt + "V " + str(wifi_rssi) + " " + str(wifi_channel), 6, True); #Refresh screen with last

magtag.exit_and_deep_sleep(TIME_BETWEEN_REFRESHES_SEC)
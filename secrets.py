# SPDX-FileCopyrightText: 2020 Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

# This file is where you keep secret settings, passwords, and tokens!
# If you put them in the code you risk committing that info or sharing it

secrets = {
    'ssid' : 'your ssid', 
    'password' : 'your wifi password',
    'wifi_channel_force' : 0 ,  #0 for no force
    'aio_username' : 'your adafruit user',
    'aio_key' : 'your adafruit key',
    'timezone' : "Europe/Tallinn", # http://worldtimeapi.org/timezones
    'ha_api_token' : "your HA token",
    'BATT_MQTT_TOPIC' : "your desired token", # esp32-magtag-1/battery_voltage
    'TIME_BETWEEN_REFRESHES_SEC' : 1200
    }
 
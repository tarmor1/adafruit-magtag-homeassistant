# adafruit-magtag-homeassistant

Hi!

This repo serves as an example and an easy possible way on how to populate data from Home Assistant to Adafruit's cool MagTag e-ink screen and as an example to send data back via MQTT to Home Assistant.
MagTag is a really cool gadget to your smart home.

The product https://learn.adafruit.com/adafruit-magtag

It has quite nice graphic capabilities, so what you see here is the most basic of everything.

It's convenient to load data in from Home Assistant REST API's - see the manual from https://developers.home-assistant.io/docs/api/rest/

1. Set up your magtag and load libraries from any of the example projects on Adafruits site: 
* install CircuitPython: https://learn.adafruit.com/adafruit-magtag/circuitpython
* take libraries from:  https://circuitpython.org/libraries

2. change your secrets.py accordingly
3. set your Home Assistant IP address and MQTT server IP's in code.py (or remove the MQTT part altogether)

4. Change all the entities you load accordingly.

This repo here serves as an example how to get data out as it took me some time to figure it out.
Some comments and apologies in advance:
* the code and values variable names are in Estonian.
* what it does is loading in a bunch of temperature sensors from HA plus power meter and PV panels current power
* MQTT is for loading back to HA data about battery voltage for Home Assistant logging.
* The code is truly not formatted and has excessivities in it. If you have multiple Magtags, it'll make sense to store unit-specific values to secrets.py and upload/change only code.py
* I have had my fair share of time messing with "no network with that SSID" error. Some notes on that in: https://github.com/adafruit/circuitpython/issues/7260
* if connecting to unsecured MQTT server, make sure your username and password are not set(null), not empty strings. I found it out the hard way.
* As for my case and based on the Wifi issues, I have debug info printed on lower right corner - namely wifi rssid and channel. As well the timestamp for screen population. For the same wifi reason the variable `use_live` is either to mock data or actually load it.
* I'm refreshing it every 20 minutes (see the constant set in secrets.py).
* As I know the only way to get rid of the small power-on LED from the back side is to unsolder it.


... And you should have it as:
![This is an image](https://github.com/tarmor1/adafruit-magtag-homeassistant/blob/main/my-magtag.jpg?raw=true)

Thanks goes to the Adafruit site for extensive help material and @cjoh for his code:
https://gist.github.com/cjoh/18d35063af7010a45599de58a63842bd

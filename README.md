Visual Traceroute
------------------
Description:
A GUI traceroute program visualizing the path packets take from a device to a website using a geomap. The backend performs the traceroute and geolocation in python, while the frontend displays results in an interactive map in html.


Dependencies:
1. Npcap - Packet capture library for Windows ()
2. GeoIP2 - MaxMind's GeoIP2 Python API, for IP address geolocation
3. MaxMind DB Reader - Reader for MaxMind's Geo database
4. webview - Webview library to render GUI
5. Scapy - Crafts and sends packets for traceroute
6. Flask - Web app framework, for GUI and handling requests
7. Flask-CORS - Flask extension for to allow communication between frontend and backend


Installation:
Npcap needs to be installed manually from www.npcap.com

pip install geoip2
pip install scapy
pip install Flask
pip install Flask-CORS
pip install pywebview


Usage:
Run from IDE or execute this command in terminal: python vizTrace.py

Make sure 'GeoLite2-City.mmdb' database file is in the same folder as vizTrace.py

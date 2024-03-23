import scapy # for packet manipulation
from flask import Flask, render_template, request, jsonify # for web app
from flask_cors import CORS # for resource sharing
from scapy.layers.inet import IP, ICMP # for IP and ICMP packets
from scapy.sendrecv import sr1 # for sending packets
import geoip2.database # database to look up geographic info
import threading # threading for flask app to run in separate thread
import webview # to open page in window rather than browser


app = Flask(__name__) # initialize flask app
CORS(app) # apply CORS settings to flask app

geo_db = geoip2.database.Reader('./GeoLite2-City.mmdb') # load GeoLite2 City database
def perform_traceroute(target): # function for traceroute
    result = [] # initialize list of results
    for i in range(1, 30):  # initialize loop for hop limit)
        pkt = IP(dst=target, ttl=i) / ICMP() # create packet with current TTL
        reply = sr1(pkt, verbose=0, timeout=1) # send packet and wait for reply
        if reply is None: # if no reply then state so
            print(f"TTL {i}: No reply")
            result.append({'ip': None, 'ttl': i})
        else:
            print(f"TTL {i}: Reply from {reply.src}") # if there is a reply then log it
            response = None
            try:
                response = geo_db.city(reply.src) # get geographic info
            except geoip2.errors.AddressNotFoundError:
                pass  # if no info found

            geo_info = { # geographic info pull for markers on map
                'ip': reply.src,
                'ttl': i,
                'latitude': response.location.latitude if response else None,
                'longitude': response.location.longitude if response else None,
                'city': response.city.name if response and response.city.name else '',
                'state': response.subdivisions.most_specific.name if response and response.subdivisions.most_specific.name else '',
                'country': response.country.name if response and response.country.name else ''
            }
            result.append(geo_info) # add info to list of results

            if reply.type == 0:  # checks if destination IP is reached
                break
    return result

@app.route('/') # define flask route for index page then serve it
def index():
    return render_template('pg.html')

@app.route('/trace', methods=['POST']) # define flask route for traceroute
def trace_route():
    data = request.json # get request data
    target = data['target'] # extract target from request
    trace_result = perform_traceroute(target) # perform traceroute to the target
    return jsonify(trace_result) # return results in JSON

def run_flask_app(): # function to run flask app without reload
    app.run(debug=False, use_reloader=False)

if __name__ == '__main__':
    t = threading.Thread(target=run_flask_app) # start flask server in separate thread
    t.daemon = True # mark thread as daemon so it exits with main thread
    t.start() # start thread

    webview.create_window('Visual Traceroute', 'http://127.0.0.1:5000', width=1024, height=680)
    webview.start() # open webview pointing to flask app and starts the GUI
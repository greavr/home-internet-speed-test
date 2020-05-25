from flask import Flask, render_template, flash, request, redirect, jsonify
import socket
import logging
import sys
import my_db

# Flask Magic
app = Flask(__name__)
ip = ""
hostname = ""

# Get Primary IP
def set_ip():
    global ip
    global hostname
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.10.10.10', 1))
        print (s.getsockname())
        ip = s.getsockname()[2]
    except:
        print ("Default")
        ip = '127.0.0.1'
    finally:
        s.close()
    hostname = socket.gethostname()


#Wifi Config
@app.route("/wifi", methods=['GET', 'POST'])
def wifisetup():
    global ip
    global hostname
    return render_template('wifi.html',ip_address=ip)

#Ping List
@app.route("/ping_list", methods=['GET'])
def ping_table():
    # Function to return all ping lists
    result_set = my_db.AllPings()
    print (result_set)
    return render_template('ping_list.html', result_set = result_set, this_hostname=hostname)

#Home Page
@app.route("/", methods=['GET', 'POST'])
def default():
    global ip
    global hostname
    return render_template('index.html',ip_address=ip, this_hostname=hostname)

@app.route("/latest", methods=['GET'])
def getResult():
    # Get latest data from speed.db
    setResults = list(my_db.GetLatestPing()[0])
    # Create array
    ping_result = {}
    ping_result["id"] = setResults[0]
    ping_result["time_stamp"]  = setResults[1]
    ping_result["ping"]  = setResults[2]
    return jsonify(ping_result)


if __name__ == "__main__":
    #Get global IP
    set_ip()

    app.run(host='0.0.0.0', port=80)
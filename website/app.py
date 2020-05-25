from flask import Flask, render_template, flash, request, redirect
import socket
import logging
import sys

# Get Primary IP
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


# Flask Magic
app = Flask(__name__)
ip = ""
hostname = ""

#Wifi Config
@app.route("/wifi", methods=['GET', 'POST'])
def wifisetup():
    return render_template('wifi.html',ip_address=ip)


#Home Page
@app.route("/", methods=['GET', 'POST'])
def default():
    return render_template('index.html',ip_address=ip)



if __name__ == "__main__":
    #Get global IP
    ip = get_ip()
    hostname = socket.gethostname()
    print ("Running on this private IP: " + ip)
    print ("Running on this Host: " + hostname)

    app.run(host='0.0.0.0', port=80)
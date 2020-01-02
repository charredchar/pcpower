import time, syslog, uuid
import RPi.GPIO as GPIO
from flask import Flask, render_template, request
app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

# Create a dictionary called pins to store the pin number, name, and pin state:
switchpins = {
   0 : {'name' : 'Blackbox - Power', 'state' : GPIO.HIGH},
   1 : {'name' : 'Blackbox - Reset', 'state' : GPIO.HIGH},
   3 : {'name' : 'KH-PrimeRadiant - Power', 'state' : GPIO.HIGH},
   4 : {'name' : 'KH-PrimeRadiant - Reset', 'state' : GPIO.HIGH},
   }

# Set each pin as an output and make it HIGH:
for pin in switchpins:
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, GPIO.HIGH)
   
@app.route("/")
def main():
   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in switchpins:
      switchpins[pin]['state'] = GPIO.input(pin)
   # Put the pin dictionary into the template data dictionary:
   templateData = {
      'switchpins' : switchpins
      }
   # Pass the template data into the template main.html and return it to the user
   return render_template('main.html', **templateData)

# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<changePin>/<action>")
def action(changePin, action):
   # Convert the pin from the URL into an integer:
   changePin = int(changePin)
   # Get the device name for the pin being changed:
   deviceName = switchpins[changePin]['name']
   # If the action part of the URL is "on," execute the code indented below:
   if action == "on":
      # Set the pin low:
      GPIO.output(changePin, GPIO.LOW)
      time.sleep(0.2)
      GPIO.output(changePin, GPIO.HIGH)
      # Save the status message to be passed into the template:
      message = "Turned " + deviceName + " on."
   if action == "off":
      GPIO.output(changePin, GPIO.LOW)
      time.sleep(0.2)
      GPIO.output(changePin, GPIO.HIGH)
      message = "Turned " + deviceName + " off."

   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in switchpins:
      switchpins[pin]['state'] = GPIO.output(pin)

   # Along with the pin dictionary, put the message into the template data dictionary:
   templateData = {
      'switchpins' : switchpins
   }

   return render_template('main.html', **templateData)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)

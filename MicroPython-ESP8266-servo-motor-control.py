import socket
import machine
from machine import Pin
import network

# Connect to WiFi network
ssid = "Your_SSID"
password = "Your_Password"
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)
while station.isconnected() == False:
  pass

# Set up the socket server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

# Set up the micro servo motor
servo_pin = Pin(2, Pin.OUT) # D4
servo = machine.PWM(servo_pin, freq=50)

# Define the HTML response
html = """<!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Micro Servo Motor Control Web Server</title>
  </head>
  <body>
    <h2>Micro Servo Motor Control Web Server</h2>
    <p>Position: <span id="position">%s</span></p>
    <input type="range" min="0" max="180" onchange="updateServo(this.value)">
    <script>
      function updateServo(position) {
        var xhr = new XMLHttpRequest();
        xhr.open("GET", "/position?value=" + position, true);
        xhr.send();
        document.getElementById("position").innerHTML = position;
      }
    </script>
  </body>
</html>
"""

# Handle incoming client requests
def handle_request(client):
  request = client.recv(1024)
  request_str = request.decode('utf-8')
  request_method = request_str.split(' ')[0]
  request_path = request_str.split(' ')[1]

  # If the request is for the root path, send the HTML response
  if request_path == '/':
    response = html % servo.duty()
    client.send(response.encode('utf-8'))
  
  # If the request is for the position path, set the servo position
  elif request_path.startswith('/position'):
    position = int(request_path.split('=')[1])
    servo.duty(40 + (position * 8 // 180))
    client.send('OK'.encode('utf-8'))
  
  # If the request is for an invalid path, return a 404 error
  else:
    response = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\nNot Found'
    client.send(response.encode('utf-8'))

# Start the main loop
while True:
  # Wait for a client to connect
  client, addr = s.accept()
  print('Client connected from', addr)
  
  # Handle the client request
  handle_request(client)
  
  # Close the client connection
  client.close()

import machine
import time
from machine import PWM, Pin
import uasyncio as asyncio
from microWebSrv import MicroWebSrv

# Define LED Pins
red_led_pin = 5
blue_led_pin = 6
green_led_pin = 7

# Setup LEDs
red_led = Pin(red_led_pin, Pin.OUT)
blue_led = Pin(blue_led_pin, Pin.OUT)
green_led = Pin(green_led_pin, Pin.OUT)

# Define Servo Pin
servo_pin = 4

# Setup Servo
servo = PWM(Pin(servo_pin), freq=50)

# Web Interface Functionality
async def index(request, response):
    content = """\
<html>
<head>
  <title>ESP8266 MicroPython</title>
</head>
<body>
  <h1>ESP8266 MicroPython Web Interface</h1>
  <table>
    <tr>
      <td><form action="/red_led" method="POST"><button name="red_led" value="toggle">Toggle Red LED</button></form></td>
      <td><form action="/blue_led" method="POST"><button name="blue_led" value="toggle">Toggle Blue LED</button></form></td>
      <td><form action="/green_led" method="POST"><button name="green_led" value="toggle">Toggle Green LED</button></form></td>
    </tr>
    <tr>
      <td><form action="/red_led" method="POST">Red LED Brightness: <input type="range" min="0" max="1023" name="brightness"></form></td>
      <td><form action="/blue_led" method="POST">Blue LED Brightness: <input type="range" min="0" max="1023" name="brightness"></form></td>
      <td><form action="/green_led" method="POST">Green LED Brightness: <input type="range" min="0" max="1023" name="brightness"></form></td>
    </tr>
  </table>
</body>
</html>
"""
    response.WriteResponseOk(headers=None,
                             contentType="text/html",
                             contentCharset="UTF-8",
                             content=content)

async def red_led(request, response):
    global red_led
    if request.GetPost("red_led", "") == "toggle":
        red_led.value(not red_led.value())
    brightness = request.GetPost("brightness", "")
    if brightness:
        red_led_pwm = PWM(Pin(red_led_pin), freq=500, duty=int(brightness))
    response.WriteResponseOk()

async def blue_led(request, response):
    global blue_led
    if request.GetPost("blue_led", "") == "toggle":
        blue_led.value(not blue_led.value())
    brightness = request.GetPost("brightness", "")
    if brightness:
        blue_led_pwm = PWM(Pin(blue_led_pin), freq=500, duty=int(brightness))
    response.WriteResponseOk()

async def green_led(request, response):
    global green_led
    if request.GetPost("green_led", "") == "toggle":
        green_led.value(not green_led.value())
    brightness = request.GetPost("brightness", "")
    if brightness:
        green_led_pwm = PWM(Pin(green_led_pin), freq=500, duty=int(brightness))
    response.WriteResponseOk()

# Start the Web Server
srv = MicroWebSrv(webPath='/', port=80)
srv.Max
srv.Start()

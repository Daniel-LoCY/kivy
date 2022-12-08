import base64
import cv2 as cv
import numpy as np
import paho.mqtt.client as mqtt
import time
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.clock import Clock

MQTT_BROKER = "20.80.46.248"
MQTT_RECEIVE = "home/server"
frame = np.zeros((240, 320, 3), np.uint8)
jpg = 'frame.jpg'

client = mqtt.Client()

client.connect(MQTT_BROKER)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(MQTT_RECEIVE)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print('on message')
    global frame
    # Decoding the message
    img = base64.b64decode(msg.payload)
    # converting into numpy array from buffer
    npimg = np.frombuffer(img, dtype=np.uint8)
    # Decode to Original Frame
    frame = cv.imdecode(npimg, 1)
    cv.imwrite(jpg, frame)

client.on_connect = on_connect
client.on_message = on_message
# Starting thread which will receive the frames
client.loop_start()
# Stop the Thread
# client.loop_stop()

class LoginScreen(GridLayout):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 1
        # self.add_widget(Label(text='User Name'))
        # self.username = TextInput(multiline=False)
        # self.add_widget(self.username)
        # self.add_widget(Label(text='password'))
        # self.password = TextInput(password=True, multiline=False)
        # self.add_widget(self.password)
        self.image = Image()
        self.i = self.add_widget(self.image)
        Clock.schedule_interval(self.update_image, 0.1)

    def update_image(self, d):
        print('update image')
        self.image.source=jpg
        self.image.reload()

class MyApp(App):

    def build(self):
        return LoginScreen()


if __name__ == '__main__':
    MyApp().run()

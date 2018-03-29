import time
import sys

import ibmiotf.device

from pynput.keyboard import Key, Controller
from flask import Flask

organization = "ah7y2u"
deviceType = "laptop"
deviceId = "mymacpro"
authMethod = "token"
authToken = "passw0rd"
domain = "internetofthings.ibmcloud.com"

def ppt_op(op):
    keyboard = Controller()
    if op == "play" :
        with keyboard.pressed(Key.cmd):
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
    elif op == "next" : 
        keyboard.press(Key.down)
        keyboard.release(Key.down)
    elif op == "prev":
        keyboard.press(Key.up)
        keyboard.release(Key.up)
    elif op == "end":
        keyboard.press(Key.esc)
        keyboard.release(Key.esc)

def myCommandCallback(cmd):
    print("Command received:%s", cmd.data["cmd"])
    ppt_op(cmd.data["cmd"])

def run_mqtt():
    # Initialize the device client.
    try:
        deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken, "domain":domain}
        client = ibmiotf.device.Client(deviceOptions)
    except Exception as e:
        print("Caught exception connecting device: %s" % str(e))
        sys.exit()

    client.connect()
    client.commandCallback = myCommandCallback

    while(1):
		data = { 'connected' : True}
		client.publishEvent("status", "json", data)
		time.sleep(3)

if __name__ == '__main__':
	run_mqtt()
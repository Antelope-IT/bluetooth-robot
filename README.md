Robot
=====
This repository contains source code for a bluetooth controlled robot. The robot uses the [CamJam Edukit3](https://camjam.me/?page_id=1035) components and the software is inspired by the [tutorials](https://github.com/CamJam-EduKit/EduKit3/tree/master/CamJam%20Edukit%203%20-%20GPIO%20Zero) for the kit. This project is a learning vehicle for me to learn about and improve my Python, Raspberry Pi, Electronics and Robotics skills. 

In addition to the CamJam kit this project also uses an [8BitDo Zero 2](https://www.8bitdo.com/zero2/) bluetooth controller to control the robot.

Health Warning
==============
Please be aware that this project is still a work in progress and is incomplete - this is just the first commit. As such, its not finished and therefore not fully implemented, and what code there is here probably doesn't all work. Worse than that I'm just learning Python so I'm not even an expert. That all said, you are welcome to use this code, borrow from it, and to learn from my mistakes, however I make no guarantees as to its functionality or suitability. You can't say I didn't warn you.

Status
======
The initial commit includes one code file device_connector.py. This module encapsulates the code that maintains the connection to the bluetooth controller and returns a stream of events. It leverages the libevdev library to return a stream of events from the controller. The events that are returned are the direct output from the libevdev library, so as yet there is no translation layer to convert the events to commands: Forward, Left, Right, Back, Stop, etc.

Features
--------
Features and functionality are limited at the moment for obvious reasons - its not finished. But what can be demonstrated by running this module is:

* When run with a device Id.
  - It waits for the device to connect.


* When the device connects.
  - It prints a series of controller keypad events


* If the device disconnects.
  - It handles the disconnection gracefully (no exceptions).
  - It waits to reconnect.


* On reconnection.
  - It resumes printing keypad events.


* When running.
  - It terminates gracefully when CTRL-C is pressed.


* When run without a device id.
  - It prints usage help to the console.
 
Testing
=======
This code is being built on Raspbian Buster using Python 3. To test the code, setup the pre-requisites and then run the python module with the command shown below.


Pre-Requisites
--------------
From memory the only pre-requisites are the libevdev library and you will need to pair the bluetooth controller with the Raspberry Pi manually. With Raspbian Buster pairing the controller from the desktop is as easy as following the the 8BitDo pairing instructions for clarity I have configured my controller to work in xinput mode but I don't believe it matters (YMMV).

Having paired the controller and more importantly while the controller is still connected (because it disappears when its not) identify the device Id for the controller. 

List out the devices attached to your computer with the following command:

```
cat /proc/bus/input/devices
```

From here inspect the output and search for the device with the name "8BitDo Zero 2 gamepad". From here scan down until you find the H: Handlers=kb event<x> js<y> where x and y are replaced by integers which I think will depend on the number of devices and joysticks you have attached. The one to take note of here is the eventX handler value - this is the value we'll construct our device id with which gets passed to the module as the first(only) argument when run. 

To install the python libevdev library use:

```
sudo pip3 install libevdev
```

Usage
-----
Run the module with the command below replacing 'eventX' with the id of the handler you found above.

```
python3 device_connector.py /dev/input/eventX
```

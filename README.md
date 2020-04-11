Robot
=====
This repository contains source code for a Bluetooth controlled robot. The robot uses the [CamJam Edukit3](https://camjam.me/?page_id=1035) components and the software is inspired by the [tutorials](https://github.com/CamJam-EduKit/EduKit3/tree/master/CamJam%20Edukit%203%20-%20GPIO%20Zero) for the kit. This project is a learning vehicle for me to learn about and improve my Python, Raspberry Pi, Electronics and Robotics skills. 

In addition to the CamJam kit this project also uses an [8BitDo Zero 2](https://www.8bitdo.com/zero2/) Bluetooth controller to control the robot.

Health Warning
==============
Please be aware that this project is still a work in progress and is incomplete - these are just first commits. As such, its not finished and therefore not fully implemented, and what code there is here probably doesn't all work. Worse than that I'm just learning Python so I'm not even an expert. That all said, you are welcome to use this code, borrow from it, and to learn from my mistakes, however I make no guarantees as to its functionality or suitability. You can't say I didn't warn you.

Status
======
The project has now been moved to the [JetBrains pycharm (Community Edition) IDE](https://www.jetbrains.com/pycharm/) essentially for the improved (imho) debugging experience hence the .idea directory - this can be safely ignored it contains no pertinent code.

The initial commit had one code file: device_connector.py. This commit has some modifications to the way this module functions with no (intentional) major changes to the functionality. 
In addition to this module the events module has been added which adds the EventSource class.  

The EventSource class provides the same functionality as the device_events function in the device_connector module but adds the ability to track and query if the device is attached. This new class can be exercised from the main module in the same way as the device_connector module.

Both modules encapsulate code that maintains the connection to the Bluetooth controller and returns a stream of events. Each leverages the libevdev library to return a stream of events from the controller. The events that are returned are the direct output from the libevdev library, so as yet there is no translation layer to convert the events to commands: Forward, Left, Right, Back, Stop, etc.

The focus of the development moves to the new EventSource class. 

Features (as demonstrated by main.py)
--------
Features and functionality are limited at the moment for obvious reasons - its not finished. But what can be demonstrated by running this module is:

* When run with a device Id.
  - It waits for the device to connect.


* When the device connects.
  - It prints a series of controller keypad events


* If the device disconnects
  - It handles the disconnection gracefully (no exceptions)
  - It waits to reconnect 
  - It prints a `Disconnected message` - driven by the EventSource instance is_connected property

* On reconnection 
  - It resumes printing keypad events.


* When running (and the controller is disconnected)
  - It terminates gracefully when CTRL-C is pressed

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
From memory the only pre-requisites are the libevdev library and you will need to pair the Bluetooth controller with the Raspberry Pi manually. With Raspbian Buster pairing the controller from the desktop is as easy as following the the 8BitDo pairing instructions for clarity I have configured my controller to work in `xinput` mode but I don't believe it matters (YMMV).

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
python3 main.py /dev/input/eventX

```

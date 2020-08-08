Robot
=====
This repository contains source code for a Bluetooth controlled robot. The robot uses the [CamJam Edukit3](https://camjam.me/?page_id=1035) components and the software is inspired by the [tutorials](https://github.com/CamJam-EduKit/EduKit3/tree/master/CamJam%20Edukit%203%20-%20GPIO%20Zero) for the kit. This project is a learning vehicle for me to learn about and improve my Python, Raspberry Pi, Electronics and Robotics skills. 

In addition to the CamJam kit this project also uses an [8BitDo Zero 2](https://www.8bitdo.com/zero2/) Bluetooth controller to control the robot.

Health Warning
==============
Please be aware that this project is a work in progress. As such, its not finished in so far as while I am happy with the current functionality of the robot(buggy) and the ability to control it with the 8BitDo controller I am sure the code could be improved and simplified. That all said, you are welcome to use this code, borrow from it, and to learn from my mistakes, however I make no guarantees as to its functionality or suitability. As always, it works for me but YMMV.

Status
======
The project has now been moved to the [JetBrains pycharm (Community Edition) IDE](https://www.jetbrains.com/pycharm/) essentially for the improved (imho) debugging experience hence the .idea directory - this can be safely ignored it contains no pertinent code.

The initial commit had one code file: device_connector.py. This commit has some modifications to the way this module functions with no (intentional) major changes to the functionality. In addition to this module the events module has been added which adds the EventSource class.  

The project has moved on since the original commit adding the ability to interface and control the hardware attached to the pi. The project structure has changed in an attempt to conform to standard practice for python projects this hasn't been entirely successful and further changes and refinements are necessary.

This version of the code is functional; it is possible to control the robot with the Bluetooth controller. The proximity sensor has been added to the project with code to implement an auto-breaking function. This can be best described as experimental 

Code quality is low and work is required to improve code quality, the packaging of project and its overall usability. 

Features (as demonstrated by main.py)
--------
Features and functionality are limited at the moment for obvious reasons - its not finished. But what can be demonstrated by running this module is:

* When run with a device Id.
  - It waits for the device to connect.

* When the device connects.
  - It prints a device connected message
  - It updates the control states

* If the device disconnects
  - It handles the disconnection gracefully (no exceptions)
  - It waits to reconnect 
  - It zeroes the control state, stopping the robot
  - ~It prints a `Disconnected message` - driven by the EventSource instance is_connected property~ TODO: Fix

* On reconnection 
  - It resumes updating the state of the robot control with keypad events from the controller.

* When running (and the controller is disconnected)
  - ~It terminates gracefully when CTRL-C is pressed.~ TODO Fix

* When running (and the controller is connected).
  - It ignores when CTRL-C is pressed.
  - It updates the state of the robot control with keypad events from the controller.
  - The control state is surfaced as an iterable that can be queried by the GPIZero Robot device.

* When run without a device id.
  - It prints usage help to the console.
  
* Shutdown button 
  - Robot (script and OS) can be shutdown by pressing a button connected between GND and GPIO27 for 2 sec. 
 
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

Optional Pre-Requisites
-----------------------

The robot uses an ultrasonic distance sensor, when running on a Pi Zero the accuracy and performance of this sensor can be improved by using the `pigpio` pin factory. The robot can be configured to use this pin factory by passing -z or --zero on the command line. However for this to work the `pigpiod` daemon needs to be running before the application starts.

If the library is not present on you system (Raspberry Pi OS Lite) you can install it with the following command
```
$ sudo apt install pigpio

```
To automate the daemon so that it starts when the OS starts run (to disable it again switch `enable` for `disable`.)
```
$ sudo systemctl enable pigpiod

```
To run the daemon once use:
```
$ sudo systemctl start pigpiod

``` 

Usage
-----
Run the module with the command below replacing 'eventX' with the id of the handler you found above.

```
python3 main.py /dev/input/eventX

```

A full description of the command line options available can be seen  by running 

```
python3 main.py -h

```

Setup For Autorun on Startup

There are many ways to implement this; I have selected the the `systemd` method:

1. In `/lib/systemd/system/` create a file robot.service 
```
sudo nano /lib/systemd/system/robot.service
```
2. Add the following content:
```
 [Unit]
 Description=Bluetooth controlled robot service
 After=multi-user.target

 [Service]
 Type=idle
 ExecStart=/usr/bin/python3 /home/pi/<path to project>/main.py /dev/input/event0 -z

 [Install]
 WantedBy=multi-user.target

```
3. Save the file and set the following permissions.
```
sudo chmod 644 /lib/systemd/system/robot.service
```
4. Configure `systemd` to run the script at start up.
```
sudo systemctl daemon-reload
sudo systemctl enable robot.service
```

5. reboot to see your changes take effect.

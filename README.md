# WIT-motion sensor module to Open Sound Control

### Purpose and specifications
Uses IMU sensors module from https://www.wit-motion.com/ahrs.html
and send the attitude datas by Open Sound Control (OSC) protocol (UDP over Ethernet).
Those sensors uses:
1. The module integrates high-precision gyroscopes, accelerometers, and geomagnetic field sensors, and uses high-performance microprocessors and advanced dynamics calculation and Kalman dynamic filtering algorithms to quickly solve the current real-time motion posture of the module.
2. The module integrates an attitude solver and cooperates with the dynamic Kalman filter algorithm to effectively reduce measurement noise and improve measurement accuracy. It can accurately output the current attitude of the module in a dynamic environment, with an attitude measurement accuracy of 0.2°, extremely high stability, and even better performance than some professional inclinometers.
3. The Z-axis heading angle is added to the geomagnetic sensor filter fusion, which solves the cumulative error caused by the drift of the gyroscope integral in the 6-axis algorithm, and can output heading angle data stably for a long time.
4. The output content can be selected arbitrarily, the data output frequency is 200Hz, and the default is 10HZ.
5. Reserve 4 expansion ports, which can be configured as analog input, digital input, digital output and other functions.
6. Using stamp hole gold plating technology, it can be embedded in the user's PCB board. The 4-layer PCB board technology is thinner, smaller and more reliable.
7. Bluetooth 5.0: supports Android/IOS operating system

### Sources
Files originated from Wit-motion Python SDK :
See https://github.com/WITMOTION/WitBluetooth_BWT901BLE5_0/tree/main/Python/BWT901BLE5.0_python_sdk

See in /assets for protocol documentaiton and module datasheet.

About OSC : https://opensoundcontrol.stanford.edu/index.html

Send 3D angles commands:
/WT/angX
/WT/angY
/WT/angZ

And board temp
/WT/temp

And Joystick positions and buttons :
/WT/JoyX
/WT/JoyY
/WT/SwitchC
/WT/SwitchZ

## Dependencies
### pyhtonosc
https://pypi.org/project/python-osc/
For OSC communication as UDP client.

### bleak
https://pypi.org/project/bleak/
For Bluetooth LE 5.0 coms.

### WT_Nunchuck.py
This describes the device class.

## WTNUNCHUCK Project
This project is with a refurbished Nitendo Nunchuck enclosure with its joystick and buttons.
It added a battery, USC C charger, and WT901BLE sensor module.
![WTNUNCHUCK closed](/assets/images/IMG3623.jpeg)
![WTNUNCHUCK open](/assets/images/IMG3624.jpeg)
Joystick and buttons are connected to D0..D3 expansion ports.
### Usage
Run WIT2OSC-NUNCHUCK.py
This use my MAC adress as default, you can change it or switch to the "scan" method.

It will send OSC to local (127.0.0.1) IP as default, but you can specify another IP as argument in the command line.
Port is 50061 by default.

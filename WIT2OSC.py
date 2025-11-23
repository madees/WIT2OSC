import asyncio
import socket
import sys
import datetime
import time

# Bluetooth 5.0 client package
# see https://github.com/hbldh/bleak
import bleak

# WITMOTION protocol device class (not pip package, instal manually in same folder)
# https://github.com/WITMOTION/WitBluetooth_BWT901BLE5_0/tree/main/Python/BWT901BLE5.0_python_sdk
import device_model

# OSC UDP Client package
from pythonosc.udp_client import SimpleUDPClient

#
# 扫描到的设备 Scanned devices
devices = []
# 蓝牙设备 BLEDevice
BLEDevice = None

#####################
# Function for WITMOTION modules
# see https://github.com/WITMOTION/WitBluetooth_BWT901BLE5_0/tree/main/Python/BWT901BLE5.0_python_sdk
#
# 扫描蓝牙设备并过滤名称
# Scan Bluetooth devices and filter names
async def scan():
    global devices
    global BLEDevice
    find = []
    print(str(datetime.datetime.now()), "Searching for Bluetooth devices......")
    try:
        devices = await bleak.BleakScanner.discover(timeout=20.0)
        n=0
        print(str(datetime.datetime.now()), "Search ended")
        for d in devices:
            if d.name is not None and "WT" in d.name:
                n=n+1
                find.append(d)
                print(n, ">",d)
        if len(find) == 0:
            print("No devices found in this search!")
        else:
            #user_input = input("Please enter the Mac address you want to connect to (e.g. DF:E9:1F:2C:BD:59)：")
            #for d in devices:
            #    if d.address == user_input:
            #        BLEDevice = d
            #        break
            n = int(input("Choose one device number to connect (0 to quit, return to re-scan):"))
            # quit if 0, set selected device address else
            if n==0:
                print("Aborted.")
                exit()
            else:
                n=n-1
                BLEDevice=devices[n]
    except Exception as ex:
        print(str(datetime.datetime.now()), "Bluetooth search failed to start")
        print(ex)


# 指定MAC地址搜索并连接设备
# Specify MAC address to search and connect devices
async def scanByMac(device_mac):
    global BLEDevice
    print(str(datetime.datetime.now()), "Searching for", device_mac," Bluetooth devices......")
    BLEDevice = await bleak.BleakScanner.find_device_by_address(device_mac, timeout=20)


# 数据更新时会调用此方法 This method will be called when data is updated
def updateData(DeviceModel):
    global client
    # 直接打印出设备数据字典 Directly print out the device data dictionary
    # print(DeviceModel.deviceData)
    # AccX, AccY, AccZ, AsX, AsY, AsZ, AngX, AngY, AngZ, HX, HY, HZ, Q0, Q1, Q2, Q3}
    client.send_message("/WIT/angX", DeviceModel.get("AngX"))
    client.send_message("/WIT/angY", DeviceModel.get("AngY"))
    client.send_message("/WIT/angZ", DeviceModel.get("AngZ"))
    #print ("New data received)")                 


#####################
# MAIN
if __name__ == '__main__':
    # Network parameters for OSC connection
    localIP=socket.gethostbyname(socket.gethostname())
    # Tx host
    txPort=50061
    # Command line argument may be recipient IP, without arg it will be Local
    if(len(sys.argv)==2):
        ipAddress=sys.argv[1]
    else:
        ipAddress="127.0.0.1"
    
    # Start the OSC system.
    client = SimpleUDPClient(ipAddress, txPort)  # Create client
    print(str(datetime.datetime.now()), "OSC client up and running on port "+str(txPort)+" @"+ipAddress)
 
    # Start the bluetooth sensor system.
    # 方式一：广播搜索和连接蓝牙设备
    # Method 1:Broadcast search and connect Bluetooth devices
    #asyncio.run(scan())

    # # 方式二：指定MAC地址搜索并连接设备
    # # Method 2: Specify MAC address to search and connect devices
    asyncio.run(scanByMac("38:1E:C7:E4:EA:BB"))

    if BLEDevice is not None:
        # 创建设备 Create device
        device = device_model.DeviceModel("MyBle5.0", BLEDevice, updateData)
        # 开始连接设备 Start connecting devices
        asyncio.run(device.openDevice())
    else:
        print("This BLEDevice was not found!!")
    
    print(str(datetime.datetime.now()), "Bluetooth sensor up and running, going into event loop.")
          
    # Periodically call osc4py3 processing method in your event loop.
    finished = False
    while not finished:
        time.sleep(0.05)
        # …
    # Properly close the system.
import asyncio
from bleak import BleakScanner
from bleak import BleakClient

# address as global, defualt as my WT901BLE67 module for debug
address = "38:1E:C7:E4:EA:BB"

# scan all devices found on network
async def main(address):
    # Discover bluetooth devices and select one
    while True:
        print("Scanning for devices...")
        devices = await BleakScanner.discover()
        n=0
        for d in devices:
            n=n+1
            print(n, ">", d, d.backend_id)
    
        try:
            n = int(input("Choose one device number to connect (0 to quit, return to re-scan):"))
            break
        except:
            #scan again if empty string or other
            pass

    # quit if 0, set selected device address else
    if n==0:
        print("Aborted.")
        exit()
    else:
        n=n-1
        address=devices[n]

    # Connect to this device with an async context manager
    print("Now trying to connect to ",address,"...")

    async with BleakClient(address) as client:
        # Read characterisitics etc
        print("Now connected to :")
        print("@",client.address)
        print("MTU size: ",client.mtu_size)

    # Device will disconnect when block exits.
    print(address," is now disconnected.")
    # ...

# Using asyncio.run() is important to ensure that device disconnects on
# KeyboardInterrupt or other unhandled exception.0

asyncio.run(main(address))
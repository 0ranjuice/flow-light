import asyncio
from bleak import BleakScanner, BleakClient

DeviceToBeFound = '10BE6E3D-88F8-913F-2644-996BBD2C4F1A'
characteristic_uuid = '0000FFE1-0000-1000-8000-00805F9B34FB'


async def ble_connection():
    device = None
    while device is None:
        devices = await BleakScanner.discover()
        for d in devices:
            if d.address == DeviceToBeFound:
                print("Target device detected!")
                print("Device: {}".format(d.name))
                print("Address: {}.".format(d.address))
                device = d
                break

    async with BleakClient(device.address) as client:
        await client.connect()
        while True:
            try:    
                # Wait for keyboard input
                input_str = input("Enter text to send to device: ")
                # Send text to device on ENTER key press
                await client.write_gatt_char(characteristic_uuid, input_str.encode())
            except KeyboardInterrupt:
                # Exit on Ctrl+C
                break


if __name__ == "__main__":
    asyncio.run(ble_connection())

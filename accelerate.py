import os
# Force uinput before importing pynput
os.environ['PYNPUT_BACKEND_KEYBOARD'] = 'uinput'
os.environ['PYNPUT_BACKEND_MOUSE'] = 'dummy'

import asyncio
from bleak import BleakScanner, BleakClient
import struct
from evdev import UInput, ecodes as e
from pynput.keyboard import Key, Controller
import time

# keyboard = Controller()
ui = UInput()

# Standard Cycling Power Measurement Characteristic UUID
CP_MEASUREMENT_UUID = "00002a63-0000-1000-8000-00805f9b34fb"
WATTS_THRESHOLD = 20
current_power = 0

def callback(sender, data):
    # data[0:2] = Flags
    # data[2:4] = Power (uint16)
    # data[4] = Balance (%)
    # data[5:7] = Revolutions

    global current_power

    power = struct.unpack('<h', data[2:4])[0]
    current_power = power

    balance = data[4] / 2.0  # Percentage

    crank_revs = struct.unpack('<H', data[5:7])[0]

    print(f"Power: {power}W | Balance: {balance}% | Revs: {crank_revs} | Raw: {data.hex()}")

# power based acceleration
async def accelerate():
    global current_power

    while True:
        if current_power < 50:
            await asyncio.sleep(0.1)
            continue

        #delay of repeated presses is linear with power
        delay = max(0, 0.2 * (1 - (current_power / 200)))
 
        ui.write(e.EV_KEY, e.KEY_LEFTSHIFT, 1)
        ui.write(e.EV_KEY, e.KEY_X, 1)
        ui.syn()
        await asyncio.sleep(0.05)
        ui.write(e.EV_KEY, e.KEY_LEFTSHIFT, 0)
        ui.write(e.EV_KEY, e.KEY_X, 0)
        ui.syn()


        # keyboard.press(Key.shift)
        # keyboard.press('x')
        # await asyncio.sleep(0.05) 
        # keyboard.release('x')
        # keyboard.release(Key.shift)

        await asyncio.sleep(delay)

# handles bluetooth connection
async def ble_logic():
    global current_power
    print("Scanning for Assioma pedals...")
    devices = await BleakScanner.discover()

    target_address = None
    for d in devices:
        # this just looks for hardcoded name, better let user choose from a list of devices
        if d.name and "ASSIOMA" in d.name and "L" in d.name:
            print(f"Found: {d.name} at {d.address}")
            target_address = d.address
            break

    if not target_address:
        print("Assioma pedals not found. Make sure they are awake!")
        return

    async with BleakClient(target_address) as client:
        print(f"Connected: {client.is_connected}")

        await client.start_notify(CP_MEASUREMENT_UUID, callback)

        print("Reading raw data (Press Ctrl+C to stop)...")
        while True:
            await asyncio.sleep(1)


async def main():
    try:
        await asyncio.gather(accelerate(), ble_logic())
    except KeyboardInterrupt:
        print("\nStopping...")

if __name__ == "__main__":
    asyncio.run(main())

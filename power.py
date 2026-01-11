import asyncio
import tkinter as tk
import gui
import struct

from bleak import BleakScanner, BleakClient
from evdev import UInput, ecodes as e
from state import shared_state

ui = UInput()


class PowerLogic:
    def __init__(self):
        # standard UUID for power
        self.CP_MEASUREMENT_UUID = "00002a63-0000-1000-8000-00805f9b34fb"
        self.ACC_THRESHOLD = 30
        self.ITEM_THRESHOLD = 50

    def get_target_address(self, devices):
        root = tk.Tk()
        app = gui.BluetoothSelectionGUI(root, devices)
        root.mainloop()
        return app.target_address

    def callback(self, sender, data):
        # data[0:2] = Flags
        # data[2:4] = Power (uint16)
        # data[4] = Balance (%)
        # data[5:7] = Revolutions

        power = struct.unpack("<h", data[2:4])[0]
        shared_state.power = power

        balance = data[4] / 2.0  # Percentage

        crank_revs = struct.unpack("<H", data[5:7])[0]
        print(
            f"Power: {power}W | Balance: {balance}% | Revs: {crank_revs} | Raw: {data.hex()}"
        )

    # power based acceleration
    async def power_acc(self):
        while True:
            if shared_state.power < self.ACC_THRESHOLD:
                await asyncio.sleep(0.1)
                continue

            # delay of repeated presses is linear with power
            delay = max(0, 0.2 * (1 - (shared_state.power / 200)))

            ui.write(e.EV_KEY, e.KEY_LEFTSHIFT, 1)
            ui.syn()
            await asyncio.sleep(0.05)
            ui.write(e.EV_KEY, e.KEY_LEFTSHIFT, 0)
            ui.syn()

            await asyncio.sleep(delay)

    # power based item use
    async def power_item(self):
        if shared_state.power > self.ITEM_THRESHOLD:
            ui.write(e.EV_KEY, e.KEY_Y, 1)
            ui.syn()
            await asyncio.sleep(0.05)

    # handles bluetooth connection
    async def power_ble(self):
        print("Scanning for Assioma pedals...")
        devices = await BleakScanner.discover()

        target_address = self.get_target_address(devices)

        if not target_address:
            print("Assioma pedals not found. Make sure they are awake!")
            return

        async with BleakClient(target_address) as client:
            print(f"Connected: {client.is_connected}")

            await client.start_notify(self.CP_MEASUREMENT_UUID, self.callback)

            print("Reading raw data (Press Ctrl+C to stop)...")
            while True:
                await asyncio.sleep(1)

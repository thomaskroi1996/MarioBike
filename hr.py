import tkinter as tk
import gui
import asyncio

from bleak import BleakScanner, BleakClient
from evdev import UInput, ecodes as e
from state import shared_state

ui = UInput()


class HRLogic:
    def __init__(self):
        # standard UUID for HR
        self.HR_MEASUREMENT_UUID = "00002a37-0000-1000-8000-00805f9b34fb"
        self.ACC_THRESHOLD = 100
        self.ITEM_THRESHOLD = 120

    def get_target_address(self, devices):
        root = tk.Tk()
        app = gui.BluetoothSelectionGUI(root, devices)
        root.mainloop()
        return app.target_address

    def callback(self, sender, data):
        # data[0]: Flags
        # data[1]: HR Value (UINT8)

        hr_value = data[1]
        shared_state.hr = hr_value
        print(f"\rHeart Rate: {hr_value} BPM")

    # hr based acceleration
    async def hr_acc(self):
        while True:
            if shared_state.hr < self.ACC_THRESHOLD:
                await asyncio.sleep(0.1)
                continue

            # delay of repeated presses is linear with hr
            delay = max(0, 0.2 * (1 - (shared_state.hr / 190)))

            ui.write(e.EV_KEY, e.KEY_LEFTSHIFT, 1)
            ui.write(e.EV_KEY, e.KEY_X, 1)
            ui.syn()
            await asyncio.sleep(0.05)
            ui.write(e.EV_KEY, e.KEY_LEFTSHIFT, 0)
            ui.write(e.EV_KEY, e.KEY_X, 0)
            ui.syn()

            await asyncio.sleep(delay)

    async def hr_item(self):
        if shared_state.hr > self.ITEM_THRESHOLD:
            ui.write(e.EV_KEY, e.KEY_Y, 1)
            ui.syn()
            await asyncio.sleep(0.05)

    # handles bluetooth connection
    async def hr_ble(self):
        print("Scanning for HR Sensors...")
        devices = await BleakScanner.discover()

        target_address = self.get_target_address(devices)

        if not target_address:
            print("HR Sensor not found. Make sure it is awake.")
            return

        async with BleakClient(target_address) as client:
            print(f"Connected: {client.is_connected}")

            await client.start_notify(self.HR_MEASUREMENT_UUID, self.callback)

            print("Reading raw data (Press Ctrl+C to stop)...")
            while True:
                await asyncio.sleep(1)

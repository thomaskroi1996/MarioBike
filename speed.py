import tkinter as tk
import gui
import asyncio
import struct

from bleak import BleakScanner, BleakClient
from evdev import UInput, ecodes as e
from state import shared_state

ui = UInput()


class SpeedLogic:
    def __init__(self):
        # standard UUID for speed
        self.SPEED_MEASUREMENT_UUID = "00002a5b-0000-1000-8000-00805f9b34fb"
        self.ACC_THRESHOLD = 17
        self.ITEM_THRESHOLD = 20
        self.last_revs = None
        self.last_time = None
        self.wheel_circum_mm = 2105

    # just bluetooth gui
    def get_target_address(self, devices):
        root = tk.Tk()
        app = gui.BluetoothSelectionGUI(root, devices)
        root.mainloop()
        return app.target_address

    def callback(self, sender, data):
        # data[0]: Flags
        # data[1:5]: Cumulative Wheel Revolutions (uint32)
        # data[5:7]: Last Wheel Event Time (uint16)

        revs = struct.unpack("<I", data[1:5])[0]
        event_time = struct.unpack("<H", data[5:7])[0]

        if self.last_revs is not None:
            delta_revs = revs - self.last_revs
            # time is in 1/1024 seconds
            delta_time = (event_time - self.last_time) / 1024.0

            # handle the 16-bit rollover (approx every 64 seconds)
            if delta_time < 0:
                delta_time += 64.0

            if delta_time > 0:
                # distance in meters = (revs * mm) / 1000
                dist_m = (delta_revs * self.wheel_circum_mm) / 1000.0
                # convert to km/h
                speed = (dist_m / delta_time) * 3.6
                return speed, revs, event_time

        return 0.0, revs, event_time

    # item release based on speed
    async def speed_item(self):
        if shared_state.speed > self.ITEM_THRESHOLD:
            ui.write(e.EV_KEY, e.KEY_Y, 1)
            ui.syn()
            await asyncio.sleep(0.05)

    # acceleration based on speed in km/h
    async def speed_acc(self):
        while True:
            if shared_state.speed < self.ACC_THRESHOLD:
                await asyncio.sleep(0.1)
                continue

            # delay of repeated presses is linear with hr
            delay = max(0, 0.2 * (1 - (shared_state.speed / 190)))

            ui.write(e.EV_KEY, e.KEY_LEFTSHIFT, 1)
            ui.write(e.EV_KEY, e.KEY_X, 1)
            ui.syn()
            await asyncio.sleep(0.05)
            ui.write(e.EV_KEY, e.KEY_LEFTSHIFT, 0)
            ui.write(e.EV_KEY, e.KEY_X, 0)
            ui.syn()

            await asyncio.sleep(delay)

    # handles bluetooth connection
    async def speed_ble(self):
        print("Scanning for Speed sensors...")
        devices = await BleakScanner.discover()

        target_address = self.get_target_address(devices)

        if not target_address:
            print("Speed sensor not found. Make sure it is awake.")
            return

        async with BleakClient(target_address) as client:
            print(f"Connected: {client.is_connected}")

            await client.start_notify(self.SPEED_MEASUREMENT_UUID, self.callback)

            print("Reading raw data (Press Ctrl+C to stop)...")
            while True:
                await asyncio.sleep(1)

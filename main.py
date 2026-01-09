import os

# Force uinput before importing pynput
os.environ["PYNPUT_BACKEND_KEYBOARD"] = "uinput"
os.environ["PYNPUT_BACKEND_MOUSE"] = "dummy"

import asyncio
import gui
from power import PowerLogic
from hr import HRLogic
from speed import SpeedLogic

async def start_power_mode():
    run = PowerLogic()
    await asyncio.gather(run.power_acc(), run.power_ble())

async def start_hr_mode():
    run = HRLogic()
    await asyncio.gather(run.hr_acc(), run.hr_ble())

async def start_speed_mode():
    run = SpeedLogic()
    await asyncio.gather(run.speed_acc(), run.speed_ble())

if __name__ == "__main__":
    mode = gui.get_user_mode()

    if mode == "POWER":
        print("Starting Power Mode...")
        try:
            asyncio.run(start_power_mode())
        except KeyboardInterrupt:
            print("\nStopped by user.")
    elif mode == "HR":
        print("Starting HR Mode...")
        try:
            asyncio.run(start_hr_mode())
        except KeyboardInterrupt:
            print("\nStopped by user.")
    elif mode == "SPEED":
        print("Starting SPEED Mode...")
        try:
            asyncio.run(start_speed_mode())
        except KeyboardInterrupt:
            print("\nStopped by user.")

import subprocess
import sys
import pkg_resources

def install_requirements():
    requirements = ["mediapipe", "opencv-python", "bleak", "evdev"]
 
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = [pkg for pkg in requirements if pkg.replace("-", "_") not in installed]

    if missing:
        print(f"📦 Missing packages detected: {missing}. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("All packages installed. Restarting script...")
            subprocess.call([sys.executable] + sys.argv)
            sys.exit()
        except Exception as e:
            print(f"Failed to install packages: {e}")
            sys.exit(1)

install_requirements()

import os

os.environ["PYNPUT_BACKEND_KEYBOARD"] = "uinput"
os.environ["PYNPUT_BACKEND_MOUSE"] = "dummy"
os.environ["QT_QPA_PLATFORM"] = "xcb"

import asyncio
import gui
from power import PowerLogic
from hr import HRLogic
from speed import SpeedLogic
from steering import VideoSteering

async def start_power_mode():
    run = PowerLogic()
    await asyncio.gather(run.power_acc(), run.power_ble(), run.power_item())

async def start_hr_mode():
    run = HRLogic()
    await asyncio.gather(run.hr_acc(), run.hr_ble(), run.hr_item())

async def start_speed_mode():
    run = SpeedLogic()
    await asyncio.gather(run.speed_acc(), run.speed_ble(), run.speed_item())

async def launch_game():
    game_command = "mupen64plus mk64.z64"
 
    print(f"Launching game: {game_command}")

    process = await asyncio.create_subprocess_shell(
        game_command,
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL
    )

    await process.wait()
    print("Game closed.")

async def main():
    # get input from mode selection
    mode = gui.get_user_mode()

    try:
        async with asyncio.TaskGroup() as tg:
            print(f"Initializing Systems for {mode} mode...")

            # steer using webcam
            steer_system = VideoSteering()
            tg.create_task(steer_system.run())

            # select mode for acceleration logic
            if mode == "POWER":
                print("Starting Power Mode...")
                tg.create_task(start_power_mode())
            elif mode == "HR":
                print("Starting HR Mode...")
                tg.create_task(start_hr_mode())
            elif mode == "SPEED":
                print("Starting SPEED Mode...")
                tg.create_task(start_speed_mode())

            await asyncio.sleep(1.5)

            tg.create_task(launch_game())

    except* Exception as eg:
        for error in eg.exceptions:
            print(f"Task error: {error}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopping MarioBike64 ... ")

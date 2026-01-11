import asyncio

from bleak import BleakClient
from state import shared_state

class HelioStrap:
    def __init__(self, address):
        self.address = address

        # Standard HR UUIDs
        self.HR_MEAS_UUID = "00002a37-0000-1000-8000-00805f9b34fb"
        self.HR_CTRL_UUID = "00002a39-0000-1000-8000-00805f9b34fb"

    def callback(self, sender, data):
        shared_state.hr = data[1]
        print(f"[Helio Strap] HR: {shared_state.hr} BPM")

    async def connect(self):
        async with BleakClient(self.address) as client:
            print(f"Connected to Helio Strap at {self.address}")

            try:
                await client.write_gatt_char(
                    self.HR_CTRL_UUID, bytearray([0x15, 0x01, 0x01])
                )
            except:
                pass

            await client.start_notify(self.HR_MEAS_UUID, self.callback)

            while True:
                await asyncio.sleep(1)

Simple setup for using power, heart rate and speed output from bike sensors for accelerating in MarioKart 64, or any other game really.

Python libraries used:
- Bleak
- evdev
- struct
- asyncio

Additionally you will need an Nintendo 64 emulator and a ROM for the game.

The frequency of hitting the acceleration button scales linearly with the data output, and the minimum power required to move is 50 W. Minimum HR is 100, minimum speed is 17 km/h.

If HR, power and speed exceed certain thresholds, items are used.

Next:
- steer with webcam
- difficulty modes (modify minimum power)
- figure out holding items
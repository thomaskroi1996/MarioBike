Simple setup to connect Favero Assioma Duo Power meter pedals to Mario Kart 64. 
The more power you put out, the faster you go in game.
Additionally, you can steer using your phone on the handlebar with it's accelerometers using the Phyphox app.
You can only use items if you can get your heart rate above 150 BPM or the Cadence > 100.

This is easily customizable to any power meter.

Python libraries used:
- Bleak
- evdev
- struct
- asyncio

Additionally you will need an Nintendo 64 emulator and a ROM for the game.

The frequency of hitting the acceleration button scales linearly with the power output, and the minimum power required to move is 50 W.

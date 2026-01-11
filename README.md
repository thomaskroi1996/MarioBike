Simple setup for using power, heart rate and speed output from bike sensors for accelerating in MarioKart 64, or any other game really.

Steering is done by using your webcam to detect hand positions.

Additionally you will need an Nintendo 64 emulator and a ROM for the game.

The frequency of hitting the acceleration button scales linearly with the data output, and the minimum power required to move is 50 W. Minimum HR is 100, minimum speed is 17 km/h.

If HR, power and speed exceed certain thresholds, you can use an item by holding your hand on your forehead. Make sure you are in the center panel of the webcam footage. To hold an item for blocking, better aiming etc... threshold must be exceeded, and you have to make a fist above your forehead. Drifting is done by leaning into that direction.

Next:
- difficulty modes (modify minimum for acceleration and items)

User has to be part of input group:
sudo usermod -aG input $USER

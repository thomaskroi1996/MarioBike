Simple setup for using power, heart rate and speed output from bike sensors for accelerating in MarioKart 64, or any other game really.

I used Omarchy to debug, so likely there will be some issues on other OS, even though I tried to generalise it. In the future I will use Docker, but for now I just focus on a smooth experience. Ideally, you just have to run "run.sh", and it will download all the packages, and start everything from sensor conenction, to gesture recognition and the game automatically.

Since it is illegal to share ROMS, you have to download it and put it into the directory. I used mupen64plus as my emulator, so the key mappings are specialised for it.

Steering is done by using your webcam to detect hand positions.

The frequency of hitting the acceleration button scales linearly with the data output, and the minimum power required to move is 50 W. Minimum HR is 100, minimum speed is 17 km/h.

If HR, power and speed exceed certain thresholds, you can use an item by holding your hand above your forehead. Make sure you are in the center panel of the webcam footage. To hold an item for blocking, better aiming etc... threshold must be exceeded, and you have to make a fist above your forehead. Drifting is done by leaning into that direction.

Next:
- difficulty modes (modify minimum for acceleration and items)

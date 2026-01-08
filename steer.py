import requests
import pydirectinput
import time

# Replace this with the URL shown on your phone screen
PHYPHOX_URL = "http://192.168.1.15:8080"
TILT_THRESHOLD = 3.0  # Sensitivity: higher = lean more to turn

def get_tilt():
    try:
        # Phyphox provides a /get endpoint for live data
        # 'accX' is the internal name for the X-axis in the "Acceleration with g" experiment
        response = requests.get(f"{PHYPHOX_URL}/get?accX=val", timeout=0.1)
        data = response.json()
        
        # Extract the value from the buffer
        acc_x = data['buffer']['accX']['value'][0]
        return acc_x
    except Exception as e:
        print(f"Error connecting to Phyphox: {e}")
        return 0

print("Steering Active! Tilt your phone to steer.")

try:
    while True:
        tilt = get_tilt()
        
        if tilt > TILT_THRESHOLD:
            pydirectinput.keyDown('left')
            pydirectinput.keyUp('right')
            print(f"Left  ({tilt:.2f})")
        elif tilt < -TILT_THRESHOLD:
            pydirectinput.keyDown('right')
            pydirectinput.keyUp('left')
            print(f"Right ({tilt:.2f})")
        else:
            pydirectinput.keyUp('left')
            pydirectinput.keyUp('right')
            
        # Small delay to prevent spamming the phone's CPU
        time.sleep(0.05) 

except KeyboardInterrupt:
    print("Stopping...")

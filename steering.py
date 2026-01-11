import cv2
import mediapipe as mp
import asyncio

from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from evdev import UInput, ecodes as e
from state import shared_state

class VideoSteering:
    def __init__(self, model_path="hand_landmarker.task"):
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=1,
            running_mode=vision.RunningMode.VIDEO,
        )
        self.detector = vision.HandLandmarker.create_from_options(options)

        # camera
        self.cap = cv2.VideoCapture(0)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.ui = UInput()
        self.is_running = True
    # press key and wait duration before releasing
    async def tap_key(self, key, duration):
        if duration <= 0: return
        self.ui.write(e.EV_KEY, key, 1)
        self.ui.syn()
        await asyncio.sleep(duration)
        self.ui.write(e.EV_KEY, key, 0)
        self.ui.syn()

    async def run(self):
        print("Steering System Initialized...")

        current_key = None

        while self.is_running and self.cap.isOpened():
            success, frame = self.cap.read()
            if not success:
                break

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

            timestamp_ms = int(asyncio.get_event_loop().time() * 1000)
            result = self.detector.detect_for_video(mp_image, timestamp_ms)

            steer_dir = "NEUTRAL"
            target_key = None 

            if result.hand_landmarks:
                # just use hand above wrist for information
                wrist = result.hand_landmarks[0][0]
                hand_x = wrist.x
                if hand_x < 0.4:
                    intensity = (0.4 - hand_x) * 0.2 # Max pulse ~80ms
                    asyncio.create_task(self.tap_key(e.KEY_LEFT, intensity))
                elif hand_x > 0.6:
                    intensity = (hand_x - 0.6) * 0.2 
                    asyncio.create_task(self.tap_key(e.KEY_RIGHT, intensity))

            # if current_key and current_key != target_key:
            #     self.ui.write(e.EV_KEY, current_key, 0)
            #     self.ui.syn()
            #     current_key = None
            #
            # if target_key and current_key != target_key:
            #     self.ui.write(e.EV_KEY, target_key, 1)
            #     self.ui.syn()
            #     current_key = target_key
            #
            cv2.line(
                frame,
                (int(self.width * 0.35), 0),
                (int(self.width * 0.35), self.height),
                (255, 255, 255),
                1,
            )
            cv2.line(
                frame,
                (int(self.width * 0.65), 0),
                (int(self.width * 0.65), self.height),
                (255, 255, 255),
                1,
            )
            cv2.putText(
                frame,
                f"STEER: {steer_dir}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )

            cv2.imshow("Steering", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

            await asyncio.sleep(0.01)

    def close(self):
        self.cap.release()
        cv2.destroyAllWindows()

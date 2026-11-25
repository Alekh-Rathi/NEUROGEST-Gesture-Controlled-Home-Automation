"""
NEUROGEST - Gesture Control Home Automation System
Python side: webcam + MediaPipe hand tracking + serial communication.
Edit PORT to match the Arduino port shown in your computer's device manager.
"""

import time
import cv2
import mediapipe as mp
import serial

PORT = "COM10"       # Change this (e.g. COM3 on Windows or /dev/ttyACM0 on Linux)
BAUD_RATE = 9600
CAMERA_INDEX = 0
MAX_LEDS = 5


def count_raised_fingers(hand_landmarks, handedness_label):
    """Return the number of raised fingers (0 to 5) from MediaPipe landmarks."""
    lm = hand_landmarks.landmark
    count = 0

    # Thumb: compare horizontal landmark positions.
    # The webcam frame is mirrored before processing.
    if handedness_label == "Right":
        if lm[4].x < lm[3].x:
            count += 1
    else:
        if lm[4].x > lm[3].x:
            count += 1

    # Index, middle, ring and little fingers: fingertip above PIP joint.
    finger_pairs = [(8, 6), (12, 10), (16, 14), (20, 18)]
    for tip_id, pip_id in finger_pairs:
        if lm[tip_id].y < lm[pip_id].y:
            count += 1

    return min(count, MAX_LEDS)


def main():
    arduino = None
    camera = None

    try:
        print(f"Connecting to Arduino on {PORT}...")
        arduino = serial.Serial(PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # Allow the Arduino to reset after the serial connection opens.
        print("Arduino connected.")

        camera = cv2.VideoCapture(CAMERA_INDEX)
        if not camera.isOpened():
            raise RuntimeError("Could not open the webcam. Check CAMERA_INDEX and camera access.")

        mp_hands = mp.solutions.hands
        mp_drawing = mp.solutions.drawing_utils
        last_sent_count = None

        with mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.6
        ) as hands:

            while True:
                success, frame = camera.read()
                if not success:
                    print("Could not read a frame from the webcam.")
                    break

                frame = cv2.flip(frame, 1)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(rgb_frame)

                led_count = 0

                if results.multi_hand_landmarks:
                    hand_landmarks = results.multi_hand_landmarks[0]
                    handedness = results.multi_handedness[0].classification[0].label
                    led_count = count_raised_fingers(hand_landmarks, handedness)

                    mp_drawing.draw_landmarks(
                        frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                    )

                # Send only when the count changes; send 0 when no hand is detected.
                if led_count != last_sent_count:
                    arduino.write(f"{led_count}\n".encode("utf-8"))
                    last_sent_count = led_count

                cv2.putText(
                    frame,
                    f"LED Count: {led_count}",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )
                cv2.imshow("NEUROGEST - Gesture LED Control", frame)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

    except serial.SerialException as error:
        print(f"Serial connection error: {error}")
        print("Check the Arduino port, USB cable, and that the Arduino IDE Serial Monitor is closed.")
    except Exception as error:
        print(f"Error: {error}")
    finally:
        if camera is not None:
            camera.release()
        if arduino is not None and arduino.is_open:
            # Turn all LEDs off before closing, if the board is still connected.
            try:
                arduino.write(b"0\n")
                arduino.close()
            except serial.SerialException:
                pass
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

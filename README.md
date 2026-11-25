# NEUROGEST — Gesture Control Home Automation System

NEUROGEST is a touchless home-automation prototype that uses hand gestures captured by a webcam to control LED outputs through an Arduino UNO. The prototype combines computer vision, Python processing, USB serial communication and embedded hardware.

## How it works

1. A webcam captures live video of the user's hand.
2. OpenCV reads and prepares each video frame.
3. MediaPipe Hands detects hand landmarks.
4. The Python program estimates the number of raised fingers (0–5).
5. Python sends the count to the Arduino UNO over USB serial communication.
6. Arduino switches five LEDs according to the received count.
7. A 16x2 LCD displays the project name and current LED count.

**Workflow:** Camera → Python (OpenCV + MediaPipe) → USB Serial → Arduino UNO → LEDs + 16x2 LCD

## Technologies

- Python
- OpenCV
- MediaPipe
- PySerial
- Arduino UNO
- Embedded C++
- USB serial communication
- 16x2 LCD

## Hardware used

- Arduino UNO
- Webcam
- Five LEDs
- Five 220-ohm resistors
- 16x2 LCD
- Breadboard and jumper wires
- USB cable
- Potentiometer for LCD contrast

## Wiring

### LEDs

| Component | Arduino connection |
|---|---|
| LED 1 | D2 through 220Ω resistor to GND |
| LED 2 | D3 through 220Ω resistor to GND |
| LED 3 | D4 through 220Ω resistor to GND |
| LED 4 | D5 through 220Ω resistor to GND |
| LED 5 | D6 through 220Ω resistor to GND |

### 16x2 LCD (4-bit mode)

| LCD pin | Arduino connection |
|---|---|
| RS | D7 |
| E | D8 |
| D4 | D9 |
| D5 | D10 |
| D6 | D11 |
| D7 | D12 |
| VSS | GND |
| VDD | 5V |
| V0 | Middle pin of potentiometer |
| RW | GND |
| A | 5V (use suitable current limiting if required by the LCD module) |
| K | GND |

Check your specific LCD module's datasheet and wiring before powering the circuit.

## Software setup

### 1. Install Python dependencies

```bash
python -m pip install -r requirements.txt
```

### 2. Upload the Arduino sketch

1. Open `arduino/neurogest_arduino/neurogest_arduino.ino` in the Arduino IDE.
2. Select **Arduino UNO** as the board.
3. Select the correct serial port.
4. Upload the sketch.
5. Close the Arduino IDE Serial Monitor before running the Python program.

### 3. Configure the serial port

Open `python/gesture_control.py` and update:

```python
PORT = "COM10"
```

Use the port assigned to your Arduino. On Linux it may look like `/dev/ttyACM0` or `/dev/ttyUSB0`.

### 4. Run the Python program

```bash
python python/gesture_control.py
```

Show your hand to the webcam. The number of detected raised fingers controls the LEDs. Press **q** in the camera window to quit.

## Project goals

- Demonstrate real-time hand landmark detection.
- Establish serial communication between a PC and Arduino UNO.
- Control multiple LED outputs based on detected gestures.
- Provide visual feedback through an LCD.
- Explore a low-cost, touchless human-machine interface.

## Limitations

- Detection can be affected by lighting and camera position.
- The prototype supports a limited set of gestures based on raised-finger count.
- LEDs simulate appliances; this prototype does not directly switch household AC appliances.

## Future scope

- Integrate with IoT-based smart-home systems.
- Expand gesture vocabulary using more advanced recognition.
- Explore applications in assistive technology and industrial automation.

## Team project

Developed as a team project at the National Institute of Electronics and Information Technology (NIELIT), Ajmer.

**My contribution (Alekh Rathi):** Project architecture and Arduino circuit integration, including LED, resistor and LCD configuration.

## Repository structure

```text
NEUROGEST/
├── README.md
├── requirements.txt
├── .gitignore
├── python/
│   └── gesture_control.py
└── arduino/
    └── neurogest_arduino.ino
```

## Note

This repository contains a cleaned, organized implementation based on the project synopsis. Update the serial port and test the code with your actual hardware before presenting it as a working build.

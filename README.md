# NeoPixel Ring (12 LEDs) Controller for Raspberry Pi 5

Control an Adafruit NeoPixel ring with 12 LEDs using your Raspberry Pi 5.

## Hardware Setup

### Wiring Connections

Your NeoPixel ring has 4 pins:
- **Data In** (DIN) - Signal input
- **Data Out** (DOUT) - For chaining (leave disconnected for single ring)
- **5V** (or VCC) - Power
- **GND** - Ground

Connect to Raspberry Pi 5:
- **Raspberry Pi 5V (Pin 2 or 4)** → NeoPixel **5V**
- **Raspberry Pi GND (Pin 6)** → NeoPixel **GND**
- **Raspberry Pi GPIO 18 (Pin 12)** → NeoPixel **Data In**
- **Data Out** - Leave disconnected (only used for chaining multiple rings)

**Important Notes:**
- NeoPixels require 5V power. For just 12 LEDs, the Pi's 5V pin should be sufficient
- For larger installations, use an external 5V power supply
- Add a 300-500Ω resistor between GPIO 18 and NeoPixel Data In (recommended)
- Add a 1000µF capacitor between 5V and GND near the NeoPixels (recommended)

### Pin Reference (Raspberry Pi 5)
```
Physical Pin 12 = GPIO 18 (PWM0)
Physical Pin 2/4 = 5V
Physical Pin 6/9/14/20/25/30/34/39 = GND
```

## Software Setup

### 1. Clone the Repository
```bash
cd ~
git clone <your-repo-url> neopixel_12
cd neopixel_12
```

### 2. Install System Dependencies
```bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-dev python3-venv
```

### 3. Create Virtual Environment (Optional but Recommended)
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Python Dependencies
```bash
pip3 install -r requirements.txt
```

## Usage

### Run the Demo Script
```bash
sudo python3 neopixel_controller.py
```

**Note:** You must run with `sudo` because GPIO access requires root privileges.

### Using in Your Own Scripts

```python
from neopixel_controller import *

# Simple color wipe
color_wipe((255, 0, 0))  # Red

# Rainbow effect
rainbow_cycle(wait=0.01, iterations=5)

# Pulse effect
pulse((0, 255, 0))  # Green pulse

# Clear all pixels
clear()
```

## Available Effects

- **color_wipe(color, wait)** - Wipe color across the ring
- **rainbow_cycle(wait, iterations)** - Rainbow animation
- **theater_chase(color, wait, iterations)** - Theater marquee effect
- **pulse(color, wait, steps)** - Breathing/pulse effect
- **spinner(color, wait, iterations)** - Single LED spinner
- **clear()** - Turn off all LEDs

## Configuration

Edit the constants in `neopixel_controller.py` to customize:

```python
PIXEL_PIN = board.D18    # Change GPIO pin
NUM_PIXELS = 12          # Change LED count
BRIGHTNESS = 0.3         # Adjust brightness (0.0-1.0)
```

## Troubleshooting

### "No module named 'board'"
Install dependencies: `pip3 install -r requirements.txt`

### "Can't open /dev/mem"
Run with sudo: `sudo python3 neopixel_controller.py`

### LEDs not lighting up
1. Check wiring connections
2. Verify 5V power is connected
3. Try different GPIO pin and update PIXEL_PIN
4. Check if NeoPixel is WS2812 compatible

### Wrong colors
Some NeoPixels use RGB order instead of GRB. Change:
```python
ORDER = neopixel.RGB  # Instead of neopixel.GRB
```

## Auto-run on Boot (Optional)

Create a systemd service:

```bash
sudo nano /etc/systemd/system/neopixel.service
```

Add:
```ini
[Unit]
Description=NeoPixel Controller
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/neopixel_12/neopixel_controller.py
WorkingDirectory=/home/pi/neopixel_12
StandardOutput=inherit
StandardError=inherit
Restart=always
User=root

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable neopixel.service
sudo systemctl start neopixel.service
```

## License

Free to use and modify for personal and commercial projects.

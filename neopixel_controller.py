#!/usr/bin/env python3
"""
NeoPixel Ring (12 LEDs) Controller for Raspberry Pi 5
Control an Adafruit NeoPixel ring via GPIO
"""

import time
import board
import neopixel
from typing import Tuple

# NeoPixel Configuration
PIXEL_PIN = board.D18  # GPIO 18 (Pin 12) - Change if using different pin
NUM_PIXELS = 12        # Number of LEDs in the ring
BRIGHTNESS = 0.3       # Set brightness (0.0 to 1.0)
ORDER = neopixel.GRB   # Pixel color order (GRB for NeoPixels)

# Initialize NeoPixel strip
pixels = neopixel.NeoPixel(
    PIXEL_PIN, 
    NUM_PIXELS, 
    brightness=BRIGHTNESS, 
    auto_write=False,
    pixel_order=ORDER
)


def color_wipe(color: Tuple[int, int, int], wait: float = 0.05):
    """Wipe color across display one pixel at a time."""
    for i in range(NUM_PIXELS):
        pixels[i] = color
        pixels.show()
        time.sleep(wait)


def rainbow_cycle(wait: float = 0.05, iterations: int = 1):
    """Rainbow cycle animation."""
    for j in range(255 * iterations):
        for i in range(NUM_PIXELS):
            pixel_index = (i * 256 // NUM_PIXELS) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)


def wheel(pos: int) -> Tuple[int, int, int]:
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)


def theater_chase(color: Tuple[int, int, int], wait: float = 0.1, iterations: int = 10):
    """Theater chase animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, NUM_PIXELS, 3):
                if i + q < NUM_PIXELS:
                    pixels[i + q] = color
            pixels.show()
            time.sleep(wait)
            for i in range(0, NUM_PIXELS, 3):
                if i + q < NUM_PIXELS:
                    pixels[i + q] = (0, 0, 0)


def pulse(color: Tuple[int, int, int], wait: float = 0.02, steps: int = 50):
    """Pulse effect - fade in and out."""
    # Fade in
    for i in range(steps):
        brightness = i / steps
        scaled_color = tuple(int(c * brightness) for c in color)
        pixels.fill(scaled_color)
        pixels.show()
        time.sleep(wait)
    
    # Fade out
    for i in range(steps, 0, -1):
        brightness = i / steps
        scaled_color = tuple(int(c * brightness) for c in color)
        pixels.fill(scaled_color)
        pixels.show()
        time.sleep(wait)


def spinner(color: Tuple[int, int, int], wait: float = 0.1, iterations: int = 20):
    """Spinning single LED effect."""
    for j in range(iterations):
        for i in range(NUM_PIXELS):
            pixels.fill((0, 0, 0))
            pixels[i] = color
            pixels.show()
            time.sleep(wait)


def clear():
    """Turn off all pixels."""
    pixels.fill((0, 0, 0))
    pixels.show()


def demo():
    """Run a demonstration of various effects."""
    print("Starting NeoPixel demo...")
    
    try:
        print("Color wipe - Red")
        color_wipe((255, 0, 0))
        time.sleep(0.5)
        
        print("Color wipe - Green")
        color_wipe((0, 255, 0))
        time.sleep(0.5)
        
        print("Color wipe - Blue")
        color_wipe((0, 0, 255))
        time.sleep(0.5)
        
        print("Rainbow cycle")
        rainbow_cycle(wait=0.01, iterations=2)
        
        print("Theater chase - White")
        theater_chase((127, 127, 127))
        
        print("Pulse - Purple")
        pulse((255, 0, 255))
        pulse((255, 0, 255))
        
        print("Spinner - Cyan")
        spinner((0, 255, 255))
        
        print("Demo complete!")
        
    except KeyboardInterrupt:
        print("\nDemo interrupted")
    finally:
        clear()
        print("Cleared all pixels")


if __name__ == "__main__":
    try:
        demo()
    except KeyboardInterrupt:
        print("\nExiting...")
        clear()

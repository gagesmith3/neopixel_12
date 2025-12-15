#!/usr/bin/env python3
"""
Manual NeoPixel Ring Controller
Interactive control for individual LEDs and colors
"""

import time
import math
import random
import board
import neopixel
import sys

# NeoPixel Configuration
PIXEL_PIN = board.D18
NUM_PIXELS = 12
BRIGHTNESS = 0.3
ORDER = neopixel.GRB

# Initialize NeoPixel strip
pixels = neopixel.NeoPixel(
    PIXEL_PIN, 
    NUM_PIXELS, 
    brightness=BRIGHTNESS, 
    auto_write=False,
    pixel_order=ORDER
)


def clear_all():
    """Turn off all LEDs."""
    pixels.fill((0, 0, 0))
    pixels.show()
    print("All LEDs cleared")


def set_all(r, g, b):
    """Set all LEDs to the same color."""
    pixels.fill((r, g, b))
    pixels.show()
    print(f"All LEDs set to RGB({r}, {g}, {b})")


def set_pixel(index, r, g, b):
    """Set a single LED to a specific color."""
    if 0 <= index < NUM_PIXELS:
        pixels[index] = (r, g, b)
        pixels.show()
        print(f"LED {index} set to RGB({r}, {g}, {b})")
    else:
        print(f"Error: LED index must be between 0 and {NUM_PIXELS-1}")


def set_brightness(level):
    """Set overall brightness (0.0 to 1.0)."""
    if 0.0 <= level <= 1.0:
        pixels.brightness = level
        pixels.show()
        print(f"Brightness set to {level}")
    else:
        print("Error: Brightness must be between 0.0 and 1.0")


def show_status():
    """Display current LED status."""
    print(f"\n--- NeoPixel Status ---")
    print(f"Total LEDs: {NUM_PIXELS}")
    print(f"Brightness: {pixels.brightness}")
    print(f"\nCurrent LED Colors:")
    for i in range(NUM_PIXELS):
        color = pixels[i]
        print(f"  LED {i:2d}: RGB{color}")
    print()


def rainbow_cycle(wait=0.01, iterations=5):
    """Rainbow cycle animation."""
    print(f"Running rainbow animation...")
    try:
        for j in range(256 * iterations):
            for i in range(NUM_PIXELS):
                pixel_index = (i * 256 // NUM_PIXELS) + j
                pixels[i] = wheel(pixel_index & 255)
            pixels.show()
            time.sleep(wait)
        print("Animation complete")
    except KeyboardInterrupt:
        print("\nAnimation stopped")


def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)


def pulse(r, g, b, wait=0.02, steps=50, cycles=2):
    """Pulse effect - fade in and out."""
    print(f"Running pulse animation RGB({r}, {g}, {b})...")
    try:
        for _ in range(cycles):
            # Fade in
            for i in range(steps):
                brightness = i / steps
                scaled_color = (int(r * brightness), int(g * brightness), int(b * brightness))
                pixels.fill(scaled_color)
                pixels.show()
                time.sleep(wait)
            
            # Fade out
            for i in range(steps, 0, -1):
                brightness = i / steps
                scaled_color = (int(r * brightness), int(g * brightness), int(b * brightness))
                pixels.fill(scaled_color)
                pixels.show()
                time.sleep(wait)
        clear_all()
        print("Animation complete")
    except KeyboardInterrupt:
        print("\nAnimation stopped")


def spinner(r, g, b, wait=0.1, rotations=5):
    """Spinning single LED effect."""
    print(f"Running spinner animation RGB({r}, {g}, {b})...")
    try:
        for _ in range(rotations * NUM_PIXELS):
            for i in range(NUM_PIXELS):
                pixels.fill((0, 0, 0))
                pixels[i] = (r, g, b)
                pixels.show()
                time.sleep(wait)
        clear_all()
        print("Animation complete")
    except KeyboardInterrupt:
        print("\nAnimation stopped")


def theater_chase(r, g, b, wait=0.1, iterations=10):
    """Theater chase animation."""
    print(f"Running theater chase animation RGB({r}, {g}, {b})...")
    try:
        for j in range(iterations):
            for q in range(3):
                for i in range(0, NUM_PIXELS, 3):
                    if i + q < NUM_PIXELS:
                        pixels[i + q] = (r, g, b)
                pixels.show()
                time.sleep(wait)
                for i in range(0, NUM_PIXELS, 3):
                    if i + q < NUM_PIXELS:
                        pixels[i + q] = (0, 0, 0)
        clear_all()
        print("Animation complete")
    except KeyboardInterrupt:
        print("\nAnimation stopped")


def color_wipe(r, g, b, wait=0.05):
    """Wipe color across display one pixel at a time."""
    print(f"Running color wipe RGB({r}, {g}, {b})...")
    try:
        for i in range(NUM_PIXELS):
            pixels[i] = (r, g, b)
            pixels.show()
            time.sleep(wait)
        print("Animation complete")
    except KeyboardInterrupt:
        print("\nAnimation stopped")


def comet(r, g, b, wait=0.05, tail=4, laps=3):
    """Comet animation with a fading tail."""
    print(f"Running comet animation RGB({r}, {g}, {b})...")
    try:
        length = NUM_PIXELS * laps
        for step in range(length):
            head = step % NUM_PIXELS
            for i in range(NUM_PIXELS):
                distance = (head - i) % NUM_PIXELS
                if distance == 0:
                    pixels[i] = (r, g, b)
                elif 0 < distance <= tail:
                    fade = max(0, 1 - (distance / (tail + 1)))
                    pixels[i] = (int(r * fade), int(g * fade), int(b * fade))
                else:
                    pixels[i] = (0, 0, 0)
            pixels.show()
            time.sleep(wait)
        clear_all()
        print("Animation complete")
    except KeyboardInterrupt:
        print("\nAnimation stopped")


def scanner(r, g, b, wait=0.05, cycles=4, tail=3):
    """Larson scanner (KITT/Cylon) with fading tail."""
    print(f"Running scanner animation RGB({r}, {g}, {b})...")
    try:
        positions = list(range(NUM_PIXELS)) + list(range(NUM_PIXELS - 2, 0, -1))
        for _ in range(cycles):
            for head in positions:
                for i in range(NUM_PIXELS):
                    distance = abs(head - i)
                    if distance == 0:
                        pixels[i] = (r, g, b)
                    elif distance <= tail:
                        fade = max(0, 1 - (distance / (tail + 1)))
                        pixels[i] = (int(r * fade), int(g * fade), int(b * fade))
                    else:
                        pixels[i] = (0, 0, 0)
                pixels.show()
                time.sleep(wait)
        clear_all()
        print("Animation complete")
    except KeyboardInterrupt:
        print("\nAnimation stopped")


def twinkle(count=40, wait=0.05, decay=0.8):
    """Random twinkling pixels."""
    print("Running twinkle animation...")
    try:
        colors = [
            (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255),
            (255, 255, 0), (0, 255, 255), (255, 0, 255), (255, 128, 0)
        ]
        frame = [(0, 0, 0)] * NUM_PIXELS
        for _ in range(count):
            idx = random.randrange(NUM_PIXELS)
            frame[idx] = random.choice(colors)
            for i, (r, g, b) in enumerate(frame):
                frame[i] = (int(r * decay), int(g * decay), int(b * decay))
            pixels[:] = frame
            pixels.show()
            time.sleep(wait)
        clear_all()
        print("Animation complete")
    except KeyboardInterrupt:
        print("\nAnimation stopped")


def bounce(r, g, b, wait=0.05, width=3, cycles=6):
    """Color block bouncing around the ring."""
    print(f"Running bounce animation RGB({r}, {g}, {b})...")
    try:
        positions = list(range(NUM_PIXELS - width + 1)) + list(range(NUM_PIXELS - width - 1, -1, -1))
        for _ in range(cycles):
            for start in positions:
                pixels.fill((0, 0, 0))
                for i in range(width):
                    idx = (start + i) % NUM_PIXELS
                    pixels[idx] = (r, g, b)
                pixels.show()
                time.sleep(wait)
        clear_all()
        print("Animation complete")
    except KeyboardInterrupt:
        print("\nAnimation stopped")


def breath(r, g, b, wait=0.02, steps=120, cycles=3):
    """Smooth global breathing effect."""
    print(f"Running breath animation RGB({r}, {g}, {b})...")
    try:
        for _ in range(cycles):
            for i in range(steps):
                t = i / steps
                brightness = 0.5 - 0.5 * math.cos(math.pi * t)
                pixels.fill((int(r * brightness), int(g * brightness), int(b * brightness)))
                pixels.show()
                time.sleep(wait)
        clear_all()
        print("Animation complete")
    except KeyboardInterrupt:
        print("\nAnimation stopped")


def wheel_spin(wait=0.02, rotations=5):
    """Spinning rainbow gradient around the ring."""
    print("Running wheel animation...")
    try:
        for j in range(256 * rotations):
            for i in range(NUM_PIXELS):
                pixel_index = (i * 256 // NUM_PIXELS) + j
                pixels[i] = wheel(pixel_index & 255)
            pixels.show()
            time.sleep(wait)
        clear_all()
        print("Animation complete")
    except KeyboardInterrupt:
        print("\nAnimation stopped")


def wave(r, g, b, wait=0.03, cycles=4):
    """Sine-wave brightness around the ring."""
    print(f"Running wave animation RGB({r}, {g}, {b})...")
    try:
        frames = NUM_PIXELS * cycles
        for step in range(frames):
            phase = (2 * math.pi * step) / NUM_PIXELS
            for i in range(NUM_PIXELS):
                offset = (i / NUM_PIXELS) * 2 * math.pi
                amplitude = 0.5 * (1 + math.sin(phase + offset))
                pixels[i] = (int(r * amplitude), int(g * amplitude), int(b * amplitude))
            pixels.show()
            time.sleep(wait)
        clear_all()
        print("Animation complete")
    except KeyboardInterrupt:
        print("\nAnimation stopped")


def print_help():
    """Print available commands."""
    print("\n=== NeoPixel Manual Control ===")
    print("Commands:")
    print("  all <r> <g> <b>          - Set all LEDs to RGB color (0-255)")
    print("  set <led> <r> <g> <b>    - Set specific LED to RGB color")
    print("  clear                    - Turn off all LEDs")
    print("  brightness <0.0-1.0>     - Set brightness level")
    print("  status                   - Show current LED status")
    print("  preset <name>            - Load color preset")
    print("  help                     - Show this help message")
    print("  exit                     - Exit program")
    print("\nAnimations:")
    print("  rainbow                  - Rainbow cycle animation")
    print("  pulse <r> <g> <b>        - Pulsing/breathing effect")
    print("  spinner <r> <g> <b>      - Single LED spinner")
    print("  chase <r> <g> <b>        - Theater chase effect")
    print("  wipe <r> <g> <b>         - Color wipe effect")
    print("  comet <r> <g> <b>        - Comet with fading tail")
    print("  scanner <r> <g> <b>      - Larson scanner (KITT/Cylon)")
    print("  twinkle                  - Random twinkling pixels")
    print("  bounce <r> <g> <b>       - Bouncing color block")
    print("  breath <r> <g> <b>       - Smooth global breathing")
    print("  wheel                    - Spinning rainbow gradient")
    print("  wave <r> <g> <b>         - Sine wave brightness")
    print("\nPresets:")
    print("  red, green, blue, white, yellow, cyan, magenta, orange, purple")
    print("\nExamples:")
    print("  all 255 0 0              - All LEDs red")
    print("  set 0 0 255 0            - LED 0 green")
    print("  preset blue              - All LEDs blue")
    print("  rainbow                  - Run rainbow animation")
    print("  pulse 255 0 255          - Purple pulse effect")
    print("  spinner 0 255 0          - Green spinner")
    print("  comet 255 255 0          - Yellow comet")
    print("  scanner 0 255 255        - Cyan scanner")
    print("  bounce 255 128 0         - Orange bouncing block")
    print("  breath 0 0 255           - Blue breathing")
    print("  wheel                    - Rainbow wheel")
    print("  brightness 0.5           - Set 50% brightness")
    print()


def load_preset(name):
    """Load a color preset."""
    presets = {
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'white': (255, 255, 255),
        'yellow': (255, 255, 0),
        'cyan': (0, 255, 255),
        'magenta': (255, 0, 255),
        'orange': (255, 165, 0),
        'purple': (128, 0, 128),
        'pink': (255, 192, 203),
        'warm': (255, 147, 41),
        'cool': (64, 156, 255),
    }
    
    name = name.lower()
    if name in presets:
        r, g, b = presets[name]
        set_all(r, g, b)
    else:
        print(f"Error: Unknown preset '{name}'")
        print(f"Available presets: {', '.join(presets.keys())}")


def parse_command(command):
    """Parse and execute a command."""
    parts = command.strip().split()
    
    if not parts:
        return True
    
    cmd = parts[0].lower()
    
    try:
        if cmd == 'exit' or cmd == 'quit':
            return False
        
        elif cmd == 'help':
            print_help()
        
        elif cmd == 'clear':
            clear_all()
        
        elif cmd == 'status':
            show_status()
        
        elif cmd == 'all':
            if len(parts) == 4:
                r, g, b = int(parts[1]), int(parts[2]), int(parts[3])
                set_all(r, g, b)
            else:
                print("Usage: all <r> <g> <b>")
        
        elif cmd == 'set':
            if len(parts) == 5:
                index = int(parts[1])
                r, g, b = int(parts[2]), int(parts[3]), int(parts[4])
                set_pixel(index, r, g, b)
            else:
                print("Usage: set <led> <r> <g> <b>")
        
        elif cmd == 'brightness':
            if len(parts) == 2:
                level = float(parts[1])
                set_brightness(level)
            else:
                print("Usage: brightness <0.0-1.0>")
        
        elif cmd == 'preset':
            if len(parts) == 2:
                load_preset(parts[1])
            else:
                print("Usage: preset <name>")
        
        elif cmd == 'rainbow':
            rainbow_cycle()
        
        elif cmd == 'pulse':
            if len(parts) == 4:
                r, g, b = int(parts[1]), int(parts[2]), int(parts[3])
                pulse(r, g, b)
            else:
                print("Usage: pulse <r> <g> <b>")
        
        elif cmd == 'spinner':
            if len(parts) == 4:
                r, g, b = int(parts[1]), int(parts[2]), int(parts[3])
                spinner(r, g, b)
            else:
                print("Usage: spinner <r> <g> <b>")
        
        elif cmd == 'chase':
            if len(parts) == 4:
                r, g, b = int(parts[1]), int(parts[2]), int(parts[3])
                theater_chase(r, g, b)
            else:
                print("Usage: chase <r> <g> <b>")
        
        elif cmd == 'wipe':
            if len(parts) == 4:
                r, g, b = int(parts[1]), int(parts[2]), int(parts[3])
                color_wipe(r, g, b)
            else:
                print("Usage: wipe <r> <g> <b>")

        elif cmd == 'comet':
            if len(parts) == 4:
                r, g, b = int(parts[1]), int(parts[2]), int(parts[3])
                comet(r, g, b)
            else:
                print("Usage: comet <r> <g> <b>")

        elif cmd == 'scanner':
            if len(parts) == 4:
                r, g, b = int(parts[1]), int(parts[2]), int(parts[3])
                scanner(r, g, b)
            else:
                print("Usage: scanner <r> <g> <b>")

        elif cmd == 'twinkle':
            twinkle()

        elif cmd == 'bounce':
            if len(parts) == 4:
                r, g, b = int(parts[1]), int(parts[2]), int(parts[3])
                bounce(r, g, b)
            else:
                print("Usage: bounce <r> <g> <b>")

        elif cmd == 'breath':
            if len(parts) == 4:
                r, g, b = int(parts[1]), int(parts[2]), int(parts[3])
                breath(r, g, b)
            else:
                print("Usage: breath <r> <g> <b>")

        elif cmd == 'wheel':
            wheel_spin()

        elif cmd == 'wave':
            if len(parts) == 4:
                r, g, b = int(parts[1]), int(parts[2]), int(parts[3])
                wave(r, g, b)
            else:
                print("Usage: wave <r> <g> <b>")
        
        else:
            print(f"Unknown command: {cmd}")
            print("Type 'help' for available commands")
    
    except ValueError as e:
        print(f"Error: Invalid value - {e}")
    except Exception as e:
        print(f"Error: {e}")
    
    return True


def interactive_mode():
    """Run interactive command prompt."""
    print_help()
    
    try:
        while True:
            try:
                command = input("NeoPixel> ").strip()
                if not parse_command(command):
                    break
            except EOFError:
                break
    except KeyboardInterrupt:
        print("\n")
    finally:
        clear_all()
        print("Goodbye!")


if __name__ == "__main__":
    try:
        # Check for command-line arguments
        if len(sys.argv) > 1:
            command = ' '.join(sys.argv[1:])
            parse_command(command)
        else:
            interactive_mode()
    except KeyboardInterrupt:
        print("\nExiting...")
        clear_all()

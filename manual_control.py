#!/usr/bin/env python3
"""
Manual NeoPixel Ring Controller
Interactive control for individual LEDs and colors
"""

import time
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
    print("\nPresets:")
    print("  red, green, blue, white, yellow, cyan, magenta, orange, purple")
    print("\nExamples:")
    print("  all 255 0 0              - All LEDs red")
    print("  set 0 0 255 0            - LED 0 green")
    print("  preset blue              - All LEDs blue")
    print("  rainbow                  - Run rainbow animation")
    print("  pulse 255 0 255          - Purple pulse effect")
    print("  spinner 0 255 0          - Green spinner")
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

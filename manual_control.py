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
    print("\nPresets:")
    print("  red, green, blue, white, yellow, cyan, magenta, orange, purple")
    print("\nExamples:")
    print("  all 255 0 0              - All LEDs red")
    print("  set 0 0 255 0            - LED 0 green")
    print("  preset blue              - All LEDs blue")
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

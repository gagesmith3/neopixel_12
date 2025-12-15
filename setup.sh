#!/bin/bash
# Setup script for NeoPixel controller on Raspberry Pi 5

echo "=== NeoPixel Ring Setup Script ==="
echo ""

# Update system
echo "Updating system packages..."
sudo apt-get update

# Install dependencies
echo "Installing system dependencies..."
sudo apt-get install -y python3-pip python3-dev python3-venv

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install Python packages
echo "Installing Python dependencies..."
pip3 install --upgrade pip
pip3 install -r requirements.txt

echo ""
echo "=== Setup Complete! ==="
echo ""
echo "To run the demo:"
echo "  sudo python3 neopixel_controller.py"
echo ""
echo "Or activate the virtual environment first:"
echo "  source venv/bin/activate"
echo "  sudo python3 neopixel_controller.py"
echo ""

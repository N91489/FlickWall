#!/bin/bash

# Stop and disable the systemd service
echo "Stopping and disabling the FlickWall service..."
sudo systemctl stop FlickWall.service
sudo systemctl disable FlickWall.service

# Remove the systemd service file
SERVICE_FILE="/etc/systemd/system/FlickWall.service"
if [ -f "$SERVICE_FILE" ]; then
    echo "Removing the systemd service file..."
    sudo rm "$SERVICE_FILE"
else
    echo "Service file not found."
fi

# Reload systemd daemon
sudo systemctl daemon-reload

# Remove the program folder from /opt
PROGRAM_DIR="/opt/FlickWall"
if [ -d "$PROGRAM_DIR" ]; then
    echo "Removing the program folder from /opt..."
    sudo rm -rf "$PROGRAM_DIR"
else
    echo "Program folder not found."
fi

# Remove the .env file (if not already inside /opt)
if [ -f ".env" ]; then
    echo "Removing the .env file..."
    rm .env
else
    echo ".env file not found."
fi

echo "Uninstallation completed."

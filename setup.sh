#!/bin/bash

# Function to install Python3 based on the detected Linux distro
install_python3() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        case "$ID" in
            ubuntu|debian)
                sudo apt update && sudo apt install -y python3 python3-pip
                ;;
            fedora)
                sudo dnf install -y python3 python3-pip
                ;;
            rhel|centos)
                sudo yum install -y python3 python3-pip
                ;;
            gentoo)
                sudo emerge --ask dev-lang/python
                ;;
            arch|manjaro)
                sudo pacman -Syu python python-pip
                ;;
            suse|opensuse)
                sudo zypper install -y python3 python3-pip
                ;;
            *)
                echo "Unsupported Linux distribution: $ID"
                exit 1
                ;;
        esac
    else
        echo "Cannot detect Linux distribution. Please install Python3 manually."
        exit 1
    fi
}

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Installing Python3..."
    install_python3
else
    echo "Python3 is already installed."
fi

# Check if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing packages from requirements.txt..."
    python3 -m pip install -r requirements.txt
else
    echo "requirements.txt not found."
    exit 1
fi

# Ask for API key and store it in a .env file
echo "Please enter your API key from https://developer.themoviedb.org/reference/intro/authentication :"
read -r api_key

# Create or overwrite the .env file with the API key
echo "TMDB_API_KEY=$api_key" > .env
echo "API key saved to .env file."

# Create a systemd service to run the Python script after the system starts and internet is connected, but only once
echo "Setting up a service for flickwall"

SERVICE_FILE="/etc/systemd/system/flickwall.service"
cat <<EOF > $SERVICE_FILE

[Unit]
Description=Runs FlickWall Once After System Start and Network is Online
Wants=network-online.target
After=network-online.target

[Service]
Type=oneshot
User=$(whoami)
WorkingDirectory=/opt/flickwall
ExecStart=/usr/bin/python3 /opt/flickwall/request.py
RemainAfterExit=true

[Install]
WantedBy=network-online.target

EOF

# Move Script to /opt/flickwall
sudo mkdir -p /opt/flickwall
sudo mv -r $(pwd)/flickwall /opt/flickwall

# Reload systemd and enable the service
sudo systemctl daemon-reload
sudo systemctl enable python-network-check.service

echo "Systemd service created and enabled. Your script will run automatically once after boot and when the internet is connected."

echo "All done!"

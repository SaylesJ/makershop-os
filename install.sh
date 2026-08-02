#!/bin/bash

# MakerShop OS - Automated Installer for Debian/Ubuntu (Proxmox LXC)

echo "Starting MakerShop OS Installation..."

# 1. Update system and install Python/pip
echo "Updating packages..."
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv git

# 2. Setup application directory
APP_DIR="/opt/makershop-os"
echo "Moving application to $APP_DIR..."
sudo mkdir -p $APP_DIR
sudo cp -r ./* $APP_DIR/
sudo chown -R $USER:$USER $APP_DIR

# 3. Create a Python Virtual Environment and install requirements
cd $APP_DIR
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Create the Systemd Service to keep the app running in the background
SERVICE_FILE="/etc/systemd/system/makershop.service"

echo "Creating systemd service..."
sudo bash -c "cat > $SERVICE_FILE" << EOL
[Unit]
Description=MakerShop OS Flask Application
After=network.target

[Service]
User=$USER
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
ExecStart=$APP_DIR/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
EOL

# 5. Enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable makershop
sudo systemctl start makershop

# 6. Get the local IP address
LOCAL_IP=$(hostname -I | awk '{print $1}')

echo "====================================================="
echo "✅ MakerShop OS successfully installed and running!"
echo "🌐 Access your dashboard at: http://$LOCAL_IP:5001"
echo "====================================================="
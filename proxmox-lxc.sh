#!/usr/bin/env bash

# MakerShop OS - Proxmox LXC Auto-Creator
echo "Starting MakerShop OS Proxmox LXC Creation..."

# 1. Get next available container ID
CTID=$(pvesh get /cluster/nextid)
echo "Assigning Container ID: $CTID"

# 2. Download the latest Debian 12 template silently
echo "Fetching Debian 12 template..."
pveam update >/dev/null
TEMPLATE=$(pveam available -section system | grep debian-12 | awk '{print $2}' | head -n 1)
pveam download local $TEMPLATE >/dev/null

# 3. Create the LXC container (1GB RAM, 1 Core, 4GB Storage, DHCP)
echo "Building the container..."
pct create $CTID local:vztmpl/${TEMPLATE##*/} \
    --arch amd64 \
    --hostname makershop-os \
    --cores 1 \
    --memory 1024 \
    --swap 512 \
    --net0 name=eth0,bridge=vmbr0,ip=dhcp \
    --storage local-lvm \
    --rootfs local-lvm:4 \
    --unprivileged 1 \
    --features nesting=1

# 4. Start the container
echo "Starting container and waiting for network..."
pct start $CTID
sleep 10 # Give DHCP a few seconds to assign an IP

# 5. Execute the installation inside the new container
echo "Installing MakerShop OS inside the container..."
# NOTE: Replace YourUsername below with your actual GitHub username
pct exec $CTID -- bash -c "apt-get update && apt-get install -y git sudo && git clone https://github.com/SaylesJ/makershop-os.git /opt/makershop-os && cd /opt/makershop-os && chmod +x install.sh && ./install.sh"

# 6. Retrieve the IP address and display it
IP=$(pct exec $CTID -- hostname -I | awk '{print $1}')

echo ""
echo "========================================================="
echo "✅ MakerShop OS LXC Container Created Successfully!"
echo "🌐 Access your dashboard at: http://$IP:5001"
echo "========================================================="

# MakerShop OS

A lightweight, local-first inventory, scheduling, and project management system built specifically for makers, CNC operators, laser engravers, and 3D printing workflows.

## Features
* **Machine & Material Customization:** Manage your custom filaments, router bit sizes, and spindle/router configurations.
* **Safety Notice:** Built-in calculation guidelines emphasizing custom feeds and speeds if you aren't using a DeWalt 611 trim router.
* **Database Backup & Restore:** Easily download a secure backup of your shop data or restore from a previous `.db` file straight through the web UI.

---

## 🚀 Proxmox 1-Click Installation
If you are running Proxmox VE, you can run this single command directly in your **Proxmox Node Shell**. It will automatically create a lightweight Debian 12 LXC container and install MakerShop OS for you:

```bash
bash -c "$(wget -qLO - [https://raw.githubusercontent.com/SaylesJ/makershop-os/main/proxmox-lxc.sh](https://raw.githubusercontent.com/SaylesJ/makershop-os/main/proxmox-lxc.sh))"

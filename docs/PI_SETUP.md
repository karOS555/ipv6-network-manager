# Raspberry Pi Headless Setup Guide

This guide explains how to prepare your physical Raspberry Pi for integration with the IPv6 Network Manager without using a monitor or keyboard.

## 1. Flashing the OS
Use the official **Raspberry Pi Imager** to install **Raspberry Pi OS Lite (64-bit)**.

* Click the **Gear Icon** (Advanced Options) before flashing.
* **Hostname:** pi-simulated-device (or your preferred name).
* **Enable SSH:** Select "Use password authentication".
* **Configure Wireless LAN:** Enter your Hotspot/Wi-Fi SSID and password. Set the Wireless LAN country to your current location (e.g., DE).
* **Set Username/Password:** Create a user (e.g., `admin`). **Remember these credentials for the Python app.**

## 2. Initial System Preparation
Once the Pi has booted and you have connected via SSH (`ssh admin@pi-simulated-device.local`), run the following commands:

`sudo apt update && sudo apt upgrade -y`
`sudo apt install -y radvd ndisc6 iproute2`

## 3. IPv6 Gateway Configuration
To allow the Pi to act as a router/gateway, IPv6 forwarding must be enabled:

`sudo sysctl -w net.ipv6.conf.all.forwarding=1`

To assign the static project IP address to the wireless interface:
`sudo ip -6 addr add 2001:db8:1::1/64 dev wlan0`

## 4. radvd Configuration (SLAAC)
To distribute the IPv6 prefix to other devices in the network, configure the Router Advertisement Daemon. 
Create the file `/etc/radvd.conf`:

`sudo nano /etc/radvd.conf`

Paste the following configuration:

interface wlan0 {
    AdvSendAdvert on;
    MinRtrAdvInterval 3;
    MaxRtrAdvInterval 10;
    prefix 2001:db8:1::/64 {
        AdvOnLink on;
        AdvAutonomous on;
    };
};



Restart and enable the service:
`sudo systemctl restart radvd`
`sudo systemctl enable radvd`

## 5. Verification
Check if the static IP is active:
`ip -6 addr show wlan0`

Verify that the Pi is reachable from your laptop:
`ping -6 2001:db8:1::1` (Windows)
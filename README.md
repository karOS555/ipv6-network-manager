# ipv6-network-manager

This is a school project created to monitor and manage a local IPv6 network. The tool allows to see all active devices in the network and change their configurations from a central dashboard.


## What it does

The application is designed to handle both physical hardware like Raspberry Pis or similar devices running Linux and simulated nodes running in Docker.

* Device Discovery: Scans the network using IPv6 multicast and the neighbor cache to find active nodes.

* Monitoring: Displays information for each device, such as the operating system version and current IPv6 addresses.

* Remote Config: Allows to toggle services like SLAAC or DHCPv6 and change IP settings on the remote devices via SSH.

* Simulation: Supports Docker containers to test the management features without needing multiple physical devices.


## Technical Setup

* Language: Python
* Frontend: Streamlit (for the web-based dashboard)
* Backend: Paramiko for SSH communication and SQLite for storing device data.
* Automation: A basic CI pipeline is set up with GitHub Actions to run tests on every push.


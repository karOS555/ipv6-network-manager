# Network Simulation Guide

To test the IPv6 Manager without needing multiple physical Raspberry Pis, this project uses a dynamic Docker simulation.

## Architecture
The simulation consists of a dedicated virtual IPv6 bridge network (`lab_network`) and lightweight Linux containers acting as managed nodes.



### Components
* **Base Image:** A custom Alpine Linux image (`my-ipv6-node`) with an SSH server and networking tools installed.
* **Network:** A Docker Bridge network configured with the IPv6 subnet `2001:db8:1::/64`.
* **Orchestration:** The Python backend (`backend.py`) uses the Docker SDK to automatically create, start, and stop containers directly from the dashboard sidebar.

## Setup & Usage

**1. Prepare the Image**
You only need to build the base image once. Run this in your terminal:
`docker build -t my-ipv6-node .`

**2. Start Simulation**
* Open the **IPv6 Network Manager** dashboard.
* In the Sidebar under **"Simulation Lab"**, select the number of nodes (e.g., 3).
* Click **"Start Simulation"**.

The application will automatically:
1. Check if `lab_network` exists (and create it if missing).
2. Spin up the containers with static IPv6 addresses starting at `2001:db8:1::11`.
3. Register them in the internal database.

**3. Stop Simulation**
Click **"Stop All Nodes"** in the sidebar to cleanly remove all simulation containers and free up resources.
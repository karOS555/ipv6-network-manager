# IPv6 Network Manager

This is a school project created to monitor and manage a local IPv6 network. The tool allows users to discover active devices in the network and change their configurations from a central dashboard.

## What it does

The application handles both physical hardware (like Raspberry Pis running Linux) and simulated nodes running in Docker.

* **Device Discovery:** Scans the network using IPv6 multicast (`ff02::1`) and parses the neighbor cache to identify active nodes automatically.
* **Monitoring:** Displays real-time information for each device, including operating system version, hostname, and active IPv6 addresses.
* **Remote Config:** Enables remote administration via SSH, allowing users to execute commands, change IP settings, or toggle services like SLAAC.
* **Simulation Lab:** Features a built-in "Simulation Mode" that uses the Docker SDK to spawn virtual Linux clients instantly, allowing for full-scale network testing without physical hardware.



## Technical Architecture

The project follows a modular design pattern separating logic, data, and presentation:

* **Language:** Python 3.10+
* **Frontend:** Streamlit (Web-based Dashboard)
* **Backend:** * `backend.py`: Handles business logic, network scanning, and Docker orchestration.
    * `paramiko`: Manages secure SSH connections to nodes.
* **Persistence:** SQLite (`network.db`) stores discovered devices and their state to ensure data persists across restarts.
* **CI/CD:** Automated testing pipeline using GitHub Actions (Linting & Unit Tests).

## Getting Started

### Prerequisites
* Python 3.9 or higher
* Docker Desktop (with IPv6 enabled in Docker Engine)

### Installation
1. Clone the repository:
   `git clone https://github.com/karOS555/ipv6-network-manager.git`
2. Create and activate a virtual environment:
   `python -m venv venv`
   # Windows:
   `.\venv\Scripts\activate`
3. Install dependencies:
   `pip install -r requirements.txt`
4. Build the simulation image:
   `docker build -t my-ipv6-node .`

### Usage
Simply run the start script to launch the dashboard:
* **Windows:** Double-click `run_app.bat`

Alternatively, run manually:
`streamlit run app.py`
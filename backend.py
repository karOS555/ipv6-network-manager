import subprocess
import platform
import socket
import docker
import paramiko
from database import upsert_device, update_device_details

# --- DOCKER SIMULATION ---
def create_simulation_nodes(count):
    """Creates N docker containers based on the alpine image."""
    try:
        client = docker.from_env()
        # check if network exists, else create one
        networks = client.networks.list(names=["lab_network"])
        if not networks:
            network = client.networks.create("lab_network", driver="bridge", ipv6_enabled=True, 
                                             ipam={"Config": [{"Subnet": "2001:db8:1::/64"}]})
        else:
            network = networks[0]

        created_nodes = []
        for i in range(1, count + 1):
            node_name = f"sim-node-{i}"
            # start container (fi not already running)
            try:
                client.containers.get(node_name) # check if it exists
            except docker.errors.NotFound:
                ip_addr = f"2001:db8:1::{10+i}"
                client.containers.run(
                    "my-ipv6-node", # image name
                    name=node_name,
                    hostname=node_name,
                    detach=True,
                    network="lab_network",
                    mac_address=f"02:42:ac:11:00:{10+i}", # Staatic MAC für Recognition
                )
                # connect Network with static IP (Docker SDK Workaround for static IPv6)
                upsert_device(ip_addr, f"02:42:ac:11:00:{10+i}", "Simulation (Docker)")
                created_nodes.append(node_name)
        return True, f"Created {len(created_nodes)} nodes."
    except Exception as e:
        return False, str(e)

def destroy_simulation():
    client = docker.from_env()
    containers = client.containers.list(filters={"ancestor": "my-ipv6-node"})
    for c in containers:
        c.remove(force=True)

# --- NETWORK DISCOVERY ---
def scan_network():
    """Pings multicast and reads neighbor table (Windows compatible)."""
    # 1. Multicast Ping (wakes all devices up)
    subprocess.run(["ping", "-n", "2", "-6", "ff02::1"], capture_output=True)
    
    # 2. read neighbor table
    cmd = ["netsh", "interface", "ipv6", "show", "neighbors"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    
    count = 0
    if res.returncode == 0:
        lines = res.stdout.split("\n")
        for line in lines:
            parts = line.split()
            # simple IPv6 adress filtering (Global & Link Local)
            if len(parts) > 2 and ("2001:db8" in parts[0] or "fe80" in parts[0]):
                ip = parts[0]
                mac = parts[1]
                # filter out multicast adresses
                if not ip.startswith("ff"):
                    upsert_device(ip, mac, "Physical/Discovered")
                    count += 1
    return count

# --- REMOTE MANAGEMENT (SSH) ---
def get_remote_details(ip, user="administrator", pwd="root123"): # pwd for simulations
    """Connects via SSH to fetch hostname and OS."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        # Timeout, if device offline
        client.connect(ip, username=user, password=pwd, timeout=3)
        
        # OS Version abfragen
        stdin, stdout, stderr = client.exec_command("cat /etc/os-release | grep PRETTY_NAME")
        os_name = stdout.read().decode().replace("PRETTY_NAME=", "").strip().replace('"', '')
        
        # Hostname abfragen
        stdin, stdout, stderr = client.exec_command("hostname")
        hostname = stdout.read().decode().strip()
        
        update_device_details(ip, hostname, os_name)
        client.close()
        return True, "Details updated"
    except Exception as e:
        return False, str(e)

def send_ssh_command(ip, command, user="administrator", pwd="root123"):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(ip, username=user, password=pwd, timeout=3)
        stdin, stdout, stderr = client.exec_command(command)
        out = stdout.read().decode()
        err = stderr.read().decode()
        client.close()
        return True, out + err
    except Exception as e:
        return False, str(e)
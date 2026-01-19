import streamlit as st
import subprocess
import platform
import pandas as pd

st.set_page_config(page_title="IPv6 Network Manager", layout="wide")

st.title("🌐 IPv6 Network Manager")
st.write("Management Console for Physical and Simulated Nodes")

# Sidebar for status overview
st.sidebar.header("System Status")
st.sidebar.info("Connected to Mobile Hotspot")

# Layout with collums
col1, col2 = st.columns(2)

with col1:
    st.header("Physical Devices")
    pi_ip = "2001:db8:1::1" 
    if st.button("Ping Raspberry Pi"):
        # secure methode for Windows:
        # -n 1: just one packet
        # -6: force IPv6
        cmd = ["ping", "-n", "1", "-6", pi_ip]
        
        res = subprocess.run(cmd, capture_output=True, text=True, shell=True) # shell=True hilft oft unter Windows
        
        if res.returncode == 0:
            st.success(f"Pi {pi_ip} is reachable!")
            st.text(res.stdout) # Shows output
        else:
            st.error("Pi is not reachable.")
            st.text(res.stderr) # Shows error message

with col2:
    st.header("Simulated Nodes (Docker)")
    docker_ip = "2001:db8:1::10"
    if st.button(f"Ping Docker Node 1"):
        # docker exec, if direct Ping not working
        command = ["docker", "exec", "node1", "ping", "-c", "1", "2001:db8:1::20"]
        res = subprocess.run(command, capture_output=True, text=True)
        
        if res.returncode == 0:
            st.success("Docker Network Internal: Node 1 can see Node 2!")
            st.code(res.stdout)
        else:
            st.error("Docker Internal Communication failed.")


st.header("🔍 Network Discovery")

if st.button("Scan IPv6 Network"):
    with st.spinner("Scanning via Multicast (ff02::1)..."):
        # ping All-Nodes Multicast Adress
        # wakes all devices
        subprocess.run(["ping", "-n", "2", "-6", "ff02::1"], capture_output=True, shell=True)
        
        # reading neighbor cache (neighbor table)
        res = subprocess.run(["netsh", "interface", "ipv6", "show", "neighbors"], capture_output=True, text=True, shell=True)
        
        if res.returncode == 0:
            # filtering output
            # searching for collumns wich include 2001:db8 or fe80
            lines = res.stdout.split("\n")
            discovered_devices = []
            
            for line in lines:
                if "2001:db8" in line or "fe80" in line:
                    parts = line.split()
                    if len(parts) >= 3:
                        discovered_devices.append({
                            "IP Address": parts[0],
                            "MAC Address": parts[1],
                            "State": parts[2]
                        })
            
            if discovered_devices:
                df = pd.DataFrame(discovered_devices)
                st.table(df)
            else:
                st.warning("No devices found in neighbor cache.")
        else:
            st.error("Could not retrieve neighbor table.")
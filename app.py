import streamlit as st
import pandas as pd
import backend
import database
import time

# Initialisierung
database.init_db()
st.set_page_config(page_title="IPv6 NetManager", page_icon="🌐", layout="wide")

# --- HEADER & LINKS ---
st.title("🌐 IPv6 Network Manager")
st.markdown("""
**Repository:** [github.com/karOS555/ipv6-network-manager](https://github.com/karOS555/ipv6-network-manager) | 
**Status:** Active | **User:** Admin
""")
st.divider()

# --- SIDEBAR: SIMULATION CONTROL ---
st.sidebar.header("⚙️ Simulation Lab")
st.sidebar.caption("Docker Container Management")
num_nodes = st.sidebar.number_input("Count of Nodes", min_value=1, max_value=10, value=2)

if st.sidebar.button("🚀 Start Simulation"):
    with st.spinner("Starting containers..."):
        success, msg = backend.create_simulation_nodes(num_nodes)
        if success:
            st.sidebar.success(msg)
            time.sleep(1)
            st.rerun()
        else:
            st.sidebar.error(f"Error: {msg}")

if st.sidebar.button("🛑 Stop All Nodes"):
    backend.destroy_simulation()
    st.sidebar.warning("Simulation destroyed.")

# --- DASHBOARD METRICS ---
col1, col2, col3 = st.columns(3)
devices = database.get_all_devices()
with col1:
    st.metric("Total Devices", len(devices))
with col2:
    st.metric("IPv6 Prefix", "2001:db8:1::/64")
with col3:
    st.metric("Interface", "Wi-Fi (Host)")

# --- DISCOVERY SECTION ---
st.subheader("📡 Device Discovery")
c1, c2 = st.columns([1, 4])
if c1.button("Scan Network Now"):
    with st.spinner("Multicast Pinging..."):
        count = backend.scan_network()
        st.success(f"Scan complete. Found {count} new entries.")
        time.sleep(1)
        st.rerun()

# show table
if devices:
    df = pd.DataFrame(devices)
    # rename collumns for better view
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("No devices found yet. Start a scan.")

st.divider()

# --- DEVICE MANAGEMENT DETAILS ---
st.subheader("🛠 Device Configuration")
selected_ip = st.selectbox("Select Target Device", [d['ip'] for d in devices] if devices else [])

if selected_ip:
    # find dataset
    device = next((item for item in devices if item["ip"] == selected_ip), None)
    
    # 3 collumn layout for actions
    ac1, ac2, ac3 = st.columns(3)
    
    with ac1:
        st.info(f"**Selected:** {device['hostname']} ({device['type']})")
        if st.button("🔄 Fetch OS Details (SSH)"):
            ok, msg = backend.get_remote_details(selected_ip) # standart pwd for sim
            if ok: 
                st.success("Updated!") 
                st.rerun()
            else: 
                st.error(msg)
                
    with ac2:
        st.write("**Quick Actions**")
        if st.button("Ping Device"):
            # Ping logic
            import subprocess
            res = subprocess.run(["ping", "-n", "1", "-6", selected_ip], capture_output=True, text=True)
            if res.returncode == 0:
                st.success("Reply received!")
            else:
                st.error("Request timed out.")
                
    with ac3:
        st.write("**Configuration**")
        action = st.selectbox("Action", ["Set Static IP", "Enable SLAAC", "Reboot"])
        
        if action == "Set Static IP":
            new_ip = st.text_input("New IPv6 Address", "2001:db8:1::99/64")
            cmd = f"ip addr add {new_ip} dev eth0"
        elif action == "Enable SLAAC":
            cmd = "sysctl -w net.ipv6.conf.eth0.accept_ra=1"
        elif action == "Reboot":
            cmd = "reboot"
            
        if st.button(f"Execute: {action}"):
            ok, out = backend.send_ssh_command(selected_ip, cmd)
            if ok:
                st.success("Command executed.")
                st.code(out)
            else:
                st.error(f"Failed: {out}")
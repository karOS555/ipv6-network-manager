import paramiko

# Connection details
host = "pi-simulated-device.local" # or ip-adress
user = "administrator"
password = "root123"

def get_pi_version():
    try:
        # Initalize SSH Client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # establish connection
        print(f"Connecting to {host}...")
        client.connect(hostname=host, username=user, password=password)
        
        # Run command
        stdin, stdout, stderr = client.exec_command("uname -a")
        output = stdout.read().decode('utf-8')
        
        print("Success! Pi Output:")
        print(output)
        
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_pi_version()
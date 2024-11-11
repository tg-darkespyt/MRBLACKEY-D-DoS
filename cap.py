import socket

UDP_IP = "0.0.0.0"
PORT = 39418
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, PORT))
print(f"Listening for UDP packets on {UDP_IP}:{PORT}...\n")
while True:
    try:
        data, addr = sock.recvfrom(4096)
        if data:
            print(data)
    except KeyboardInterrupt:
        print("\nUDP server shutting down.")
        break
    except Exception as e:
        print(f"Error: {e}")
        continue
        
import socket

sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
sniffer.bind(("0.0.0.0", 0))
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
print("Capturing outgoing requests...")
try:
    while True:
        raw_data, addr = sniffer.recvfrom(65565)
        print(f"Packet captured from {addr}: {raw_data}")
except KeyboardInterrupt:
    print("Stopped capturing.")
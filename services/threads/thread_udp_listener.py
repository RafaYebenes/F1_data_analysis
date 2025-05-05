import socket

# thread_udp_listener.py
def udp_listener(queue):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 20778))
    while True:
        data, _ = sock.recvfrom(65535)
        queue.put(data)

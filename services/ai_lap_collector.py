import socket
import struct
import csv
import time

UDP_IP = "0.0.0.0"
UDP_PORT = 20778
BUFFER_SIZE = 2048

# Estructuras y configuraciones
HEADER_FORMAT = "<HBBBBQfII2B"
# H (2) + B(1)x4 + Q(8) + f(4) + I(4)x2 + B(1)x2 = 2 + 4 + 8 + 4 + 8 + 2 = 28 bytes

PACKET_ID_MOTION = 0
PACKET_ID_LAPDATA = 2
PACKET_ID_PARTICIPANTS = 4

target_ai_car_idx = None
current_lap_number = {}

output_file = "motion_ai_data.csv"

# CSV setup
CSV_FIELDS = [
    "timestamp", "lap_number", "car_idx",
    "posX", "posY", "posZ",
    "velX", "velY", "velZ",
    "forwardX", "forwardY", "forwardZ",
    "rightX", "rightY", "rightZ",
    "gLat", "gLong", "gVert",
    "yaw", "pitch", "roll"
]

def parse_header(data):
    return struct.unpack(HEADER_FORMAT, data[:28])

def get_float(data, offset):
    return struct.unpack_from("<f", data, offset)[0]

def get_int16(data, offset):
    return struct.unpack_from("<h", data, offset)[0] / 32767.0  # normalizado

def parse_motion_packet(data, car_idx, lap_number):
    base = 24 + car_idx * 60
    motion_data = {
        "timestamp": time.time(),
        "lap_number": lap_number,
        "car_idx": car_idx,
        "posX": get_float(data, base),
        "posY": get_float(data, base + 4),
        "posZ": get_float(data, base + 8),
        "velX": get_float(data, base + 12),
        "velY": get_float(data, base + 16),
        "velZ": get_float(data, base + 20),
        "forwardX": get_int16(data, base + 24),
        "forwardY": get_int16(data, base + 26),
        "forwardZ": get_int16(data, base + 28),
        "rightX": get_int16(data, base + 30),
        "rightY": get_int16(data, base + 32),
        "rightZ": get_int16(data, base + 34),
        "gLat": get_float(data, base + 36),
        "gLong": get_float(data, base + 40),
        "gVert": get_float(data, base + 44),
        "yaw": get_float(data, base + 48),
        "pitch": get_float(data, base + 52),
        "roll": get_float(data, base + 56),
    }
    return motion_data

def parse_lapdata_packet(data):
    global target_ai_car_idx, current_lap_number
    for i in range(22):
        base = 24 + i * 53
        result_status = data[base + 41]
        current_lap = data[base + 32]
        current_lap_number[i] = current_lap

        if target_ai_car_idx is None and result_status == 2:  # en pista
            target_ai_car_idx = i
            print(f"✅ Objetivo fijado: IA en pista (car_idx={i})")

def parse_participants_packet(data):
    global target_ai_car_idx
    for i in range(22):
        base = 25 + i * 56
        m_aiControlled = data[base]
        if m_aiControlled == 1 and target_ai_car_idx is None:
            print(f"Detectada IA en car_idx {i}, esperando a que salga a pista...")
            break

def start_capture():
    print(f"📡 Escuchando en {UDP_IP}:{UDP_PORT}...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    with open(output_file, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=CSV_FIELDS)
        writer.writeheader()

        try:
            while True:
                data, _ = sock.recvfrom(BUFFER_SIZE)
                header = parse_header(data)
                packet_id = header[5]

                if packet_id == PACKET_ID_PARTICIPANTS:
                    parse_participants_packet(data)
                elif packet_id == PACKET_ID_LAPDATA:
                    parse_lapdata_packet(data)
                elif packet_id == PACKET_ID_MOTION and target_ai_car_idx is not None:
                    lap = current_lap_number.get(target_ai_car_idx, 0)
                    row = parse_motion_packet(data, target_ai_car_idx, lap)
                    print("vuelta", row)
                    writer.writerow(row)

        except KeyboardInterrupt:
            print("\n🛑 Captura detenida por el usuario.")
            print(f"📁 Datos guardados en {output_file}")

if __name__ == "__main__":
    start_capture()

import ctypes
import socket
from datetime import datetime
from resources.utils import *
from interfaces.interfaces import *
import redis
from services.parser import route_packet
from services.realtime_live_data import *

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)


class F1Reader:
    
    def __init__(self, ip='0.0.0.0', port=20778):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.packet_handlers = get_packet_handlers(self)
        self.sock.bind((ip, port))

    
    def start(self):
        print("🎮 Esperando paquetes UDP de F1...")

        while True:

            data, address = self.sock.recvfrom(65535)
            
            header = PacketHeader.from_buffer_copy(data[:ctypes.sizeof(PacketHeader)])
            packet_id = header.packetId
            
            parsed_data = route_packet(packet_id, data)
            parsed_data = parsed_data or {}

            parsed_data['packet_id'] = packet_id
            parsed_data['timestamp'] = datetime.utcnow().isoformat()
            parsed_data['session_uid'] = str(header.sessionUID)
            parsed_data['car_index'] = header.playerCarIndex
            ##createFile(parsed_data, "parsedData")

            updated_data = ""

            if packet_id in {1, 2, 6, 7}:  # Solo si es Session, Lap Data, Car Telemetry o Car Status
                updated_data = update_live_data(parsed_data, 'car_data')
                
            if packet_id == 10:
                updated_data = get_damage_info(parsed_data, 'car_damage')
            
            self.save_to_redis(updated_data)
            yield updated_data
    
    

    
    def save_to_redis(self, data, channel):
        try: 
            redis_client.publish(channel, data)
            print("✅ Datos guardados correctamente en Redis")
        except Exception as e:
            print(f"❌ Error al guardar datos en Redis: {e}")


if __name__ == '__main__':
    reader = F1Reader()
    for packet in reader.start():
        print(packet)

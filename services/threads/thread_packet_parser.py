from resources.utils import *
from interfaces.interfaces import *
import parser
from services.realtime_live_data import get_track_heat_map

# thread_packet_parser.py
def packet_parser(queue, redis_client):
    while True:
        data = queue.get()
        # Extraer packet_id y parsear
        header = PacketHeader.from_buffer_copy(data[:24])
        packet_id = header.packetId
        parsed_data = parser.route_packet(packet_id, data)

        # Lógica condicional (ej. heatmap, dashboard, etc.)
        if packet_id in {0, 6}:
            heatmap_point = get_track_heat_map(parsed_data)
            if heatmap_point:
                redis_client.rpush("trackHeatMap", heatmap_point)

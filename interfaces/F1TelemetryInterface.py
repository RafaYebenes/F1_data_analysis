import socket
import json
from datetime import datetime


class F1TelemetryInterface:
    def __init__(self, ip='0.0.0.0', port=20777):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ip, self.port))
        self.sock.settimeout(0.1)

    def read_data(self):
        try:
            data, _ = self.sock.recvfrom(2048)  # Tamaño máximo de paquete
            if data:
                raw_data = data.hex()
                parsed_data = self.parse_data(data)
                parsed_data['timestamp'] = datetime.now().isoformat()
                return parsed_data
        except socket.timeout:
            pass
        except Exception as e:
            print(f"❌ Error al leer datos de F1 24: {e}")
        return None

    def parse_data(self, data):
        # Aquí se debe implementar el parser real de datos de F1 24.
        # Por ahora, devolvemos el data bruto en hexadecimal para análisis posterior.
        return {'raw_data': data.hex()}


if __name__ == "__main__":
    f1_interface = F1TelemetryInterface()
    while True:
        f1_data = f1_interface.read_data()

        if f1_data:
            print(f"✅ Datos capturados de F1 24: {f1_data}")

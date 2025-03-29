import mmap
import struct
from datetime import datetime


class AssettoCorsaInterface:
    def __init__(self):
        self.physics_layout = 'ifffiiffffffff 4f 4f 4f 4f 4f 4f 4f 4f 4f 4f 4f 4f 4f 4f 4f 4f 4f 4f 4f 4f 4f 4f 4f 4f 4f 4f 4f 4f 4f 4f 4f 4f 4f 4f 4f 4f 4f 4f 4f 4f 4f 4f 4f 4f 4f 4f 4f 4f'
        self.fields = [
            'packetId', 'throttle', 'brake', 'fuel_consumption', 'gear', 'rpm', 'steerAngle', 'speed',
            'position_x', 'position_y', 'position_z', 'accGX', 'accGY', 'accGZ',
            'wheelSlipFL', 'wheelSlipFR', 'wheelSlipRL', 'wheelSlipRR',
            'wheelLoadFL', 'wheelLoadFR', 'wheelLoadRL', 'wheelLoadRR',
            'wheelsPressureFL', 'wheelsPressureFR', 'wheelsPressureRL', 'wheelsPressureRR',
            'wheelAngularSpeedFL', 'wheelAngularSpeedFR', 'wheelAngularSpeedRL', 'wheelAngularSpeedRR',
            'engineTemperature', 'tyreWearFL', 'tyreWearFR', 'tyreWearRL', 'tyreWearRR',
            'tyreCoreTempFL', 'tyreCoreTempFR', 'tyreCoreTempRL', 'tyreCoreTempRR'
        ]

    def read_data(self):
        try:
            mmap_file = mmap.mmap(-1, struct.calcsize(self.physics_layout), "Local\\acpmf_physics", access=mmap.ACCESS_READ)
            mmap_file.seek(0)
            raw_data = mmap_file.read(struct.calcsize(self.physics_layout))
            mmap_file.close()

            if not raw_data:
                return None

            data_values = struct.unpack(self.physics_layout, raw_data)
            data = {self.fields[i]: data_values[i] for i in range(len(self.fields))}
            data['timestamp'] = datetime.now().isoformat()

            return data
        except Exception as e:
            print(f"❌ Error al leer datos de Assetto Corsa: {e}")
            return None


if __name__ == "__main__":
    ac_interface = AssettoCorsaInterface()
    ac_data = ac_interface.read_data()

    if ac_data:
        print(f"✅ Datos capturados: {ac_data}")
    else:
        print("❌ No se pudieron capturar datos de Assetto Corsa")

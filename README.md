# F1 Data Analysis

Pipeline de telemetría en tiempo real para F1 23/24. Captura los paquetes UDP que emite el juego, los parsea con structs C (ctypes), los publica en Redis y los retransmite a clientes web mediante WebSocket.

---

## Arquitectura general

```
┌─────────────────────────────────────────────────────────────────┐
│  PC con F1 23/24                                                │
│  Ajustes → Telemetría UDP → IP del servidor, Puerto 20778       │
└──────────────────────────────┬──────────────────────────────────┘
                               │ UDP (binary packets)
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│  f1_reader.py  –  F1Reader                                       │
│                                                                  │
│  1. recvfrom(65535)  →  raw bytes                                │
│  2. PacketHeader.from_buffer_copy()  →  packet_id               │
│  3. route_packet(packet_id, data)                                │
│     └── parse_<type>()  →  dict                                  │
│  4. Enriquece con timestamp, session_uid, car_index              │
│  5. update_live_data() / get_damage_info() / get_track_heat_map()│
│  6. save_to_redis(data, channel)                                 │
└────────────────────────┬─────────────────────────────────────────┘
                         │ Redis pub/sub
          ┌──────────────┼───────────────┐
          │              │               │
      "car_data"    "car_damage"   "trackHeatMap"
          │
          ▼
┌─────────────────────────┐
│  index.ts  –  Bun       │
│  WebSocket :3000        │
│  subscriber → broadcast │
└──────────┬──────────────┘
           │ WebSocket JSON
           ▼
     Clientes browser
```

### Componentes

| Componente | Archivo | Rol |
|---|---|---|
| UDP Listener + Parser | `f1_reader.py` | Entrada principal del sistema |
| Estructuras C | `interfaces/interfaces.py` | Definiciones ctypes de todos los paquetes F1 |
| Packet handlers | `resources/utils.py` | Mapa `packet_id → método` y debug logger |
| Agregador live | `services/realtime_live_data.py` | Estado en memoria del piloto; publica snapshots |
| WebSocket bridge | `index.ts` | Relay Redis → navegador (Bun runtime) |
| DDL PostgreSQL | `sql/intial.sql` | Esquema de 5 tablas para persistencia histórica |
| Schemas PySpark | `interfaces/structs.py` | Tipos para procesamiento batch (no activo en live) |

---

## Requisitos

### Python (≥ 3.10)

```bash
pip install -r requirements.txt
```

Dependencias mínimas para el flujo live:

```
redis>=4.5.0
```

### TypeScript / Bun

```bash
bun install
```

### Infraestructura

```bash
docker-compose up -d
```

Servicios levantados:

| Servicio | Puerto |
|---|---|
| Redis | 6379 |
| Kafka | 9092 |
| Zookeeper | 2181 |
| PostgreSQL | 5432 |

> **Importante:** `KAFKA_ADVERTISED_LISTENERS` en `docker-compose.yml` está hardcodeado a `192.168.1.181:9092`. Cámbialo por la IP LAN de tu máquina si los clientes Kafka corren en hosts distintos.

---

## Puesta en marcha

Orden recomendado:

```bash
# 1. Infraestructura
docker-compose up -d

# 2. Pipeline Python (UDP → Redis)
python f1_reader.py

# 3. Servidor WebSocket (Redis → Browser)
bun run index.ts
```

> **No ejecutes `driver_scanner.py` junto a `f1_reader.py`**: ambos intentan abrir el puerto UDP 20778 y colisionan. `driver_scanner.py` y `master_pipeline.py` están marcados como **DEPRECATED**.

En F1 23/24, activa la telemetría UDP en:  
`Ajustes → Telemetría y estadísticas → Telemetría UDP → Activada`  
Apunta la IP al servidor y usa el puerto `20778`.

---

## Paquetes UDP y canales Redis

### Tabla de packet IDs

| ID | Tipo de paquete | Parser | Canal Redis |
|----|----------------|--------|-------------|
| 0 | Motion | `parse_motion` | `trackHeatMap` (combinado con ID 6) |
| 1 | Session | `parse_session` | `car_data` |
| 2 | Lap Data | `parse_lap_data` | `car_data` |
| 3 | Event | `parse_event` | — |
| 4 | Participants | `parse_participants` | — |
| 5 | Car Setups | `parse_car_setups` | — |
| 6 | Car Telemetry | `parse_car_telemetry` | `car_data` + `trackHeatMap` |
| 7 | Car Status | `parse_car_status` | `car_data` |
| 8 | Final Classification | `parse_final_classification` | — |
| 9 | Lobby Info | `parse_lobby_info` | — |
| 10 | Car Damage | `parse_car_damage` | `car_damage` |
| 11 | Session History | `parse_session_history` | — |
| 12 | Tyre Sets | `parse_tyre_sets` | — |
| 14 | Time Trial | `parse_time_trial` | — |

### Esquema de mensajes Redis

**Canal `car_data`** — snapshot del piloto, JSON:

```json
{
  "username": "Rafa",
  "car_id": 0,
  "track_id": 3,
  "timestamp": 123.45,
  "rpm": 11500,
  "gear": 4,
  "speed_kph": 287,
  "invalid_lap": 0,
  "current_lap": 3,
  "sector": 1,
  "sector_1_time": 28450,
  "sector_2_time": 0,
  "brake": 0.0,
  "throttle": 1.0,
  "fuel": 42.5,
  "lap_time_ms": 65200
}
```

**Canal `car_damage`** — daños del piloto, JSON:

```json
{
  "tyresWear": [12, 14, 10, 13],
  "tyresDamage": [0, 0, 0, 0],
  "brakesDamage": [0, 0, 0, 0],
  "frontLeftWingDamage": 0,
  "frontRightWingDamage": 0,
  "rearWingDamage": 0,
  "floorDamage": 0,
  "diffuserDamage": 0,
  "sidepodDamage": 0,
  "drsFault": 0,
  "gearBoxDamage": 0,
  "engineDamage": 0,
  "engineMGUHWear": 5,
  "engineESWear": 3,
  "engineCEWear": 2,
  "engineICEWear": 4,
  "engineMGUKWear": 3,
  "engineTCWear": 1
}
```

**Canal `trackHeatMap`** — punto de posición+input para heatmap, JSON:

```json
{
  "brake": 0.85,
  "throttle": 0.0,
  "worldPositionX": 342.17,
  "worldPositionY": -15.42
}
```

El canal `trackHeatMap` solo emite cuando se han recibido **ambos** un paquete de motion (ID 0) y uno de telemetría (ID 6) para el mismo frame; si llega solo uno, devuelve `None` y no publica.

---

## WebSocket

El servidor Bun escucha en `ws://localhost:3000`. Sólo suscribe el canal `car_data` de Redis y lo retransmite tal cual (JSON string) a todos los clientes conectados.

Cada cliente recibe un heartbeat ping cada 30 segundos para mantener la conexión viva.

**Prueba rápida con `test.ts`:**

```bash
bun run test.ts
```

Esto publica un mensaje de prueba en `car_data` para verificar que el bridge funciona sin necesitar el juego.

---

## Verificación de servicios

**Redis — comprobar mensajes en tiempo real:**

```bash
redis-cli
> SUBSCRIBE car_data
> SUBSCRIBE car_damage
> SUBSCRIBE trackHeatMap
```

**Kafka — consumir topic:**

```bash
docker exec -it kafka_f1 \
  kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic telemetry_enriched \
  --from-beginning
```

---

## Base de datos PostgreSQL

Inicializar el esquema:

```bash
psql -h localhost -U user -d f1_database -f sql/intial.sql
```

Credenciales por defecto (ver `docker-compose.yml`):

| Campo | Valor |
|---|---|
| Host | localhost |
| Puerto | 5432 |
| Base de datos | f1_database |
| Usuario | user |
| Contraseña | password |

Tablas creadas: `motion_data`, `session_data`, `lap_data`, `event_data`, `car_telemetry`.

> La escritura a PostgreSQL está implementada en `resources/master_pipeline.py` (deprecado). El flujo live actual solo usa Redis.

---

## Player index

`player_index = 0` está hardcodeado en `services/realtime_live_data.py`. Cada paquete contiene arrays de 22 coches; todas las funciones de live data indexan con este valor. En sesiones multijugador debe coincidir con `header.playerCarIndex`.

---

## Añadir soporte a un nuevo tipo de paquete

1. Definir el struct ctypes en `interfaces/interfaces.py`.
2. Añadir el método `parse_<tipo>` a la clase `F1Reader` en `f1_reader.py`.
3. Registrarlo en el dict de `get_packet_handlers()` en `resources/utils.py`.
4. Si debe publicarse en Redis, añadir la lógica en el bucle `F1Reader.start()`.

---

## Debug

`resources/utils.py:createFile()` añade dicts parseados a `logs/<nombre>.json`. Hay varias llamadas comentadas en `f1_reader.py` con el prefijo `##createFile(...)`. Descoméntalas temporalmente para volcar paquetes crudos a disco durante el desarrollo.

---

## Resolución de problemas

| Error | Causa | Solución |
|---|---|---|
| `OSError: [WinError 10048]` | Puerto 20778 ya en uso | Cerrar el otro proceso o cambiar el puerto en `F1Reader.__init__` |
| `Connection refused` Redis | Redis no está corriendo | `docker-compose up -d redis` |
| `NoBrokersAvailable` Kafka | Kafka no arrancado o IP incorrecta | Verificar `docker ps` y `KAFKA_ADVERTISED_LISTENERS` |
| Datos vacíos en WebSocket | `player_index` incorrecto | Ajustar `player_index` en `services/realtime_live_data.py` |
| `Paquete demasiado corto` | Versión del juego distinta | Revisar tamaño del struct en `interfaces/interfaces.py` |

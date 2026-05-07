# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Real-time F1 23/24 telemetry pipeline: the game broadcasts UDP packets, Python parses them into structured dicts, publishes to Redis pub/sub, and a Bun/TypeScript WebSocket server fans them out to browser clients.

## Running the System

Start infrastructure (Kafka, Zookeeper, Redis, PostgreSQL):
```bash
docker-compose up -d
```

Start the UDP listener and Redis publisher (main entry point):
```bash
python f1_reader.py
```

Start the WebSocket server that bridges Redis → browser clients:
```bash
bun run index.ts
```

**Do not run `driver_scanner.py` alongside `f1_reader.py`** — both bind to UDP port 20778 and will conflict. `driver_scanner.py` and `master_pipeline.py` are deprecated (marked in their headers).

### Infrastructure defaults
| Service    | Address              |
|------------|----------------------|
| Redis      | `localhost:6379`     |
| Kafka      | `localhost:9092`     |
| PostgreSQL | `localhost:5432`, db `f1_database`, user `user`, password `password` |
| WebSocket  | `ws://localhost:3000`|

Kafka's `KAFKA_ADVERTISED_LISTENERS` in `docker-compose.yml` is hardcoded to `192.168.1.181:9092` — update this to your machine's LAN IP if Kafka producers/consumers run on a different host.

## Architecture

```
F1 Game (UDP :20778)
    │
    ▼
f1_reader.py  (F1Reader class)
    │  reads raw bytes, calls from_buffer_copy() into ctypes structs
    │  routes by packet_id (0–14) via get_packet_handlers()
    │
    ├── packet_id ∈ {1,2,6,7}  → update_live_data()  → Redis "car_data"
    ├── packet_id == 10         → get_damage_info()   → Redis "car_damage"
    └── packet_id ∈ {0,6}      → get_track_heat_map()→ Redis "trackHeatMap"
                                        │
                                        ▼
                                   index.ts (Bun)
                                   Subscribes to Redis "car_data"
                                   Broadcasts JSON over WebSocket
```

### Key files

| File | Role |
|------|------|
| `f1_reader.py` | Core: UDP socket, `route_packet()` dispatch, `save_to_redis()` |
| `interfaces/interfaces.py` | All ctypes C-struct definitions for every F1 packet type |
| `resources/utils.py` | `get_packet_handlers()` map and `createFile()` debug logger |
| `services/realtime_live_data.py` | Stateful `live_data` dict; `update_live_data()`, `get_damage_info()`, `get_track_heat_map()` |
| `index.ts` | Bun WebSocket server; subscribes Redis → broadcasts to all WS clients |
| `sql/intial.sql` | PostgreSQL DDL for 5 tables (motion, session, lap, event, telemetry) |
| `sql/queries.py` | Parameterised INSERT strings consumed by the deprecated master_pipeline |
| `interfaces/structs.py` | PySpark schema definitions (unused in live flow; for batch analytics) |

### Packet ID → parser mapping (resources/utils.py)

| ID | Type | Redis channel |
|----|------|---------------|
| 0 | Motion | trackHeatMap (combined with ID 6) |
| 1 | Session | car_data |
| 2 | Lap Data | car_data |
| 3 | Event | — |
| 4 | Participants | — |
| 5 | Car Setups | — |
| 6 | Car Telemetry | car_data + trackHeatMap |
| 7 | Car Status | car_data |
| 8 | Final Classification | — |
| 9 | Lobby Info | — |
| 10 | Car Damage | car_damage |
| 11 | Session History | — |
| 12 | Tyre Sets | — |
| 14 | Time Trial | — |

### Player index

`player_index = 0` is hardcoded in `services/realtime_live_data.py:28`. Every parsed packet contains arrays of 22 cars; all live-data functions index into these arrays using `player_index`. In multiplayer sessions this value must match `header.playerCarIndex`.

### Adding a new packet type

1. Define the ctypes struct(s) in `interfaces/interfaces.py`.
2. Add a `parse_<type>` method to `F1Reader` in `f1_reader.py`.
3. Register it in `get_packet_handlers()` in `resources/utils.py`.
4. Optionally publish the result to Redis in `F1Reader.start()`.

### Debug logging

`resources/utils.py:createFile()` appends parsed dicts to `logs/<name>.json`. Several calls are commented out in `f1_reader.py` with `##createFile(...)` — uncomment them temporarily to inspect raw packet contents.

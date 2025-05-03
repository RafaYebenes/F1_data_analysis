
# 🏁 F1 Data Analysis - Setup y Ejecución

Este proyecto permite capturar datos en tiempo real del juego F1 23 a través de UDP y analizarlos usando Redis, Kafka y PostgreSQL.

---

## 🐳 1. Inicia los contenedores con Docker

Desde la raíz del proyecto (donde está el `docker-compose.yml`):

```bash
docker-compose up -d
```

Esto levantará:
- Kafka (`localhost:9092`)
- Zookeeper (`localhost:2181`)
- Redis (`localhost:6379`)
- PostgreSQL (puerto estándar `5432`, ver `docker-compose.yml` para confirmar)

Verifica que estén corriendo con:

```bash
docker ps
```

---

## ⚙️ 2. Ejecuta el `master_pipeline.py`

Este script escucha en Kafka y procesa los datos entrantes para guardarlos o analizarlos.

```bash
python master_pipeline.py
```

Salida esperada:
```
⏳ Esperando mensajes en Kafka...
```

---

## 🎮 3. En el PC donde se ejecuta F1 23, lanza `driver_scanner.py`

Este script:
- Inicia el listener de paquetes UDP (puerto `20778`)
- Parseará los datos de F1 23
- Enviará los datos a Redis y Kafka

```bash
python driver_scanner.py
```

⚠️ **No ejecutes `f1_reader.py` por separado si usas `driver_scanner.py`, ya que ambos intentan abrir el mismo puerto UDP.**

---

## 🧪 4. Verificación (opcional)

Puedes comprobar que los datos se están enviando correctamente:

- **Redis (canal `live_dashboard`)**
```bash
redis-cli
> SUBSCRIBE live_dashboard
```

- **Kafka (topic `telemetry_enriched`)**
```bash
docker exec -it <kafka_container_name>   kafka-console-consumer --bootstrap-server localhost:9092 --topic telemetry_enriched --from-beginning
```

---

## 💡 Extras

- Si ves el error `OSError: [WinError 10048]`, significa que el puerto `20778` ya está en uso. Cierra cualquier otro proceso que lo esté usando.
- Puedes cambiar el puerto UDP en `f1_reader.py` si quieres evitar conflictos.

---

## ✅ Orden recomendado de ejecución

1. `docker-compose up -d`
2. `python master_pipeline.py`
3. `python driver_scanner.py` (en el PC donde corre F1 24)

---

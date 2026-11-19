# GameGraph · Recomendador de videojuegos con Neo4j AuraDB

Aplicación web (Python + Flask) conectada a una base de datos **de grafo** alojada en
**Neo4j AuraDB** (DaaS). Modela jugadores, videojuegos, géneros, plataformas y estudios,
y genera recomendaciones recorriendo el grafo.

- **CRUD completo** de jugadores y videojuegos, y de las relaciones `PLAYED` (partidas con
  calificación/horas) y `FRIEND_OF` (amistades).
- **Consultas de grafo**: filtrado colaborativo (3 saltos), recomendación por géneros,
  recomendación social, amigos de amigos, juegos similares (vecindad), y camino más
  corto entre jugadores con `shortestPath()`.
- **Visualización** de la vecindad de cada jugador (vis-network).

## Modelo de datos

```
(:Player)-[:PLAYED {rating, hours}]->(:Game)
(:Player)-[:FRIEND_OF {since}]-(:Player)
(:Game)-[:HAS_GENRE]->(:Genre)
(:Game)-[:AVAILABLE_ON]->(:Platform)
(:Game)-[:DEVELOPED_BY]->(:Developer)
```

## Estructura

```
neo4j-videojuegos/
├── run.py                      # punto de entrada
├── requirements.txt
├── .env.example                # plantilla de variables de entorno
├── app/
│   ├── __init__.py             # fábrica Flask + manejo de errores
│   ├── config.py               # lectura de variables de entorno
│   ├── db.py                   # driver oficial de Neo4j (singleton, execute_query)
│   ├── repositories/           # TODAS las consultas Cypher, por dominio
│   │   ├── players.py          #   CRUD jugadores, PLAYED, FRIEND_OF
│   │   ├── games.py            #   CRUD juegos, catálogos, juegos similares
│   │   ├── recommendations.py  #   motor de recomendación (traversals)
│   │   └── graph.py            #   shortestPath, ego-network, estadísticas
│   ├── routes/                 # controladores (blueprints)
│   ├── templates/              # vistas HTML (Jinja2)
│   └── static/style.css
├── database/
│   ├── schema.cypher           # restricciones de unicidad e índices
│   ├── seed.py                 # script de seeding (esquema + datos)
│   └── seed.cypher             # mismo seeding en Cypher puro (consola de Aura)
└── docs/Documentacion.pdf
```

## Requisitos

- Python 3.10 o superior
- Una instancia **Neo4j AuraDB Free** (https://console.neo4j.io)

## Instalación (Windows · CMD)

```bat
git clone https://github.com/saimonetii/neo4j-videojuegos.git
cd neo4j-videojuegos

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

copy .env.example .env
notepad .env
```

En `.env` pega los valores del archivo de credenciales que descargaste al crear la
instancia de AuraDB (`NEO4J_URI`, `NEO4J_USERNAME`, `NEO4J_PASSWORD`).

> En macOS/Linux: `source venv/bin/activate` y `cp .env.example .env`.

## Cargar la base de datos (seeding)

```bat
python -m database.seed
```

Crea las restricciones/índices y carga 32 juegos, 12 jugadores, 71 partidas y 14
amistades. **Borra todo lo anterior** para dejar la base en un estado conocido; usa
`--keep` si no quieres borrar.

Alternativa sin Python: pegar `database/schema.cypher` y luego `database/seed.cypher`
en la pestaña *Query* de la consola de AuraDB.

## Ejecutar

En Windows también puedes dar **doble clic** a `cargar_datos.bat` (seeding) y luego a
`abrir_app.bat` (abre la página sola en el navegador).


```bat
python run.py
```

Abrir http://127.0.0.1:5000. El pie de página muestra la dirección del servidor de Aura
al que está conectada la aplicación.

## Guion sugerido para la demo

1. **Inicio**: conteo de nodos/relaciones leídos en vivo desde AuraDB.
2. **Jugadores → Luis**: recomendaciones colaborativa, por género y social.
3. **Registrar partida** (ej. Sekiro, 5★) → las recomendaciones cambian al instante.
4. **Crear jugador** nuevo, agregar amigos y partidas; **editar** y **eliminar**.
5. **Videojuegos**: filtros por género/plataforma, crear/editar/eliminar un juego,
   ver *juegos similares* y *quienes lo jugaron también jugaron*.
6. **Caminos**: Luis → Fernanda: 6 saltos solo por amistades vs. 2 saltos por amistades o juegos en común (ambos juegan Valorant).
7. **Ver su grafo**: vecindad visual del jugador.
8. Recargar la página / reiniciar la app para demostrar la **persistencia** en la nube.

## Seguridad

Las credenciales solo viven en `.env`, que está en `.gitignore`. Todas las consultas
usan parámetros (`$param`), nunca concatenación de strings.

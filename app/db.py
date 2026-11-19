"""Capa de acceso a Neo4j AuraDB usando el driver oficial de Python.

- Se crea UN solo Driver por proceso (es thread-safe y mantiene un pool de
  conexiones). Crear un driver por petición sería muy costoso.
- Se usa driver.execute_query(), que abre la sesión, ejecuta la consulta dentro
  de una transacción administrada y reintenta automáticamente ante errores
  transitorios (por ejemplo, un cambio de líder en el clúster de Aura).
- Las lecturas se envían con RoutingControl.READ y las escrituras con
  RoutingControl.WRITE, para que el driver las enrute al servidor adecuado.
- Siempre se usan parámetros ($param), nunca concatenación de strings:
  evita inyección de Cypher y permite reutilizar el plan de ejecución en caché.
"""
import atexit

from neo4j import GraphDatabase, RoutingControl
from neo4j.exceptions import DriverError, Neo4jError

from .config import Config

_driver = None
_server_info = {}


def _candidates():
    """Combinaciones (URI, base) a probar: primero lo que dice el .env y, si falla,
    las que corresponden a la instancia de Aura (en las instancias nuevas de Aura
    la base se llama igual que el id de la instancia)."""
    options = [(Config.NEO4J_URI, Config.NEO4J_DATABASE)]
    if Config.AURA_INSTANCEID:
        aura_uri = f"neo4j+s://{Config.AURA_INSTANCEID}.databases.neo4j.io"
        options += [(aura_uri, Config.AURA_INSTANCEID), (aura_uri, Config.NEO4J_DATABASE),
                    (aura_uri, None)]
    unique = []
    for option in options:
        if option[0] and option not in unique:
            unique.append(option)
    return unique


def init_driver():
    """Crea el driver y verifica la conexión con la instancia en la nube."""
    global _driver, _server_info
    if _driver is not None:
        return _driver

    Config.validate()
    last_error = None
    for uri, database in _candidates():
        driver = GraphDatabase.driver(
            uri,
            auth=(Config.NEO4J_USERNAME, Config.NEO4J_PASSWORD),
            max_connection_lifetime=300,  # Aura cierra conexiones inactivas; las renovamos antes
            connection_timeout=15,
        )
        try:
            # Prueba real contra la base: falla si la URI, las credenciales o el
            # nombre de la base están mal. session.run no reintenta: responde rápido.
            with driver.session(database=database) as session:
                summary = session.run("RETURN 1 AS ok").consume()
        except (DriverError, Neo4jError) as err:
            last_error = err
            driver.close()
            continue
        _driver = driver
        Config.NEO4J_URI, Config.NEO4J_DATABASE = uri, database
        _server_info = {"address": str(summary.server.address), "agent": summary.server.agent,
                        "database": database or "(por defecto)"}
        atexit.register(close_driver)
        return _driver
    raise last_error


def close_driver():
    global _driver
    if _driver is not None:
        _driver.close()
        _driver = None


def server_info():
    return _server_info


def _run(query, params, routing):
    records, _summary, _keys = _driver.execute_query(
        query,
        parameters_=params,
        database_=Config.NEO4J_DATABASE,
        routing_=routing,
    )
    return [record.data() for record in records]


def read(query, **params):
    """Ejecuta una consulta de solo lectura y devuelve una lista de dicts."""
    return _run(query, params, RoutingControl.READ)


def write(query, **params):
    """Ejecuta una consulta de escritura y devuelve una lista de dicts."""
    return _run(query, params, RoutingControl.WRITE)

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

from .config import Config

_driver = None
_server_info = {}


def init_driver():
    """Crea el driver y verifica la conexión con la instancia en la nube."""
    global _driver, _server_info
    if _driver is not None:
        return _driver

    Config.validate()
    _driver = GraphDatabase.driver(
        Config.NEO4J_URI,
        auth=(Config.NEO4J_USERNAME, Config.NEO4J_PASSWORD),
        max_connection_lifetime=300,  # Aura cierra conexiones inactivas; las renovamos antes
    )
    _driver.verify_connectivity()  # lanza excepción si la URI o las credenciales están mal

    info = _driver.get_server_info()
    _server_info = {"address": str(info.address), "agent": info.agent}
    atexit.register(close_driver)
    return _driver


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

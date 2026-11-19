"""Configuración de la aplicación.

Todas las credenciales se leen de variables de entorno (archivo .env en
desarrollo). Nunca se escriben en el código fuente.
"""
import os

from dotenv import load_dotenv

# utf-8-sig: tolera el BOM que a veces agrega el Bloc de notas de Windows
load_dotenv(encoding="utf-8-sig", override=True)


class Config:
    # Conexión a Neo4j AuraDB (mismos nombres que el archivo de credenciales de Aura)
    # ej. neo4j+s://xxxxxxxx.databases.neo4j.io  (si falta, se arma con AURA_INSTANCEID)
    NEO4J_URI = os.getenv("NEO4J_URI") or (
        f"neo4j+s://{os.getenv('AURA_INSTANCEID')}.databases.neo4j.io"
        if os.getenv("AURA_INSTANCEID") else None)
    NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
    NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")

    # Flask
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "cambia-esta-clave")

    @classmethod
    def validate(cls):
        """Falla rápido y con un mensaje claro si falta alguna credencial."""
        missing = [name for name in ("NEO4J_URI", "NEO4J_PASSWORD") if not getattr(cls, name)]
        if missing:
            raise RuntimeError(
                "Faltan variables de entorno: " + ", ".join(missing)
                + ". Copia .env.example a .env y llena los datos de tu instancia AuraDB."
            )

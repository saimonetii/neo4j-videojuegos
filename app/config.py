"""Configuración de la aplicación.

Todas las credenciales se leen de variables de entorno (archivo .env en
desarrollo). Nunca se escriben en el código fuente.
"""
import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    # Conexión a Neo4j AuraDB (mismos nombres que el archivo de credenciales de Aura)
    NEO4J_URI = os.getenv("NEO4J_URI")            # ej. neo4j+s://xxxxxxxx.databases.neo4j.io
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

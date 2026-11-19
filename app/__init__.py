"""Fábrica de la aplicación Flask."""
from flask import Flask, render_template
from neo4j.exceptions import Neo4jError, ServiceUnavailable, SessionExpired

from . import db
from .config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_driver()  # conecta a AuraDB al arrancar (falla rápido si hay error)

    # Completa portadas faltantes o antiguas (no toca las editadas a mano)
    from database.seed import sync_images
    try:
        sync_images(db)
    except Exception as err:  # una portada nunca debe impedir que arranque la app
        app.logger.warning("No se pudieron sincronizar portadas: %s", err)

    from .routes.games import bp as games_bp
    from .routes.main import bp as main_bp
    from .routes.players import bp as players_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(players_bp)
    app.register_blueprint(games_bp)

    @app.template_filter("wall")
    def wall_filter(images, size=18):
        """Repite las portadas (sin vacíos) hasta llenar el muro del encabezado."""
        images = [img for img in images if img]
        return (images * (size // len(images) + 1))[:size] if images else []

    @app.context_processor
    def inject_server():
        return {"server": db.server_info()}

    @app.errorhandler(ServiceUnavailable)
    @app.errorhandler(SessionExpired)
    def db_unavailable(err):
        return render_template("error.html", title="Sin conexión con AuraDB",
                               message=str(err)), 503

    @app.errorhandler(Neo4jError)
    def db_error(err):
        return render_template("error.html", title="Error de Neo4j",
                               message=f"{err.code}: {err.message}"), 500

    @app.errorhandler(404)
    def not_found(_err):
        return render_template("error.html", title="No encontrado",
                               message="El recurso solicitado no existe."), 404

    return app

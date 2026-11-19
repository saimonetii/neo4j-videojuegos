"""Rutas de videojuegos: CRUD, filtros y vecindad (juegos similares)."""
import re
import unicodedata

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from neo4j.exceptions import ConstraintError

from ..repositories import games

bp = Blueprint("games", __name__, url_prefix="/juegos")


def slugify(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60]


def _split(value):
    return sorted({item.strip() for item in value.split(",") if item.strip()})


def _game_form():
    """Lee y valida el formulario. Devuelve (datos, error)."""
    title = request.form.get("title", "").strip()
    developer = request.form.get("developer", "").strip()
    try:
        year = int(request.form.get("year", ""))
    except ValueError:
        year = None
    data = {
        "title": title,
        "year": year,
        "description": request.form.get("description", "").strip(),
        "developer": developer,
        "genres": _split(request.form.get("genres", "")),
        "platforms": _split(request.form.get("platforms", "")),
    }
    if not title or not developer or year is None or not 1970 <= year <= 2100:
        return data, "Título, desarrollador y año (1970-2100) son obligatorios."
    return data, None


@bp.route("/")
def list_games():
    genre = request.args.get("genre") or None
    platform = request.args.get("platform") or None
    q = request.args.get("q") or None
    return render_template("games/list.html",
                           games=games.list_games(genre, platform, q),
                           catalog=games.catalog(),
                           genre=genre, platform=platform, q=q)


@bp.route("/nuevo", methods=["GET", "POST"])
def create():  # CREATE
    data, error = {}, None
    if request.method == "POST":
        data, error = _game_form()
        if error:
            flash(error, "error")
        else:
            data["id"] = slugify(data["title"])
            try:
                games.create_game(data)
                flash(f"Juego «{data['title']}» creado.", "ok")
                return redirect(url_for("games.detail", game_id=data["id"]))
            except ConstraintError:
                flash("Ya existe un juego con ese título (id único).", "error")
    return render_template("games/form.html", game=data, catalog=games.catalog(),
                           action=url_for("games.create"), heading="Nuevo videojuego")


@bp.route("/<game_id>")
def detail(game_id):  # READ
    data = games.get_game(game_id)
    if data is None:
        abort(404)
    return render_template("games/detail.html", data=data,
                           similar=games.similar_games(game_id),
                           also_played=games.also_played(game_id))


@bp.route("/<game_id>/editar", methods=["GET", "POST"])
def edit(game_id):  # UPDATE
    current = games.get_game(game_id)
    if current is None:
        abort(404)
    if request.method == "POST":
        data, error = _game_form()
        if error:
            flash(error, "error")
        else:
            games.update_game(game_id, data)
            flash("Juego actualizado.", "ok")
            return redirect(url_for("games.detail", game_id=game_id))
    game = dict(current["game"])
    game["developer"] = ", ".join(current["developers"])
    game["genres"] = current["genres"]
    game["platforms"] = current["platforms"]
    return render_template("games/form.html", game=game, catalog=games.catalog(),
                           action=url_for("games.edit", game_id=game_id),
                           heading=f"Editar: {game['title']}")


@bp.route("/<game_id>/eliminar", methods=["POST"])
def delete(game_id):  # DELETE
    if games.delete_game(game_id):
        flash("Juego eliminado junto con sus relaciones.", "ok")
    return redirect(url_for("games.list_games"))

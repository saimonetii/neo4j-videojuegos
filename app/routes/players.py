"""Rutas de jugadores: CRUD, partidas (PLAYED), amistades y recomendaciones."""
import re

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from neo4j.exceptions import ConstraintError

from ..repositories import games, graph, players, recommendations

bp = Blueprint("players", __name__, url_prefix="/jugadores")

USERNAME_RE = re.compile(r"^[a-z0-9_]{3,20}$")


def _player_form():
    name = request.form.get("name", "").strip()
    country = request.form.get("country", "").strip().upper()[:2] or None
    return name, country


@bp.route("/", methods=["GET", "POST"])
def list_players():
    if request.method == "POST":  # CREATE
        username = request.form.get("username", "").strip().lower()
        name, country = _player_form()
        if not USERNAME_RE.match(username) or not name:
            flash("Usuario inválido (3-20 caracteres: a-z, 0-9, _) o nombre vacío.", "error")
        else:
            try:
                players.create_player(username, name, country)
                flash(f"Jugador «{name}» creado.", "ok")
                return redirect(url_for("players.detail", username=username))
            except ConstraintError:
                flash(f"El usuario «{username}» ya existe (restricción UNIQUE).", "error")
    return render_template("players/list.html", players=players.list_players(),
                           covers=[c["image"] for c in graph.covers()])


@bp.route("/<username>")
def detail(username):  # READ
    data = players.get_player(username)
    if data is None:
        abort(404)
    played_ids = {g["id"] for g in data["played"]}
    friend_ids = {f["username"] for f in data["friends"]}
    return render_template(
        "players/detail.html",
        data=data,
        all_games=[g for g in games.list_games()],
        played_ids=played_ids,
        other_players=[p for p in players.list_players()
                       if p["username"] != username and p["username"] not in friend_ids],
        recs={
            "collaborative": recommendations.collaborative(username),
            "content": recommendations.content_based(username),
            "social": recommendations.social(username),
        },
        friend_suggestions=recommendations.friend_suggestions(username),
    )


@bp.route("/<username>/editar", methods=["GET", "POST"])
def edit(username):  # UPDATE
    data = players.get_player(username)
    if data is None:
        abort(404)
    if request.method == "POST":
        name, country = _player_form()
        if not name:
            flash("El nombre no puede estar vacío.", "error")
        else:
            players.update_player(username, name, country)
            flash("Jugador actualizado.", "ok")
            return redirect(url_for("players.detail", username=username))
    return render_template("players/edit.html", player=data["player"])


@bp.route("/<username>/eliminar", methods=["POST"])
def delete(username):  # DELETE
    if players.delete_player(username):
        flash(f"Jugador «{username}» eliminado junto con sus relaciones.", "ok")
    return redirect(url_for("players.list_players"))


@bp.route("/<username>/partidas", methods=["POST"])
def add_play(username):
    game_id = request.form.get("game_id")
    try:
        rating = int(request.form.get("rating", 0))
        hours = int(request.form.get("hours", 0))
    except ValueError:
        rating, hours = 0, -1
    if not game_id or not 1 <= rating <= 5 or hours < 0:
        flash("Datos de partida inválidos (calificación 1-5, horas >= 0).", "error")
    elif players.upsert_play(username, game_id, rating, hours):
        flash("Partida registrada.", "ok")
    return redirect(url_for("players.detail", username=username))


@bp.route("/<username>/partidas/<game_id>/eliminar", methods=["POST"])
def delete_play(username, game_id):
    players.delete_play(username, game_id)
    flash("Partida eliminada.", "ok")
    return redirect(url_for("players.detail", username=username))


@bp.route("/<username>/amigos", methods=["POST"])
def add_friend(username):
    other = request.form.get("friend")
    if other and other != username and players.add_friend(username, other):
        flash("Amistad agregada.", "ok")
    return redirect(url_for("players.detail", username=username))


@bp.route("/<username>/amigos/<other>/eliminar", methods=["POST"])
def remove_friend(username, other):
    players.remove_friend(username, other)
    flash("Amistad eliminada.", "ok")
    return redirect(url_for("players.detail", username=username))

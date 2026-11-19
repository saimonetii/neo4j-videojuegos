"""Inicio, buscador de caminos y visualización del grafo."""
from flask import Blueprint, abort, jsonify, render_template, request

from ..repositories import graph, players

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return render_template("index.html", stats=graph.stats())


@bp.route("/caminos")
def paths():
    all_players = players.list_players()
    source = request.args.get("source")
    target = request.args.get("target")
    mode = request.args.get("mode", "social")
    result, error = None, None
    if source and target:
        if source == target:
            error = "Elige dos jugadores distintos."
        else:
            result = graph.shortest_path(source, target, mode)
            if result is None:
                error = "No existe un camino entre esos jugadores (dentro del límite de saltos)."
    return render_template("paths.html", players=all_players, source=source,
                           covers=[c["image"] for c in graph.covers()],
                           target=target, mode=mode, result=result, error=error)


@bp.route("/grafo/<username>")
def graph_view(username):
    if players.get_player(username) is None:
        abort(404)
    return render_template("graph.html", username=username)


@bp.route("/api/grafo/<username>")
def graph_api(username):
    return jsonify(graph.ego_network(username))

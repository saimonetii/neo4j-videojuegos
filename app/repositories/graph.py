"""Consultas de grafo generales: caminos más cortos, vecindad y estadísticas."""
from .. import db

# Camino más corto SOLO por amistades (grados de separación, máx. 6 saltos).
SHORTEST_PATH_SOCIAL = """
MATCH (a:Player {username: $source}), (b:Player {username: $target})
MATCH path = shortestPath((a)-[:FRIEND_OF*..6]-(b))
RETURN [n IN nodes(path) | {label: labels(n)[0], key: n.username, name: n.name, image: null}] AS nodes,
       [r IN relationships(path) | type(r)] AS rels,
       length(path) AS hops
"""

# Camino más corto por amistades O juegos en común (máx. 8 saltos).
SHORTEST_PATH_ANY = """
MATCH (a:Player {username: $source}), (b:Player {username: $target})
MATCH path = shortestPath((a)-[:FRIEND_OF|PLAYED*..8]-(b))
RETURN [n IN nodes(path) | {label: labels(n)[0],
                            key: coalesce(n.username, n.id),
                            name: coalesce(n.name, n.title),
                            image: n.image}] AS nodes,
       [r IN relationships(path) | type(r)] AS rels,
       length(path) AS hops
"""

# Vecindad de un jugador (ego-network) para la visualización:
# jugador -> juegos y amigos (1 salto) y juegos -> géneros (2 saltos).
EGO_NETWORK = """
MATCH (me:Player {username: $username})-[r:PLAYED|FRIEND_OF]-(n)
RETURN type(r) AS type, labels(n)[0] AS label,
       coalesce(n.username, n.id) AS key, coalesce(n.name, n.title) AS name,
       r.rating AS rating
"""

EGO_GENRES = """
MATCH (:Player {username: $username})-[:PLAYED]->(g:Game)-[:HAS_GENRE]->(ge:Genre)
RETURN DISTINCT g.id AS game, ge.name AS genre
"""

COUNT_BY_LABEL = """
MATCH (n)
RETURN labels(n)[0] AS label, count(*) AS total
ORDER BY label
"""

COUNT_RELS = """
MATCH ()-[r]->()
RETURN type(r) AS type, count(*) AS total
ORDER BY type
"""

TOP_GAMES = """
MATCH (g:Game)<-[r:PLAYED]-(:Player)
WITH g, avg(r.rating) AS avgRating, count(r) AS votes, sum(r.hours) AS hours
WHERE votes >= 2
RETURN g.id AS id, g.title AS title, round(avgRating, 1) AS avgRating, votes, hours
ORDER BY avgRating DESC, votes DESC
LIMIT 5
"""

TOP_GENRES = """
MATCH (:Player)-[r:PLAYED]->(:Game)-[:HAS_GENRE]->(ge:Genre)
RETURN ge.name AS genre, sum(r.hours) AS hours
ORDER BY hours DESC
LIMIT 5
"""


# Portadas para el muro del inicio y la fila de "más jugados"
COVERS = """
MATCH (g:Game) WHERE g.image IS NOT NULL
OPTIONAL MATCH (g)<-[r:PLAYED]-(:Player)
WITH g, count(r) AS players
RETURN g.id AS id, g.title AS title, g.image AS image, players
ORDER BY players DESC, g.title
LIMIT 18
"""


def covers():
    return db.read(COVERS)


def shortest_path(source, target, mode="social"):
    query = SHORTEST_PATH_ANY if mode == "any" else SHORTEST_PATH_SOCIAL
    rows = db.read(query, source=source, target=target)
    return rows[0] if rows else None


def ego_network(username):
    """Devuelve nodos y aristas en el formato que espera vis-network."""
    nodes = {f"Player:{username}": {"id": f"Player:{username}", "label": username, "group": "Me"}}
    edges = []
    for row in db.read(EGO_NETWORK, username=username):
        node_id = f"{row['label']}:{row['key']}"
        nodes[node_id] = {"id": node_id, "label": row["name"], "group": row["label"]}
        label = f"{row['rating']}★" if row["type"] == "PLAYED" else ""
        edges.append({"from": f"Player:{username}", "to": node_id, "label": label,
                      "type": row["type"]})
    for row in db.read(EGO_GENRES, username=username):
        genre_id = f"Genre:{row['genre']}"
        nodes[genre_id] = {"id": genre_id, "label": row["genre"], "group": "Genre"}
        edges.append({"from": f"Game:{row['game']}", "to": genre_id, "label": "",
                      "type": "HAS_GENRE"})
    return {"nodes": list(nodes.values()), "edges": edges}


def stats():
    return {
        "labels": db.read(COUNT_BY_LABEL),
        "rels": db.read(COUNT_RELS),
        "top_games": db.read(TOP_GAMES),
        "top_genres": db.read(TOP_GENRES),
        "covers": db.read(COVERS),
    }

"""CRUD de videojuegos (:Game) y catálogos (:Genre, :Platform, :Developer)."""
from .. import db

# ---------------------------------------------------------------- Consultas
# FOREACH permite crear 0..n relaciones sin "matar" la fila cuando la lista
# viene vacía (con UNWIND [] la consulta no devolvería nada).
CREATE_GAME = """
CREATE (g:Game {id: $id, title: $title, year: $year, description: $description,
                image: $image})
MERGE (d:Developer {name: $developer})
MERGE (g)-[:DEVELOPED_BY]->(d)
FOREACH (name IN $genres |
    MERGE (ge:Genre {name: name})
    MERGE (g)-[:HAS_GENRE]->(ge))
FOREACH (name IN $platforms |
    MERGE (pf:Platform {name: name})
    MERGE (g)-[:AVAILABLE_ON]->(pf))
RETURN g.id AS id
"""

LIST_GAMES = """
MATCH (g:Game)
WHERE ($genre IS NULL OR EXISTS { (g)-[:HAS_GENRE]->(:Genre {name: $genre}) })
  AND ($platform IS NULL OR EXISTS { (g)-[:AVAILABLE_ON]->(:Platform {name: $platform}) })
  AND ($q IS NULL OR toLower(g.title) CONTAINS toLower($q))
OPTIONAL MATCH (g)<-[r:PLAYED]-(:Player)
WITH g, avg(r.rating) AS avgRating, count(r) AS players
RETURN g.id AS id, g.title AS title, g.year AS year, g.image AS image,
       [(g)-[:HAS_GENRE]->(ge:Genre) | ge.name] AS genres,
       round(avgRating, 1) AS avgRating, players
ORDER BY players DESC, title
"""

GET_GAME = """
MATCH (g:Game {id: $id})
RETURN g {.id, .title, .year, .description, .image} AS game,
       [(g)-[:DEVELOPED_BY]->(d:Developer) | d.name] AS developers,
       [(g)-[:HAS_GENRE]->(ge:Genre) | ge.name] AS genres,
       [(g)-[:AVAILABLE_ON]->(pf:Platform) | pf.name] AS platforms,
       [(p:Player)-[r:PLAYED]->(g) |
           {username: p.username, name: p.name, rating: r.rating, hours: r.hours}] AS players
"""

# Para actualizar las listas se borran las relaciones salientes de catálogo
# y se vuelven a crear con los valores nuevos.
UPDATE_GAME = """
MATCH (g:Game {id: $id})
SET g.title = $title, g.year = $year, g.description = $description,
    g.image = $image, g.updatedAt = datetime()
WITH g
OPTIONAL MATCH (g)-[old:HAS_GENRE|AVAILABLE_ON|DEVELOPED_BY]->()
DELETE old
WITH DISTINCT g
MERGE (d:Developer {name: $developer})
MERGE (g)-[:DEVELOPED_BY]->(d)
FOREACH (name IN $genres |
    MERGE (ge:Genre {name: name})
    MERGE (g)-[:HAS_GENRE]->(ge))
FOREACH (name IN $platforms |
    MERGE (pf:Platform {name: name})
    MERGE (g)-[:AVAILABLE_ON]->(pf))
RETURN g.id AS id
"""

DELETE_GAME = """
MATCH (g:Game {id: $id})
DETACH DELETE g
RETURN count(*) AS deleted
"""

LIST_CATALOG = """
MATCH (n)
WHERE n:Genre OR n:Platform OR n:Developer
RETURN labels(n)[0] AS label, n.name AS name
ORDER BY name
"""

# ------------------------------------------- Vecindades (consultas de grafo)
# Juegos a 2 saltos que comparten género o desarrollador con el juego actual.
SIMILAR_GAMES = """
MATCH (g:Game {id: $id})-[:HAS_GENRE|DEVELOPED_BY]->(trait)<-[:HAS_GENRE|DEVELOPED_BY]-(other:Game)
WHERE other <> g
WITH other, count(trait) AS shared, collect(trait.name) AS traits
OPTIONAL MATCH (other)<-[r:PLAYED]-(:Player)
WITH other, shared, traits, avg(r.rating) AS avgRating
RETURN other.id AS id, other.title AS title, other.image AS image, shared, traits,
       round(coalesce(avgRating, 0.0), 1) AS avgRating
ORDER BY shared DESC, avgRating DESC, title
LIMIT 6
"""

# "Quienes jugaron esto también jugaron..." (co-ocurrencia vía jugadores)
ALSO_PLAYED = """
MATCH (g:Game {id: $id})<-[:PLAYED]-(p:Player)-[r:PLAYED]->(other:Game)
WHERE other <> g
RETURN other.id AS id, other.title AS title, other.image AS image,
       count(DISTINCT p) AS sharedPlayers, round(avg(r.rating), 1) AS avgRating
ORDER BY sharedPlayers DESC, avgRating DESC, title
LIMIT 6
"""


# ---------------------------------------------------------------- Funciones
def create_game(data):
    return db.write(CREATE_GAME, **data)


def list_games(genre=None, platform=None, q=None):
    return db.read(LIST_GAMES, genre=genre or None, platform=platform or None, q=q or None)


def get_game(game_id):
    rows = db.read(GET_GAME, id=game_id)
    if not rows:
        return None
    data = rows[0]
    data["players"].sort(key=lambda p: (-p["rating"], -p["hours"]))
    data["genres"].sort()
    data["platforms"].sort()
    ratings = [p["rating"] for p in data["players"]]
    data["avgRating"] = round(sum(ratings) / len(ratings), 1) if ratings else None
    return data


def update_game(game_id, data):
    return bool(db.write(UPDATE_GAME, id=game_id, **data))


def delete_game(game_id):
    return db.write(DELETE_GAME, id=game_id)[0]["deleted"] > 0


def catalog():
    """Devuelve {'Genre': [...], 'Platform': [...], 'Developer': [...]}."""
    result = {"Genre": [], "Platform": [], "Developer": []}
    for row in db.read(LIST_CATALOG):
        result[row["label"]].append(row["name"])
    return result


def similar_games(game_id):
    return db.read(SIMILAR_GAMES, id=game_id)


def also_played(game_id):
    return db.read(ALSO_PLAYED, id=game_id)

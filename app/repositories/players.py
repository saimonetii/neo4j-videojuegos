"""CRUD de jugadores (:Player) y de sus relaciones PLAYED y FRIEND_OF."""
from .. import db

# ---------------------------------------------------------------- Consultas
CREATE_PLAYER = """
CREATE (p:Player {username: $username, name: $name, country: $country,
                  createdAt: datetime()})
RETURN p.username AS username
"""

LIST_PLAYERS = """
MATCH (p:Player)
OPTIONAL MATCH (p)-[r:PLAYED]->(:Game)
WITH p, count(r) AS games
RETURN p.username AS username, p.name AS name, p.country AS country, games,
       [(p)-[pl:PLAYED]->(g:Game) WHERE g.image IS NOT NULL | g.image][0] AS cover
ORDER BY name
"""

GET_PLAYER = """
MATCH (p:Player {username: $username})
RETURN p {.username, .name, .country} AS player,
       [(p)-[r:PLAYED]->(g:Game) |
           {id: g.id, title: g.title, image: g.image, rating: r.rating, hours: r.hours}] AS played,
       [(p)-[:FRIEND_OF]-(f:Player) | f {.username, .name}] AS friends
"""

UPDATE_PLAYER = """
MATCH (p:Player {username: $username})
SET p.name = $name, p.country = $country, p.updatedAt = datetime()
RETURN p.username AS username
"""

DELETE_PLAYER = """
MATCH (p:Player {username: $username})
DETACH DELETE p
RETURN count(*) AS deleted
"""

# MERGE sobre la relación: si ya existe se actualiza (upsert), si no se crea.
UPSERT_PLAY = """
MATCH (p:Player {username: $username}), (g:Game {id: $gameId})
MERGE (p)-[r:PLAYED]->(g)
SET r.rating = $rating, r.hours = $hours, r.updatedAt = datetime()
RETURN g.title AS title
"""

DELETE_PLAY = """
MATCH (:Player {username: $username})-[r:PLAYED]->(:Game {id: $gameId})
DELETE r
RETURN count(*) AS deleted
"""

# La amistad es simétrica: se guarda UNA relación dirigida y se consulta sin
# dirección (-[:FRIEND_OF]-). El MERGE sin dirección evita duplicados a->b y b->a.
ADD_FRIEND = """
MATCH (a:Player {username: $a}), (b:Player {username: $b})
WHERE a <> b
MERGE (a)-[r:FRIEND_OF]-(b)
ON CREATE SET r.since = date()
RETURN b.name AS name
"""

REMOVE_FRIEND = """
MATCH (:Player {username: $a})-[r:FRIEND_OF]-(:Player {username: $b})
DELETE r
RETURN count(*) AS deleted
"""


# ---------------------------------------------------------------- Funciones
def create_player(username, name, country):
    return db.write(CREATE_PLAYER, username=username, name=name, country=country)


def list_players():
    return db.read(LIST_PLAYERS)


def get_player(username):
    rows = db.read(GET_PLAYER, username=username)
    if not rows:
        return None
    data = rows[0]
    data["played"].sort(key=lambda g: (-g["rating"], -g["hours"]))
    data["friends"].sort(key=lambda f: f["name"])
    return data


def update_player(username, name, country):
    return bool(db.write(UPDATE_PLAYER, username=username, name=name, country=country))


def delete_player(username):
    return db.write(DELETE_PLAYER, username=username)[0]["deleted"] > 0


def upsert_play(username, game_id, rating, hours):
    return db.write(UPSERT_PLAY, username=username, gameId=game_id, rating=rating, hours=hours)


def delete_play(username, game_id):
    return db.write(DELETE_PLAY, username=username, gameId=game_id)[0]["deleted"] > 0


def add_friend(a, b):
    return db.write(ADD_FRIEND, a=a, b=b)


def remove_friend(a, b):
    return db.write(REMOVE_FRIEND, a=a, b=b)[0]["deleted"] > 0

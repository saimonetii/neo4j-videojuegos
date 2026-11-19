"""Motor de recomendación: consultas de recorrido (traversal) sobre el grafo.

Cada estrategia es un patrón de 2 a 4 saltos que en SQL requeriría varios
JOIN sobre tablas intermedias (y auto-JOIN sobre la tabla de jugadores).
"""
from .. import db

# 1) Filtrado colaborativo: jugadores con gustos parecidos a los míos
#    (calificaron los mismos juegos con +/- 1 estrella) -> juegos que ellos
#    calificaron alto y que yo no he jugado.
#    me -PLAYED-> juego <-PLAYED- otro -PLAYED-> recomendación   (3 saltos)
COLLABORATIVE = """
MATCH (me:Player {username: $username})-[mine:PLAYED]->(:Game)<-[theirs:PLAYED]-(other:Player)
WHERE other <> me AND abs(mine.rating - theirs.rating) <= 1
WITH me, other, count(*) AS affinity
MATCH (other)-[r:PLAYED]->(rec:Game)
WHERE r.rating >= 4 AND NOT EXISTS { (me)-[:PLAYED]->(rec) }
RETURN rec.id AS id, rec.title AS title,
       sum(affinity * r.rating) AS score,
       collect(DISTINCT other.name)[0..3] AS because
ORDER BY score DESC, title
LIMIT $limit
"""

# 2) Basado en contenido: géneros de mis juegos favoritos (rating >= 4)
#    -> otros juegos de esos géneros que no he jugado.
CONTENT_BASED = """
MATCH (me:Player {username: $username})-[r:PLAYED]->(:Game)-[:HAS_GENRE]->(ge:Genre)
WHERE r.rating >= 4
WITH me, ge, count(*) AS weight
MATCH (ge)<-[:HAS_GENRE]-(rec:Game)
WHERE NOT EXISTS { (me)-[:PLAYED]->(rec) }
RETURN rec.id AS id, rec.title AS title,
       sum(weight) AS score, collect(ge.name) AS genres
ORDER BY score DESC, title
LIMIT $limit
"""

# 3) Social: lo que mis amigos calificaron alto y yo no he jugado.
SOCIAL = """
MATCH (me:Player {username: $username})-[:FRIEND_OF]-(f:Player)-[r:PLAYED]->(rec:Game)
WHERE r.rating >= 4 AND NOT EXISTS { (me)-[:PLAYED]->(rec) }
RETURN rec.id AS id, rec.title AS title,
       count(DISTINCT f) AS friends, round(avg(r.rating), 1) AS avgRating,
       collect(DISTINCT f.name) AS byFriends
ORDER BY friends DESC, avgRating DESC, title
LIMIT $limit
"""

# 4) Sugerencia de amigos: amigos de mis amigos (vecindad a 2 saltos) que
#    aún no son mis amigos, ordenados por amigos en común y juegos en común.
FRIEND_SUGGESTIONS = """
MATCH (me:Player {username: $username})-[:FRIEND_OF]-(f:Player)-[:FRIEND_OF]-(fof:Player)
WHERE fof <> me AND NOT EXISTS { (me)-[:FRIEND_OF]-(fof) }
WITH me, fof, count(DISTINCT f) AS mutualFriends
OPTIONAL MATCH (me)-[:PLAYED]->(g:Game)<-[:PLAYED]-(fof)
RETURN fof.username AS username, fof.name AS name, mutualFriends,
       count(DISTINCT g) AS gamesInCommon
ORDER BY mutualFriends DESC, gamesInCommon DESC, name
LIMIT $limit
"""


def collaborative(username, limit=6):
    return db.read(COLLABORATIVE, username=username, limit=limit)


def content_based(username, limit=6):
    return db.read(CONTENT_BASED, username=username, limit=limit)


def social(username, limit=6):
    return db.read(SOCIAL, username=username, limit=limit)


def friend_suggestions(username, limit=5):
    return db.read(FRIEND_SUGGESTIONS, username=username, limit=limit)

"""Script de esquema + datos iniciales (seeding).

Uso (desde la raíz del proyecto):
    python -m database.seed              # borra todo, crea esquema y carga datos
    python -m database.seed --keep       # NO borra; solo hace MERGE (idempotente)
    python -m database.seed --export database/seed.cypher
                                         # genera un .cypher para la consola de Aura

Las cargas usan UNWIND $lista: un solo viaje de red por lote en lugar de una
consulta por fila, que es la práctica recomendada para cargas en Neo4j.
"""
import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent

# ------------------------------------------------------------------ Datos
# (id, título, año, desarrollador, [géneros], [plataformas], descripción)
GAMES = [
    ("the-witcher-3", "The Witcher 3: Wild Hunt", 2015, "CD Projekt Red", ["RPG", "Mundo abierto", "Acción"], ["PC", "PS5", "Xbox Series", "Switch"], "Geralt de Rivia busca a Ciri en un enorme mundo de fantasía oscura."),
    ("elden-ring", "Elden Ring", 2022, "FromSoftware", ["RPG", "Acción", "Soulslike", "Mundo abierto"], ["PC", "PS5", "Xbox Series"], "Mundo abierto con combate exigente en las Tierras Intermedias."),
    ("dark-souls-3", "Dark Souls III", 2016, "FromSoftware", ["RPG", "Acción", "Soulslike"], ["PC", "PS4", "Xbox One"], "Combate desafiante y exploración en el reino de Lothric."),
    ("sekiro", "Sekiro: Shadows Die Twice", 2019, "FromSoftware", ["Acción", "Soulslike", "Aventura"], ["PC", "PS4", "Xbox One"], "Un shinobi en el Japón de la era Sengoku; combate de parrys."),
    ("cyberpunk-2077", "Cyberpunk 2077", 2020, "CD Projekt Red", ["RPG", "Mundo abierto", "Shooter"], ["PC", "PS5", "Xbox Series"], "RPG en primera persona en la megalópolis de Night City."),
    ("baldurs-gate-3", "Baldur's Gate 3", 2023, "Larian Studios", ["RPG", "Estrategia"], ["PC", "PS5", "Xbox Series"], "RPG por turnos basado en Dungeons & Dragons."),
    ("divinity-os2", "Divinity: Original Sin 2", 2017, "Larian Studios", ["RPG", "Estrategia"], ["PC", "PS4", "Switch"], "RPG táctico por turnos con gran libertad de decisiones."),
    ("hollow-knight", "Hollow Knight", 2017, "Team Cherry", ["Metroidvania", "Indie", "Plataformas"], ["PC", "Switch", "PS4"], "Exploración de un reino de insectos en ruinas."),
    ("celeste", "Celeste", 2018, "Extremely OK Games", ["Plataformas", "Indie"], ["PC", "Switch"], "Plataformas de precisión sobre escalar una montaña."),
    ("hades", "Hades", 2020, "Supergiant Games", ["Roguelike", "Acción", "Indie"], ["PC", "Switch", "PS5"], "Zagreus intenta escapar del inframundo griego."),
    ("dead-cells", "Dead Cells", 2018, "Motion Twin", ["Roguelike", "Metroidvania", "Indie"], ["PC", "Switch", "PS4"], "Roguelite de acción con progresión entre partidas."),
    ("stardew-valley", "Stardew Valley", 2016, "ConcernedApe", ["Simulación", "Indie", "RPG"], ["PC", "Switch", "PS4"], "Granja, pesca y vida de pueblo a tu propio ritmo."),
    ("minecraft", "Minecraft", 2011, "Mojang Studios", ["Sandbox", "Supervivencia"], ["PC", "Switch", "PS4", "Xbox One"], "Construye y sobrevive en un mundo de bloques."),
    ("terraria", "Terraria", 2011, "Re-Logic", ["Sandbox", "Supervivencia", "Indie"], ["PC", "Switch"], "Sandbox 2D de exploración, construcción y jefes."),
    ("valorant", "Valorant", 2020, "Riot Games", ["Shooter", "Competitivo"], ["PC"], "Shooter táctico 5 contra 5 con habilidades."),
    ("cs2", "Counter-Strike 2", 2023, "Valve", ["Shooter", "Competitivo"], ["PC"], "El clásico shooter táctico competitivo."),
    ("overwatch-2", "Overwatch 2", 2022, "Blizzard Entertainment", ["Shooter", "Competitivo"], ["PC", "PS5", "Xbox Series", "Switch"], "Shooter de héroes por equipos."),
    ("apex-legends", "Apex Legends", 2019, "Respawn Entertainment", ["Shooter", "Battle Royale", "Competitivo"], ["PC", "PS5", "Xbox Series"], "Battle royale por escuadras con leyendas."),
    ("fortnite", "Fortnite", 2017, "Epic Games", ["Shooter", "Battle Royale"], ["PC", "PS5", "Xbox Series", "Switch"], "Battle royale con construcción."),
    ("league-of-legends", "League of Legends", 2009, "Riot Games", ["MOBA", "Competitivo", "Estrategia"], ["PC"], "MOBA 5 contra 5 por equipos."),
    ("fc-25", "EA Sports FC 25", 2024, "EA Sports", ["Deportes", "Competitivo"], ["PC", "PS5", "Xbox Series"], "Simulador de fútbol."),
    ("rocket-league", "Rocket League", 2015, "Psyonix", ["Deportes", "Competitivo"], ["PC", "PS5", "Switch"], "Fútbol con autos propulsados."),
    ("zelda-totk", "The Legend of Zelda: Tears of the Kingdom", 2023, "Nintendo", ["Aventura", "Mundo abierto", "Acción"], ["Switch"], "Link explora Hyrule, sus cielos y sus profundidades."),
    ("mario-kart-8", "Mario Kart 8 Deluxe", 2017, "Nintendo", ["Carreras"], ["Switch"], "Carreras de karts para jugar en grupo."),
    ("smash-ultimate", "Super Smash Bros. Ultimate", 2018, "Sora Ltd.", ["Pelea", "Competitivo"], ["Switch"], "Juego de pelea de plataformas con decenas de personajes."),
    ("gta-v", "Grand Theft Auto V", 2013, "Rockstar Games", ["Acción", "Mundo abierto"], ["PC", "PS5", "Xbox Series"], "Tres protagonistas en la ciudad de Los Santos."),
    ("rdr2", "Red Dead Redemption 2", 2018, "Rockstar Games", ["Acción", "Mundo abierto", "Aventura"], ["PC", "PS4", "Xbox One"], "La banda de Van der Linde en el ocaso del Viejo Oeste."),
    ("god-of-war-ragnarok", "God of War Ragnarök", 2022, "Santa Monica Studio", ["Acción", "Aventura"], ["PS5", "PC"], "Kratos y Atreus frente al Ragnarök nórdico."),
    ("street-fighter-6", "Street Fighter 6", 2023, "Capcom", ["Pelea", "Competitivo"], ["PC", "PS5", "Xbox Series"], "Juego de pelea 1 contra 1."),
    ("resident-evil-4", "Resident Evil 4", 2023, "Capcom", ["Survival horror", "Acción"], ["PC", "PS5", "Xbox Series"], "Remake del clásico de horror y acción."),
    ("portal-2", "Portal 2", 2011, "Valve", ["Puzzle", "Aventura"], ["PC"], "Rompecabezas con portales y mucho humor."),
    ("it-takes-two", "It Takes Two", 2021, "Hazelight Studios", ["Aventura", "Plataformas", "Cooperativo"], ["PC", "PS5", "Xbox Series", "Switch"], "Aventura cooperativa obligatoria para dos."),
]

# Portadas: imagen "header" oficial de la tienda de Steam (los juegos que no
# están en Steam quedan sin imagen y la página muestra la inicial del título).
STEAM_APP_IDS = {
    "the-witcher-3": 292030, "elden-ring": 1245620, "dark-souls-3": 374320, "sekiro": 814380,
    "cyberpunk-2077": 1091500, "baldurs-gate-3": 1086940, "divinity-os2": 435150,
    "hollow-knight": 367520, "celeste": 504230, "hades": 1145360, "dead-cells": 588650,
    "stardew-valley": 413150, "terraria": 105600, "cs2": 730, "overwatch-2": 2357570,
    "apex-legends": 1172470, "fc-25": 2669320, "rocket-league": 252950, "gta-v": 271590,
    "rdr2": 1174180, "god-of-war-ragnarok": 2322010, "street-fighter-6": 1364780,
    "resident-evil-4": 2050650, "portal-2": 620, "it-takes-two": 1426210,
}
STEAM_HEADER = "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/{}/header.jpg"


def image_for(game_id):
    app_id = STEAM_APP_IDS.get(game_id)
    return STEAM_HEADER.format(app_id) if app_id else None


# (username, nombre, país)
PLAYERS = [
    ("ana_rpg", "Ana López", "MX"),
    ("beto_fps", "Alberto Ruiz", "MX"),
    ("carla_indie", "Carla Méndez", "MX"),
    ("diego", "Diego Hernández", "MX"),
    ("elena", "Elena Torres", "CO"),
    ("fer_gamer", "Fernanda Castillo", "MX"),
    ("gabo", "Gabriel Pérez", "AR"),
    ("hugo", "Hugo Martínez", "ES"),
    ("isa", "Isabel Gómez", "MX"),
    ("javi", "Javier Morales", "MX"),
    ("karla", "Karla Díaz", "CL"),
    ("luis", "Luis Ramírez", "MX"),
]

# (username, juego, calificación 1-5, horas)
PLAYS = [
    ("ana_rpg", "the-witcher-3", 5, 180), ("ana_rpg", "elden-ring", 5, 140), ("ana_rpg", "baldurs-gate-3", 5, 120),
    ("ana_rpg", "dark-souls-3", 4, 90), ("ana_rpg", "divinity-os2", 4, 80), ("ana_rpg", "stardew-valley", 3, 40),
    ("beto_fps", "valorant", 5, 400), ("beto_fps", "cs2", 5, 600), ("beto_fps", "apex-legends", 4, 200),
    ("beto_fps", "overwatch-2", 3, 80), ("beto_fps", "fortnite", 3, 60), ("beto_fps", "cyberpunk-2077", 4, 70),
    ("carla_indie", "hollow-knight", 5, 60), ("carla_indie", "celeste", 5, 40), ("carla_indie", "hades", 5, 90),
    ("carla_indie", "dead-cells", 4, 50), ("carla_indie", "stardew-valley", 5, 150), ("carla_indie", "terraria", 4, 100),
    ("carla_indie", "portal-2", 4, 15),
    ("diego", "the-witcher-3", 5, 150), ("diego", "cyberpunk-2077", 5, 110), ("diego", "elden-ring", 4, 100),
    ("diego", "gta-v", 4, 200), ("diego", "rdr2", 5, 130), ("diego", "baldurs-gate-3", 4, 70),
    ("elena", "stardew-valley", 5, 200), ("elena", "minecraft", 5, 300), ("elena", "terraria", 5, 150),
    ("elena", "celeste", 4, 30), ("elena", "hollow-knight", 4, 45), ("elena", "it-takes-two", 5, 20),
    ("elena", "portal-2", 4, 12),
    ("fer_gamer", "valorant", 5, 500), ("fer_gamer", "league-of-legends", 5, 900), ("fer_gamer", "overwatch-2", 4, 150),
    ("fer_gamer", "apex-legends", 4, 120), ("fer_gamer", "cs2", 3, 50), ("fer_gamer", "street-fighter-6", 3, 30),
    ("gabo", "fc-25", 5, 300), ("gabo", "rocket-league", 5, 250), ("gabo", "fortnite", 3, 40),
    ("gabo", "mario-kart-8", 4, 30), ("gabo", "gta-v", 3, 60),
    ("hugo", "elden-ring", 5, 200), ("hugo", "dark-souls-3", 5, 160), ("hugo", "sekiro", 5, 110),
    ("hugo", "hollow-knight", 4, 60), ("hugo", "god-of-war-ragnarok", 4, 50), ("hugo", "resident-evil-4", 4, 30),
    ("isa", "zelda-totk", 5, 180), ("isa", "mario-kart-8", 5, 90), ("isa", "smash-ultimate", 4, 100),
    ("isa", "stardew-valley", 4, 80), ("isa", "celeste", 4, 25), ("isa", "minecraft", 3, 40),
    ("isa", "it-takes-two", 5, 15),
    ("javi", "gta-v", 5, 400), ("javi", "rdr2", 5, 200), ("javi", "cyberpunk-2077", 4, 90),
    ("javi", "god-of-war-ragnarok", 5, 45), ("javi", "resident-evil-4", 4, 25), ("javi", "the-witcher-3", 4, 100),
    ("karla", "street-fighter-6", 5, 200), ("karla", "smash-ultimate", 5, 250), ("karla", "mario-kart-8", 4, 60),
    ("karla", "zelda-totk", 4, 90), ("karla", "rocket-league", 3, 20), ("karla", "overwatch-2", 3, 25),
    ("luis", "elden-ring", 4, 30), ("luis", "hollow-knight", 5, 20), ("luis", "valorant", 3, 15),
]

# (jugador A, jugador B, fecha) — se guarda A->B y se consulta sin dirección
FRIENDSHIPS = [
    ("ana_rpg", "diego", "2021-03-14"), ("ana_rpg", "hugo", "2022-07-01"), ("ana_rpg", "carla_indie", "2020-11-20"),
    ("beto_fps", "fer_gamer", "2019-05-02"), ("beto_fps", "gabo", "2018-09-10"), ("beto_fps", "javi", "2021-01-15"),
    ("carla_indie", "elena", "2020-02-28"), ("carla_indie", "isa", "2022-04-17"), ("diego", "javi", "2017-08-08"),
    ("elena", "isa", "2023-06-30"), ("fer_gamer", "karla", "2021-10-05"), ("gabo", "karla", "2022-12-24"),
    ("hugo", "luis", "2024-01-09"), ("isa", "karla", "2020-06-12"),
]

# ------------------------------------------------------------------ Consultas
WIPE = "MATCH (n) DETACH DELETE n"

LOAD_GAMES = """
UNWIND $rows AS row
MERGE (g:Game {id: row.id})
SET g.title = row.title, g.year = row.year, g.description = row.description,
    g.image = row.image
MERGE (d:Developer {name: row.developer})
MERGE (g)-[:DEVELOPED_BY]->(d)
FOREACH (name IN row.genres |
    MERGE (ge:Genre {name: name})
    MERGE (g)-[:HAS_GENRE]->(ge))
FOREACH (name IN row.platforms |
    MERGE (pf:Platform {name: name})
    MERGE (g)-[:AVAILABLE_ON]->(pf))
"""

LOAD_PLAYERS = """
UNWIND $rows AS row
MERGE (p:Player {username: row.username})
SET p.name = row.name, p.country = row.country,
    p.createdAt = coalesce(p.createdAt, datetime())
"""

LOAD_PLAYS = """
UNWIND $rows AS row
MATCH (p:Player {username: row.username})
MATCH (g:Game {id: row.game})
MERGE (p)-[r:PLAYED]->(g)
SET r.rating = row.rating, r.hours = row.hours
"""

LOAD_FRIENDSHIPS = """
UNWIND $rows AS row
MATCH (a:Player {username: row.a})
MATCH (b:Player {username: row.b})
MERGE (a)-[r:FRIEND_OF]-(b)
SET r.since = date(row.since)
"""


def rows():
    """Convierte las tuplas en listas de diccionarios (parámetros de UNWIND)."""
    return {
        "games": [dict(zip(("id", "title", "year", "developer", "genres", "platforms", "description"), g),
                       image=image_for(g[0])) for g in GAMES],
        "players": [dict(zip(("username", "name", "country"), p)) for p in PLAYERS],
        "plays": [dict(zip(("username", "game", "rating", "hours"), p)) for p in PLAYS],
        "friendships": [dict(zip(("a", "b", "since"), f)) for f in FRIENDSHIPS],
    }


def schema_statements():
    text = (ROOT / "schema.cypher").read_text(encoding="utf-8")
    lines = [line for line in text.splitlines() if not line.strip().startswith("//")]
    return [stmt.strip() for stmt in "\n".join(lines).split(";") if stmt.strip()]


def run(keep=False):
    sys.path.insert(0, str(ROOT.parent))
    from app import db

    db.init_driver()
    print(f"Conectado a {db.server_info()['address']}")
    if not keep:
        db.write(WIPE)
        print("· Base de datos vaciada")
    for stmt in schema_statements():
        db.write(stmt)
    print("· Restricciones e índices creados")
    data = rows()
    db.write(LOAD_GAMES, rows=data["games"])
    db.write(LOAD_PLAYERS, rows=data["players"])
    db.write(LOAD_PLAYS, rows=data["plays"])
    db.write(LOAD_FRIENDSHIPS, rows=data["friendships"])
    print(f"· {len(GAMES)} juegos, {len(PLAYERS)} jugadores, {len(PLAYS)} partidas, "
          f"{len(FRIENDSHIPS)} amistades")
    for row in db.read("MATCH (n) RETURN labels(n)[0] AS label, count(*) AS total ORDER BY label"):
        print(f"  :{row['label']:<10} {row['total']}")
    db.close_driver()
    print("Listo.")


# ------------------------------------------------------- Exportar a .cypher
def to_cypher(value):
    """Convierte un valor de Python a literal de Cypher (para el .cypher exportado)."""
    if isinstance(value, dict):
        return "{" + ", ".join(f"{k}: {to_cypher(v)}" for k, v in value.items()) + "}"
    if isinstance(value, (list, tuple)):
        return "[" + ", ".join(to_cypher(v) for v in value) + "]"
    return json.dumps(value, ensure_ascii=False)


def export(path):
    data = rows()
    parts = [
        "// Datos iniciales generados con: python -m database.seed --export database/seed.cypher",
        "// Pegar en la consola Query de AuraDB DESPUÉS de schema.cypher.",
        "// Cada bloque es una sentencia independiente separada por ';'.",
        "",
        WIPE + ";",
        "",
    ]
    for key, query in (("games", LOAD_GAMES), ("players", LOAD_PLAYERS),
                       ("plays", LOAD_PLAYS), ("friendships", LOAD_FRIENDSHIPS)):
        literal = "[\n  " + ",\n  ".join(to_cypher(r) for r in data[key]) + "\n]"
        parts.append(f"// ---- {key}")
        parts.append(query.strip().replace("UNWIND $rows AS row", f"UNWIND {literal} AS row") + ";")
        parts.append("")
    pathlib.Path(path).write_text("\n".join(parts), encoding="utf-8")
    print(f"Exportado a {path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Esquema + datos iniciales")
    parser.add_argument("--keep", action="store_true", help="no borrar los datos existentes")
    parser.add_argument("--export", metavar="ARCHIVO", help="generar archivo .cypher y salir")
    args = parser.parse_args()
    if args.export:
        export(args.export)
    else:
        run(keep=args.keep)

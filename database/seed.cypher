// Datos iniciales generados con: python -m database.seed --export database/seed.cypher
// Pegar en la consola Query de AuraDB DESPUÉS de schema.cypher.
// Cada bloque es una sentencia independiente separada por ';'.

MATCH (n) DETACH DELETE n;

// ---- games
UNWIND [
  {id: "the-witcher-3", title: "The Witcher 3: Wild Hunt", year: 2015, developer: "CD Projekt Red", genres: ["RPG", "Mundo abierto", "Acción"], platforms: ["PC", "PS5", "Xbox Series", "Switch"], description: "Geralt de Rivia busca a Ciri en un enorme mundo de fantasía oscura."},
  {id: "elden-ring", title: "Elden Ring", year: 2022, developer: "FromSoftware", genres: ["RPG", "Acción", "Soulslike", "Mundo abierto"], platforms: ["PC", "PS5", "Xbox Series"], description: "Mundo abierto con combate exigente en las Tierras Intermedias."},
  {id: "dark-souls-3", title: "Dark Souls III", year: 2016, developer: "FromSoftware", genres: ["RPG", "Acción", "Soulslike"], platforms: ["PC", "PS4", "Xbox One"], description: "Combate desafiante y exploración en el reino de Lothric."},
  {id: "sekiro", title: "Sekiro: Shadows Die Twice", year: 2019, developer: "FromSoftware", genres: ["Acción", "Soulslike", "Aventura"], platforms: ["PC", "PS4", "Xbox One"], description: "Un shinobi en el Japón de la era Sengoku; combate de parrys."},
  {id: "cyberpunk-2077", title: "Cyberpunk 2077", year: 2020, developer: "CD Projekt Red", genres: ["RPG", "Mundo abierto", "Shooter"], platforms: ["PC", "PS5", "Xbox Series"], description: "RPG en primera persona en la megalópolis de Night City."},
  {id: "baldurs-gate-3", title: "Baldur's Gate 3", year: 2023, developer: "Larian Studios", genres: ["RPG", "Estrategia"], platforms: ["PC", "PS5", "Xbox Series"], description: "RPG por turnos basado en Dungeons & Dragons."},
  {id: "divinity-os2", title: "Divinity: Original Sin 2", year: 2017, developer: "Larian Studios", genres: ["RPG", "Estrategia"], platforms: ["PC", "PS4", "Switch"], description: "RPG táctico por turnos con gran libertad de decisiones."},
  {id: "hollow-knight", title: "Hollow Knight", year: 2017, developer: "Team Cherry", genres: ["Metroidvania", "Indie", "Plataformas"], platforms: ["PC", "Switch", "PS4"], description: "Exploración de un reino de insectos en ruinas."},
  {id: "celeste", title: "Celeste", year: 2018, developer: "Extremely OK Games", genres: ["Plataformas", "Indie"], platforms: ["PC", "Switch"], description: "Plataformas de precisión sobre escalar una montaña."},
  {id: "hades", title: "Hades", year: 2020, developer: "Supergiant Games", genres: ["Roguelike", "Acción", "Indie"], platforms: ["PC", "Switch", "PS5"], description: "Zagreus intenta escapar del inframundo griego."},
  {id: "dead-cells", title: "Dead Cells", year: 2018, developer: "Motion Twin", genres: ["Roguelike", "Metroidvania", "Indie"], platforms: ["PC", "Switch", "PS4"], description: "Roguelite de acción con progresión entre partidas."},
  {id: "stardew-valley", title: "Stardew Valley", year: 2016, developer: "ConcernedApe", genres: ["Simulación", "Indie", "RPG"], platforms: ["PC", "Switch", "PS4"], description: "Granja, pesca y vida de pueblo a tu propio ritmo."},
  {id: "minecraft", title: "Minecraft", year: 2011, developer: "Mojang Studios", genres: ["Sandbox", "Supervivencia"], platforms: ["PC", "Switch", "PS4", "Xbox One"], description: "Construye y sobrevive en un mundo de bloques."},
  {id: "terraria", title: "Terraria", year: 2011, developer: "Re-Logic", genres: ["Sandbox", "Supervivencia", "Indie"], platforms: ["PC", "Switch"], description: "Sandbox 2D de exploración, construcción y jefes."},
  {id: "valorant", title: "Valorant", year: 2020, developer: "Riot Games", genres: ["Shooter", "Competitivo"], platforms: ["PC"], description: "Shooter táctico 5 contra 5 con habilidades."},
  {id: "cs2", title: "Counter-Strike 2", year: 2023, developer: "Valve", genres: ["Shooter", "Competitivo"], platforms: ["PC"], description: "El clásico shooter táctico competitivo."},
  {id: "overwatch-2", title: "Overwatch 2", year: 2022, developer: "Blizzard Entertainment", genres: ["Shooter", "Competitivo"], platforms: ["PC", "PS5", "Xbox Series", "Switch"], description: "Shooter de héroes por equipos."},
  {id: "apex-legends", title: "Apex Legends", year: 2019, developer: "Respawn Entertainment", genres: ["Shooter", "Battle Royale", "Competitivo"], platforms: ["PC", "PS5", "Xbox Series"], description: "Battle royale por escuadras con leyendas."},
  {id: "fortnite", title: "Fortnite", year: 2017, developer: "Epic Games", genres: ["Shooter", "Battle Royale"], platforms: ["PC", "PS5", "Xbox Series", "Switch"], description: "Battle royale con construcción."},
  {id: "league-of-legends", title: "League of Legends", year: 2009, developer: "Riot Games", genres: ["MOBA", "Competitivo", "Estrategia"], platforms: ["PC"], description: "MOBA 5 contra 5 por equipos."},
  {id: "fc-25", title: "EA Sports FC 25", year: 2024, developer: "EA Sports", genres: ["Deportes", "Competitivo"], platforms: ["PC", "PS5", "Xbox Series"], description: "Simulador de fútbol."},
  {id: "rocket-league", title: "Rocket League", year: 2015, developer: "Psyonix", genres: ["Deportes", "Competitivo"], platforms: ["PC", "PS5", "Switch"], description: "Fútbol con autos propulsados."},
  {id: "zelda-totk", title: "The Legend of Zelda: Tears of the Kingdom", year: 2023, developer: "Nintendo", genres: ["Aventura", "Mundo abierto", "Acción"], platforms: ["Switch"], description: "Link explora Hyrule, sus cielos y sus profundidades."},
  {id: "mario-kart-8", title: "Mario Kart 8 Deluxe", year: 2017, developer: "Nintendo", genres: ["Carreras"], platforms: ["Switch"], description: "Carreras de karts para jugar en grupo."},
  {id: "smash-ultimate", title: "Super Smash Bros. Ultimate", year: 2018, developer: "Sora Ltd.", genres: ["Pelea", "Competitivo"], platforms: ["Switch"], description: "Juego de pelea de plataformas con decenas de personajes."},
  {id: "gta-v", title: "Grand Theft Auto V", year: 2013, developer: "Rockstar Games", genres: ["Acción", "Mundo abierto"], platforms: ["PC", "PS5", "Xbox Series"], description: "Tres protagonistas en la ciudad de Los Santos."},
  {id: "rdr2", title: "Red Dead Redemption 2", year: 2018, developer: "Rockstar Games", genres: ["Acción", "Mundo abierto", "Aventura"], platforms: ["PC", "PS4", "Xbox One"], description: "La banda de Van der Linde en el ocaso del Viejo Oeste."},
  {id: "god-of-war-ragnarok", title: "God of War Ragnarök", year: 2022, developer: "Santa Monica Studio", genres: ["Acción", "Aventura"], platforms: ["PS5", "PC"], description: "Kratos y Atreus frente al Ragnarök nórdico."},
  {id: "street-fighter-6", title: "Street Fighter 6", year: 2023, developer: "Capcom", genres: ["Pelea", "Competitivo"], platforms: ["PC", "PS5", "Xbox Series"], description: "Juego de pelea 1 contra 1."},
  {id: "resident-evil-4", title: "Resident Evil 4", year: 2023, developer: "Capcom", genres: ["Survival horror", "Acción"], platforms: ["PC", "PS5", "Xbox Series"], description: "Remake del clásico de horror y acción."},
  {id: "portal-2", title: "Portal 2", year: 2011, developer: "Valve", genres: ["Puzzle", "Aventura"], platforms: ["PC"], description: "Rompecabezas con portales y mucho humor."},
  {id: "it-takes-two", title: "It Takes Two", year: 2021, developer: "Hazelight Studios", genres: ["Aventura", "Plataformas", "Cooperativo"], platforms: ["PC", "PS5", "Xbox Series", "Switch"], description: "Aventura cooperativa obligatoria para dos."}
] AS row
MERGE (g:Game {id: row.id})
SET g.title = row.title, g.year = row.year, g.description = row.description
MERGE (d:Developer {name: row.developer})
MERGE (g)-[:DEVELOPED_BY]->(d)
FOREACH (name IN row.genres |
    MERGE (ge:Genre {name: name})
    MERGE (g)-[:HAS_GENRE]->(ge))
FOREACH (name IN row.platforms |
    MERGE (pf:Platform {name: name})
    MERGE (g)-[:AVAILABLE_ON]->(pf));

// ---- players
UNWIND [
  {username: "ana_rpg", name: "Ana López", country: "MX"},
  {username: "beto_fps", name: "Alberto Ruiz", country: "MX"},
  {username: "carla_indie", name: "Carla Méndez", country: "MX"},
  {username: "diego", name: "Diego Hernández", country: "MX"},
  {username: "elena", name: "Elena Torres", country: "CO"},
  {username: "fer_gamer", name: "Fernanda Castillo", country: "MX"},
  {username: "gabo", name: "Gabriel Pérez", country: "AR"},
  {username: "hugo", name: "Hugo Martínez", country: "ES"},
  {username: "isa", name: "Isabel Gómez", country: "MX"},
  {username: "javi", name: "Javier Morales", country: "MX"},
  {username: "karla", name: "Karla Díaz", country: "CL"},
  {username: "luis", name: "Luis Ramírez", country: "MX"}
] AS row
MERGE (p:Player {username: row.username})
SET p.name = row.name, p.country = row.country,
    p.createdAt = coalesce(p.createdAt, datetime());

// ---- plays
UNWIND [
  {username: "ana_rpg", game: "the-witcher-3", rating: 5, hours: 180},
  {username: "ana_rpg", game: "elden-ring", rating: 5, hours: 140},
  {username: "ana_rpg", game: "baldurs-gate-3", rating: 5, hours: 120},
  {username: "ana_rpg", game: "dark-souls-3", rating: 4, hours: 90},
  {username: "ana_rpg", game: "divinity-os2", rating: 4, hours: 80},
  {username: "ana_rpg", game: "stardew-valley", rating: 3, hours: 40},
  {username: "beto_fps", game: "valorant", rating: 5, hours: 400},
  {username: "beto_fps", game: "cs2", rating: 5, hours: 600},
  {username: "beto_fps", game: "apex-legends", rating: 4, hours: 200},
  {username: "beto_fps", game: "overwatch-2", rating: 3, hours: 80},
  {username: "beto_fps", game: "fortnite", rating: 3, hours: 60},
  {username: "beto_fps", game: "cyberpunk-2077", rating: 4, hours: 70},
  {username: "carla_indie", game: "hollow-knight", rating: 5, hours: 60},
  {username: "carla_indie", game: "celeste", rating: 5, hours: 40},
  {username: "carla_indie", game: "hades", rating: 5, hours: 90},
  {username: "carla_indie", game: "dead-cells", rating: 4, hours: 50},
  {username: "carla_indie", game: "stardew-valley", rating: 5, hours: 150},
  {username: "carla_indie", game: "terraria", rating: 4, hours: 100},
  {username: "carla_indie", game: "portal-2", rating: 4, hours: 15},
  {username: "diego", game: "the-witcher-3", rating: 5, hours: 150},
  {username: "diego", game: "cyberpunk-2077", rating: 5, hours: 110},
  {username: "diego", game: "elden-ring", rating: 4, hours: 100},
  {username: "diego", game: "gta-v", rating: 4, hours: 200},
  {username: "diego", game: "rdr2", rating: 5, hours: 130},
  {username: "diego", game: "baldurs-gate-3", rating: 4, hours: 70},
  {username: "elena", game: "stardew-valley", rating: 5, hours: 200},
  {username: "elena", game: "minecraft", rating: 5, hours: 300},
  {username: "elena", game: "terraria", rating: 5, hours: 150},
  {username: "elena", game: "celeste", rating: 4, hours: 30},
  {username: "elena", game: "hollow-knight", rating: 4, hours: 45},
  {username: "elena", game: "it-takes-two", rating: 5, hours: 20},
  {username: "elena", game: "portal-2", rating: 4, hours: 12},
  {username: "fer_gamer", game: "valorant", rating: 5, hours: 500},
  {username: "fer_gamer", game: "league-of-legends", rating: 5, hours: 900},
  {username: "fer_gamer", game: "overwatch-2", rating: 4, hours: 150},
  {username: "fer_gamer", game: "apex-legends", rating: 4, hours: 120},
  {username: "fer_gamer", game: "cs2", rating: 3, hours: 50},
  {username: "fer_gamer", game: "street-fighter-6", rating: 3, hours: 30},
  {username: "gabo", game: "fc-25", rating: 5, hours: 300},
  {username: "gabo", game: "rocket-league", rating: 5, hours: 250},
  {username: "gabo", game: "fortnite", rating: 3, hours: 40},
  {username: "gabo", game: "mario-kart-8", rating: 4, hours: 30},
  {username: "gabo", game: "gta-v", rating: 3, hours: 60},
  {username: "hugo", game: "elden-ring", rating: 5, hours: 200},
  {username: "hugo", game: "dark-souls-3", rating: 5, hours: 160},
  {username: "hugo", game: "sekiro", rating: 5, hours: 110},
  {username: "hugo", game: "hollow-knight", rating: 4, hours: 60},
  {username: "hugo", game: "god-of-war-ragnarok", rating: 4, hours: 50},
  {username: "hugo", game: "resident-evil-4", rating: 4, hours: 30},
  {username: "isa", game: "zelda-totk", rating: 5, hours: 180},
  {username: "isa", game: "mario-kart-8", rating: 5, hours: 90},
  {username: "isa", game: "smash-ultimate", rating: 4, hours: 100},
  {username: "isa", game: "stardew-valley", rating: 4, hours: 80},
  {username: "isa", game: "celeste", rating: 4, hours: 25},
  {username: "isa", game: "minecraft", rating: 3, hours: 40},
  {username: "isa", game: "it-takes-two", rating: 5, hours: 15},
  {username: "javi", game: "gta-v", rating: 5, hours: 400},
  {username: "javi", game: "rdr2", rating: 5, hours: 200},
  {username: "javi", game: "cyberpunk-2077", rating: 4, hours: 90},
  {username: "javi", game: "god-of-war-ragnarok", rating: 5, hours: 45},
  {username: "javi", game: "resident-evil-4", rating: 4, hours: 25},
  {username: "javi", game: "the-witcher-3", rating: 4, hours: 100},
  {username: "karla", game: "street-fighter-6", rating: 5, hours: 200},
  {username: "karla", game: "smash-ultimate", rating: 5, hours: 250},
  {username: "karla", game: "mario-kart-8", rating: 4, hours: 60},
  {username: "karla", game: "zelda-totk", rating: 4, hours: 90},
  {username: "karla", game: "rocket-league", rating: 3, hours: 20},
  {username: "karla", game: "overwatch-2", rating: 3, hours: 25},
  {username: "luis", game: "elden-ring", rating: 4, hours: 30},
  {username: "luis", game: "hollow-knight", rating: 5, hours: 20},
  {username: "luis", game: "valorant", rating: 3, hours: 15}
] AS row
MATCH (p:Player {username: row.username})
MATCH (g:Game {id: row.game})
MERGE (p)-[r:PLAYED]->(g)
SET r.rating = row.rating, r.hours = row.hours;

// ---- friendships
UNWIND [
  {a: "ana_rpg", b: "diego", since: "2021-03-14"},
  {a: "ana_rpg", b: "hugo", since: "2022-07-01"},
  {a: "ana_rpg", b: "carla_indie", since: "2020-11-20"},
  {a: "beto_fps", b: "fer_gamer", since: "2019-05-02"},
  {a: "beto_fps", b: "gabo", since: "2018-09-10"},
  {a: "beto_fps", b: "javi", since: "2021-01-15"},
  {a: "carla_indie", b: "elena", since: "2020-02-28"},
  {a: "carla_indie", b: "isa", since: "2022-04-17"},
  {a: "diego", b: "javi", since: "2017-08-08"},
  {a: "elena", b: "isa", since: "2023-06-30"},
  {a: "fer_gamer", b: "karla", since: "2021-10-05"},
  {a: "gabo", b: "karla", since: "2022-12-24"},
  {a: "hugo", b: "luis", since: "2024-01-09"},
  {a: "isa", b: "karla", since: "2020-06-12"}
] AS row
MATCH (a:Player {username: row.a})
MATCH (b:Player {username: row.b})
MERGE (a)-[r:FRIEND_OF]-(b)
SET r.since = date(row.since);

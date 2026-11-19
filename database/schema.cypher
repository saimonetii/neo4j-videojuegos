// =====================================================================
//  Esquema de la base de grafo (Neo4j 5 / AuraDB)
//  Se ejecuta automáticamente con:  python -m database.seed
//  También se puede pegar en la consola "Query" de AuraDB.
// =====================================================================

// Restricciones de unicidad (cada una crea además un índice de rango)
CREATE CONSTRAINT player_username IF NOT EXISTS
FOR (p:Player) REQUIRE p.username IS UNIQUE;

CREATE CONSTRAINT game_id IF NOT EXISTS
FOR (g:Game) REQUIRE g.id IS UNIQUE;

CREATE CONSTRAINT genre_name IF NOT EXISTS
FOR (ge:Genre) REQUIRE ge.name IS UNIQUE;

CREATE CONSTRAINT platform_name IF NOT EXISTS
FOR (pf:Platform) REQUIRE pf.name IS UNIQUE;

CREATE CONSTRAINT developer_name IF NOT EXISTS
FOR (d:Developer) REQUIRE d.name IS UNIQUE;

// Índice adicional para búsquedas por título
CREATE INDEX game_title IF NOT EXISTS
FOR (g:Game) ON (g.title);

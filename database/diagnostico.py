"""Diagnóstico de conexión a AuraDB.

Uso:  python -m database.diagnostico
Prueba varias combinaciones de URI y base de datos e indica cuál funciona.
No muestra la contraseña.
"""
from dotenv import dotenv_values
from neo4j import GraphDatabase

vals = dotenv_values(".env", encoding="utf-8-sig")
user = vals.get("NEO4J_USERNAME") or "neo4j"
pwd = vals.get("NEO4J_PASSWORD") or ""
uri_cfg = vals.get("NEO4J_URI") or ""
inst = vals.get("AURA_INSTANCEID") or uri_cfg.split("//")[-1].split(".")[0]

print("=== Lo que hay en .env ===")
print(f"NEO4J_URI       = {uri_cfg or '(vacío)'}")
print(f"NEO4J_USERNAME  = {user}")
print(f"NEO4J_PASSWORD  = {'*' * len(pwd)} ({len(pwd)} caracteres)")
print(f"NEO4J_DATABASE  = {vals.get('NEO4J_DATABASE') or '(vacío -> base por defecto)'}")
print(f"Instancia       = {inst}")
print()

ok = []
for scheme in ("neo4j+s", "bolt+s"):
    uri = f"{scheme}://{inst}.databases.neo4j.io"
    print(f"=== {uri} ===")
    try:
        driver = GraphDatabase.driver(uri, auth=(user, pwd), connection_timeout=10)
    except Exception as e:
        print(f"  no se pudo crear el driver: {type(e).__name__}: {str(e)[:200]}")
        continue
    try:
        for db in (None, "neo4j", inst):
            label = db or "(por defecto)"
            try:
                with driver.session(database=db) as session:  # sin reintentos: respuesta rápida
                    real = session.run("CALL db.info() YIELD name RETURN name").single()["name"]
                print(f"  base {label:<14} -> OK  (nombre real: {real})", flush=True)
                ok.append((scheme, db, real))
            except Exception as e:
                msg = getattr(e, "message", None) or str(e)
                print(f"  base {label:<14} -> FALLA  {type(e).__name__}: {msg[:160]}", flush=True)
    finally:
        driver.close()
    print()

print("=== Resultado ===")
if ok:
    scheme, db, real = ok[0]
    print("Pon esto en tu .env:")
    print(f"  NEO4J_URI={scheme}://{inst}.databases.neo4j.io")
    print(f"  NEO4J_DATABASE={real}")
else:
    print("Ninguna combinación funcionó. Revisa en console.neo4j.io que la instancia diga")
    print("Running, y que usuario y contraseña sean los del archivo descargado.")

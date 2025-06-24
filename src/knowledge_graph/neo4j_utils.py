"""Utility to store triples in Neo4j."""
from neo4j import GraphDatabase


def save_triples_to_neo4j(triples, config):
    """Save triples to Neo4j.

    Args:
        triples: List of triple dicts with 'subject', 'predicate', 'object'.
        config: Dict with keys 'uri', 'user', 'password'.
    """
    uri = config.get("uri")
    user = config.get("user")
    password = config.get("password")
    if not uri or not user or not password:
        print("Neo4j configuration incomplete; skipping save")
        return

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        with driver.session() as session:
            for triple in triples:
                subject = triple.get("subject")
                predicate = str(triple.get("predicate", "")).replace("`", "")
                obj = triple.get("object")
                if not subject or not predicate or not obj:
                    continue
                cypher = (
                    "MERGE (a:Entity {name: $subject}) "
                    "MERGE (b:Entity {name: $object}) "
                    "MERGE (a)-[:`" + predicate + "`]->(b)"
                )
                session.run(cypher, subject=subject, object=obj)
        print("Saved triples to Neo4j")
    except Exception as exc:  # pragma: no cover - connection errors
        print(f"Error saving to Neo4j: {exc}")
    finally:
        driver.close()

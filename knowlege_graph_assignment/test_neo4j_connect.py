import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env
project_root = Path(__file__).parent
env_path = project_root / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    print('No .env file found')

# Import settings
from config.settings import settings

print('NEO4J_URI:', settings.neo4j_uri)
print('Username:', settings.neo4j_username)
print('Password set?', bool(settings.neo4j_password))

# Test connection
try:
    from neo4j import GraphDatabase
    driver = GraphDatabase.driver(settings.neo4j_uri, auth=(settings.neo4j_username, settings.neo4j_password))
    with driver.session() as session:
        result = session.run("RETURN 1 AS test")
        record = result.single()
        print('Connection successful, test result:', record['test'])
except Exception as e:
    print('Connection failed:', e)

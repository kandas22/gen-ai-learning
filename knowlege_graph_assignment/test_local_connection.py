from database.neo4j_graph_store import Neo4jGraphStore
from config import settings
import sys

def test_connection():
    print(f"Testing connection to: {settings.neo4j_uri}")
    try:
        store = Neo4jGraphStore()
        with store.driver.session() as session:
            result = session.run("RETURN 1 as val")
            record = result.single()
            print(f"✅ Connection successful! Value: {record['val']}")
            
            # Check if APOC is installed (optional but good to know)
            try:
                result = session.run("RETURN apoc.version() as version")
                record = result.single()
                if record:
                    print(f"✅ APOC version: {record['version']}")
            except Exception:
                print("⚠️ APOC not detected or not accessible")
                
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        sys.exit(1)
    finally:
        if 'store' in locals():
            store.close()

if __name__ == "__main__":
    test_connection()

from database.neo4j_graph_store import Neo4jGraphStore
import sys

def check_data():
    print("Checking Neo4j data...")
    try:
        store = Neo4jGraphStore()
        with store.driver.session() as session:
            # Count Entity nodes
            result = session.run("MATCH (n:Entity) RETURN count(n) as count")
            entity_count = result.single()['count']
            print(f"Entity Nodes: {entity_count}")
            
            # Count RELATES_TO relationships
            result = session.run("MATCH ()-[r:RELATES_TO]->() RETURN count(r) as count")
            rel_count = result.single()['count']
            print(f"RELATES_TO Relationships: {rel_count}")
            
            if entity_count > 0:
                print("✅ Entities exist.")
            else:
                print("⚠️ No Entity nodes found. Entity extraction might have failed or skipped.")
                
    except Exception as e:
        print(f"❌ Failed to check data: {e}")
    finally:
        if 'store' in locals():
            store.close()

if __name__ == "__main__":
    check_data()

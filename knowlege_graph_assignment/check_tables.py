import os
import psycopg2
from config import settings
from dotenv import load_dotenv

load_dotenv()

def check_tables():
    print(f"Connecting to: {settings.neon_db_uri}")
    try:
        conn = psycopg2.connect(settings.neon_db_uri)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public';
        """)
        
        tables = cursor.fetchall()
        print("\nTables found in database:")
        for table in tables:
            print(f"- {table[0]}")
            
        # Check specifically for documents table
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'documents'
            );
        """)
        exists = cursor.fetchone()[0]
        print(f"\n'documents' table exists: {exists}")
        
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_tables()

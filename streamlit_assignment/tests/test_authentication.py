"""
Test script to verify the authentication system
"""

import sqlite3
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from database import (
    get_connection,
    init_db,
    init_users_table,
    authenticate_user,
    create_user,
    fetch_all_users,
    delete_user,
    user_exists
)

def test_auth_system():
    """Test the authentication system"""
    print("🧪 Testing Authentication System\n")
    
    # Use a test database
    test_db = "test_auth.db"
    
    # Clean up if exists
    if os.path.exists(test_db):
        os.remove(test_db)
    
    conn = get_connection(test_db)
    
    try:
        # Test 1: Initialize tables
        print("1️⃣ Testing table initialization...")
        init_db(conn)
        init_users_table(conn)
        print("   ✅ Tables initialized successfully\n")
        
        # Test 2: Check admin user exists
        print("2️⃣ Testing admin user creation...")
        admin = authenticate_user(conn, "admin", "admin")
        assert admin is not None, "Admin user not found"
        assert admin["username"] == "admin", "Admin username incorrect"
        assert admin["role"] == "admin", "Admin role incorrect"
        print(f"   ✅ Admin user exists: {admin['username']} (role: {admin['role']})\n")
        
        # Test 3: Create a new user
        print("3️⃣ Testing user creation...")
        user_id = create_user(conn, "testuser", "testpass", "admin")
        assert user_id > 0, "User creation failed"
        print(f"   ✅ User created with ID: {user_id}\n")
        
        # Test 4: Check username exists
        print("4️⃣ Testing username existence check...")
        assert user_exists(conn, "testuser"), "User should exist"
        assert not user_exists(conn, "nonexistent"), "Non-existent user should not exist"
        print("   ✅ Username existence check works\n")
        
        # Test 5: Authenticate new user
        print("5️⃣ Testing user authentication...")
        user = authenticate_user(conn, "testuser", "testpass")
        assert user is not None, "User authentication failed"
        assert user["username"] == "testuser", "Username incorrect"
        assert user["role"] == "user", "User role should be 'user'"
        print(f"   ✅ User authenticated: {user['username']} (role: {user['role']})\n")
        
        # Test 6: Test wrong password
        print("6️⃣ Testing wrong password...")
        wrong_auth = authenticate_user(conn, "testuser", "wrongpass")
        assert wrong_auth is None, "Authentication should fail with wrong password"
        print("   ✅ Wrong password correctly rejected\n")
        
        # Test 7: Fetch all users
        print("7️⃣ Testing fetch all users...")
        users_df = fetch_all_users(conn)
        assert len(users_df) == 2, "Should have 2 users (admin + testuser)"
        print(f"   ✅ Found {len(users_df)} users\n")
        print("   Users:")
        for _, row in users_df.iterrows():
            print(f"      - {row['username']} ({row['role']}) created by {row['created_by']}")
        print()
        
        # Test 8: Delete user
        print("8️⃣ Testing user deletion...")
        delete_user(conn, user_id)
        users_df_after = fetch_all_users(conn)
        assert len(users_df_after) == 1, "Should have 1 user after deletion"
        print("   ✅ User deleted successfully\n")
        
        # Test 9: Verify deleted user cannot login
        print("9️⃣ Testing deleted user cannot login...")
        deleted_auth = authenticate_user(conn, "testuser", "testpass")
        assert deleted_auth is None, "Deleted user should not be able to login"
        print("   ✅ Deleted user cannot login\n")
        
        print("=" * 50)
        print("✅ All tests passed!")
        print("=" * 50)
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        conn.close()
        # Clean up test database
        if os.path.exists(test_db):
            os.remove(test_db)
    
    return True

if __name__ == "__main__":
    success = test_auth_system()
    sys.exit(0 if success else 1)

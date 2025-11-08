"""
Test script to verify the lab tests system
"""

import sqlite3
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from database import (
    get_connection,
    init_db,
    init_lab_tests_tables,
    get_all_lab_tests,
    get_lab_tests_by_category,
    order_lab_test,
    fetch_patient_lab_tests,
    fetch_all_lab_tests_orders,
    update_lab_test_result,
    delete_lab_test_order,
    insert_patient
)

def test_lab_tests_system():
    """Test the lab tests system"""
    print("🧪 Testing Lab Tests System\n")
    
    # Use a test database
    test_db = "test_lab_tests.db"
    
    # Clean up if exists
    if os.path.exists(test_db):
        os.remove(test_db)
    
    conn = get_connection(test_db)
    
    try:
        # Test 1: Initialize tables
        print("1️⃣ Testing table initialization...")
        init_db(conn)
        init_lab_tests_tables(conn)
        print("   ✅ Lab tests tables initialized successfully\n")
        
        # Test 2: Check lab tests populated
        print("2️⃣ Testing lab tests list...")
        all_tests = get_all_lab_tests(conn)
        assert len(all_tests) > 0, "No lab tests found"
        print(f"   ✅ Found {len(all_tests)} lab tests\n")
        print(f"   Sample tests: {all_tests[:5]}\n")
        
        # Test 3: Get tests by category
        print("3️⃣ Testing tests by category...")
        tests_by_cat = get_lab_tests_by_category(conn)
        assert len(tests_by_cat) > 0, "No categories found"
        print(f"   ✅ Found {len(tests_by_cat)} categories\n")
        for cat, tests in tests_by_cat.items():
            print(f"   - {cat}: {len(tests)} tests")
        print()
        
        # Test 4: Create a test patient
        print("4️⃣ Creating test patient...")
        patient_id = insert_patient(conn, "John", "Doe", "1234567890", "john@test.com", "123 Test St")
        assert patient_id > 0, "Patient creation failed"
        print(f"   ✅ Patient created with ID: {patient_id}\n")
        
        # Test 5: Order lab tests
        print("5️⃣ Testing lab test ordering...")
        test_date = datetime.now().strftime("%Y-%m-%d")
        
        test_orders = ["CRP Test", "Lipid Profile Test", "HbA1c Test"]
        order_ids = []
        
        for test_name in test_orders:
            order_id = order_lab_test(
                conn,
                patient_id,
                test_name,
                test_date,
                "admin",
                "Routine checkup"
            )
            order_ids.append(order_id)
            print(f"   ✅ Ordered: {test_name} (ID: {order_id})")
        
        print(f"\n   Total orders created: {len(order_ids)}\n")
        
        # Test 6: Fetch patient lab tests
        print("6️⃣ Testing fetch patient lab tests...")
        patient_tests = fetch_patient_lab_tests(conn, patient_id)
        assert len(patient_tests) == len(test_orders), "Patient tests count mismatch"
        print(f"   ✅ Found {len(patient_tests)} tests for patient\n")
        
        # Test 7: Fetch all lab test orders
        print("7️⃣ Testing fetch all lab test orders...")
        all_orders = fetch_all_lab_tests_orders(conn)
        assert len(all_orders) == len(test_orders), "All orders count mismatch"
        print(f"   ✅ Found {len(all_orders)} total orders\n")
        
        # Test 8: Update lab test result
        print("8️⃣ Testing lab test result update...")
        first_order_id = order_ids[0]
        update_lab_test_result(
            conn,
            first_order_id,
            "Completed",
            "5.2",
            "mg/L",
            "0-10 mg/L",
            "Normal range"
        )
        print("   ✅ Test result updated successfully\n")
        
        # Test 9: Verify update
        print("9️⃣ Testing result verification...")
        updated_orders = fetch_all_lab_tests_orders(conn)
        updated_order = updated_orders[updated_orders["id"] == first_order_id].iloc[0]
        assert updated_order["test_status"] == "Completed", "Status not updated"
        assert updated_order["result_value"] == "5.2", "Result value not updated"
        print(f"   ✅ Status: {updated_order['test_status']}")
        print(f"   ✅ Result: {updated_order['result_value']} {updated_order['result_unit']}\n")
        
        # Test 10: Delete lab test order
        print("🔟 Testing lab test order deletion...")
        delete_lab_test_order(conn, order_ids[-1])
        remaining_orders = fetch_all_lab_tests_orders(conn)
        assert len(remaining_orders) == len(order_ids) - 1, "Order not deleted"
        print("   ✅ Order deleted successfully\n")
        
        print("=" * 50)
        print("✅ All lab tests system tests passed!")
        print("=" * 50)
        
        # Print summary
        print("\n📊 Summary:")
        print(f"   - Total lab tests available: {len(all_tests)}")
        print(f"   - Test categories: {len(tests_by_cat)}")
        print(f"   - Test patient ID: {patient_id}")
        print(f"   - Orders created: {len(order_ids)}")
        print(f"   - Orders remaining: {len(remaining_orders)}")
        
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
    success = test_lab_tests_system()
    sys.exit(0 if success else 1)

from data_manager import save_workout, load_data
import os

def test_data_manager():
    print("Testing data manager...")
    
    # Clean up existing file if any
    if os.path.exists("workouts.csv"):
        os.remove("workouts.csv")
        
    # Test saving
    save_workout("Test Exercise", 3, 10, 50.0)
    print("Saved workout.")
    
    # Test loading
    df = load_data()
    print("Loaded data:")
    print(df)
    
    assert not df.empty
    assert df.iloc[0]["Exercise"] == "Test Exercise"
    assert df.iloc[0]["Weight"] == 50.0
    
    print("Verification successful!")

if __name__ == "__main__":
    test_data_manager()

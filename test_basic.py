import os
import database
import pytest

def test_database_init():
    # Setup: delete DB if active
    if os.path.exists("test.db"):
        os.remove("test.db")
    
    # testing if init function crashes
    try:
        database.init_db()
        assert True
    except Exception as e:
        pytest.fail(f"Database init failed: {e}")

def test_upsert():
    try:
        database.upsert_device("2001:db8::TEST", "00:00:00:00:00:00")
        devs = database.get_all_devices()
        found = False
        for d in devs:
            if d['ip'] == "2001:db8::TEST":
                found = True
        assert found
    except Exception as e:
        pytest.fail(f"Upsert failed: {e}")
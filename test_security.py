import requests

BASE_URL = "http://localhost:8000"

def login(username, password):
    session = requests.Session()
    response = session.post(f"{BASE_URL}/login", json={"username": username, "password": password})
    if response.status_code == 200:
        return session
    return None

def test_idor_protection():
    print("Test 1: IDOR Protection - Alice tries to access Bob's file...")
    
    alice_session = login("alice", "alice123")
    if not alice_session:
        print("FAILED: Could not login as alice")
        return False
    
    response = alice_session.get(f"{BASE_URL}/files/2")
    
    if response.status_code == 404:
        print("PASSED: Alice got 404 when accessing Bob's file")
        return True
    else:
        print(f"FAILED: Got status {response.status_code}, expected 404")
        return False

def test_owner_access():
    print("Test 2: Owner Access - Alice accesses her own file...")
    
    alice_session = login("alice", "alice123")
    if not alice_session:
        print("FAILED: Could not login as alice")
        return False
    
    response = alice_session.get(f"{BASE_URL}/files/1")
    
    if response.status_code == 200:
        print("PASSED: Alice can access her own file")
        return True
    else:
        print(f"FAILED: Got status {response.status_code}, expected 200")
        return False

def test_admin_delete():
    print("Test 3: Admin Delete - Admin deletes Bob's file...")
    
    admin_session = login("admin", "admin123")
    if not admin_session:
        print("FAILED: Could not login as admin")
        return False
    
    response = admin_session.delete(f"{BASE_URL}/files/2")
    
    if response.status_code == 200:
        print("PASSED: Admin can delete Bob's file")
        return True
    else:
        print(f"FAILED: Got status {response.status_code}, expected 200")
        return False

def test_my_files():
    print("Test 4: My Files - Alice gets only her files...")
    
    alice_session = login("alice", "alice123")
    if not alice_session:
        print("FAILED: Could not login as alice")
        return False
    
    response = alice_session.get(f"{BASE_URL}/files/my")
    
    if response.status_code == 200:
        files = response.json().get("files", [])
        all_owned = all(f["owner"] == "alice" for f in files)
        if all_owned:
            print(f"PASSED: Alice sees only her {len(files)} files")
            return True
        else:
            print("FAILED: Alice sees files not owned by her")
            return False
    else:
        print(f"FAILED: Got status {response.status_code}")
        return False

if __name__ == "__main__":
    print("Security Tests for File Manager")
    
    tests = [test_idor_protection, test_owner_access, test_admin_delete, test_my_files]
    results = [test() for test in tests]
    
    print("Results")
    passed = sum(results)
    total = len(results)
    print(f"{passed}/{total} tests passed")
    
    if passed == total:
        print("All security tests passed!")
    else:
        print("Some tests failed.")
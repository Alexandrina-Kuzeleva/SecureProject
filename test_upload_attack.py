import requests

BASE_URL = "http://localhost:8000"

def login(username, password):
    session = requests.Session()
    response = session.post(f"{BASE_URL}/login", json={"username": username, "password": password})
    if response.status_code == 200:
        return session
    return None

def test_upload_fake_jpg():
    print("Test: Upload fake.jpg (text file renamed to .jpg)...")
    
    alice_session = login("alice", "alice123")
    if not alice_session:
        print("  FAILED: Could not login as alice")
        return False
    
    with open("fake.jpg", "wb") as f:
        f.write(b"This is not a real JPEG file")
    
    with open("fake.jpg", "rb") as f:
        response = alice_session.post(
            f"{BASE_URL}/files/upload",
            files={"file": ("fake.jpg", f, "image/jpeg")}
        )
    
    if response.status_code == 400:
        print(f"  PASSED: Server rejected fake.jpg: {response.json().get('detail')}")
        return True
    else:
        print(f"  FAILED: Got status {response.status_code}, expected 400")
        return False

if __name__ == "__main__":
    test_upload_fake_jpg()
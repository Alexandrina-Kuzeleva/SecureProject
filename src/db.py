from src.schemas import UserInDB, FileMetadata

users_db = {
    "alice": UserInDB(username="alice", role="user", password="alice123"),
    "bob": UserInDB(username="bob", role="user", password="bob123"),
    "admin": UserInDB(username="admin", role="admin", password="admin123"),
}

files_db = [
    FileMetadata(id=1, filename="report_alice.pdf", owner="alice", size=1024),
    FileMetadata(id=2, filename="photo_bob.jpg", owner="bob", size=2048),
    FileMetadata(id=3, filename="admin_keys.txt", owner="admin", size=512),
    FileMetadata(id=4, filename="alice_notes.txt", owner="alice", size=256),
]

next_file_id = 5
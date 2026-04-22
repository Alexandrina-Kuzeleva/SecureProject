from src.schemas import UserInDB, FileInDB

users_db = {
    "alice": UserInDB(username="alice", role="user", password="alice123"),
    "bob": UserInDB(username="bob", role="user", password="bob123"),
    "admin": UserInDB(username="admin", role="admin", password="admin123"),
}

files_db = [
    FileInDB(
        id=1, 
        filename="report_alice.pdf", 
        owner="alice", 
        size=1024,
        path="storage/alice_report.pdf",
        original_name="report_alice.pdf",
        is_encrypted=False
    ),
    FileInDB(
        id=2, 
        filename="photo_bob.jpg", 
        owner="bob", 
        size=2048,
        path="storage/bob_photo.jpg",
        original_name="photo_bob.jpg",
        is_encrypted=False
    ),
    FileInDB(
        id=3, 
        filename="admin_keys.txt", 
        owner="admin", 
        size=512,
        path="storage/admin_keys.txt",
        original_name="admin_keys.txt",
        is_encrypted=False
    ),
]

next_file_id = 4
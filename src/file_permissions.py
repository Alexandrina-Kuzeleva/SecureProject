from fastapi import Depends, HTTPException
from src.db import files_db
from src.auth import get_current_user

def get_file_secure(file_id: int, current_user: dict = Depends(get_current_user)):
    file = next((f for f in files_db if f.id == file_id), None)
    
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    is_owner = file.owner == current_user["username"]
    is_admin = current_user.get("role") == "admin"
    
    if not (is_owner or is_admin):
        raise HTTPException(status_code=404, detail="File not found")
    
    return file
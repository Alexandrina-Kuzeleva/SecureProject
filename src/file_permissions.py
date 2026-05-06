from fastapi import Depends, HTTPException
from src.db import files_db
from src.auth import get_current_user
from src.logger import get_logger

logger = get_logger("security")

def get_file_secure(file_id: int, current_user: dict = Depends(get_current_user)):
    file = next((f for f in files_db if f.id == file_id), None)
    
    if not file:
        logger.warning(f"User '{current_user['username']}' tried to access non-existent file ID: {file_id}")
        raise HTTPException(status_code=404, detail="File not found")
    
    is_owner = file.owner == current_user["username"]
    is_admin = current_user.get("role") == "admin"
    
    if not (is_owner or is_admin):
        logger.warning(
            f"ACCESS DENIED: User '{current_user['username']}' (role: {current_user.get('role')}) "
            f"tried to access file '{file.filename}' (owner: {file.owner}, id: {file_id})"
        )
        raise HTTPException(status_code=404, detail="File not found")
    
    logger.info(f"User '{current_user['username']}' accessed file '{file.filename}' (id: {file_id})")
    return file
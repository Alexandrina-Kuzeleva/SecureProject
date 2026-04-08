from fastapi import APIRouter, Depends
from src.db import files_db
from src.auth import get_current_user, get_admin_user
from src.file_permissions import get_file_secure

router = APIRouter(prefix="/files", tags=["files"])

@router.get("/my")
def get_my_files(current_user: dict = Depends(get_current_user)):
    user_files = [f for f in files_db if f.owner == current_user["username"]]
    return {"files": [f.model_dump() for f in user_files]}

@router.get("/all")
def get_all_files(admin: dict = Depends(get_admin_user)):
    return {"files": [f.model_dump() for f in files_db]}

@router.get("/{file_id}")
def get_file(file = Depends(get_file_secure)):
    return file.model_dump()

@router.delete("/{file_id}")
def delete_file(file = Depends(get_file_secure), current_user: dict = Depends(get_current_user)):
    files_db.remove(file)
    return {"message": f"File '{file.filename}' deleted successfully"}
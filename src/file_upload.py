import uuid
import os
from fastapi import UploadFile, HTTPException, Depends, Query
from src.db import files_db, next_file_id
from src.auth import get_current_user
from src.encryption import encrypt_data
import filetype

MAX_FILE_SIZE = 2 * 1024 * 1024 
ALLOWED_MIME_TYPES = ["image/jpeg", "image/png"]

async def save_upload_file(
    file: UploadFile, 
    current_user: dict,
    encrypt: bool = False
) -> dict:

    content = await file.read()
    
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413, 
            detail=f"File too large. Max size: {MAX_FILE_SIZE // (1024*1024)}MB"
        )
    
    kind = filetype.guess(content)
    if not kind or kind.mime not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400, 
            detail=f"File type not allowed. Allowed: {', '.join(ALLOWED_MIME_TYPES)}"
        )
    
    file_extension = kind.extension
    uuid_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join("storage", uuid_filename)
    
    if encrypt:
        content_to_save = encrypt_data(content)
    else:
        content_to_save = content
    
    with open(file_path, "wb") as f:
        f.write(content_to_save)
    
    global next_file_id
    from src.schemas import FileInDB
    
    file_obj = FileInDB(
        id=next_file_id,
        filename=uuid_filename,
        owner=current_user["username"],
        size=len(content),
        path=file_path,
        original_name=file.filename,
        is_encrypted=encrypt
    )
    files_db.append(file_obj)
    next_file_id += 1
    
    return {
        "id": file_obj.id,
        "message": "File uploaded successfully",
        "original_name": file_obj.original_name,
        "stored_as": uuid_filename,
        "encrypted": encrypt
    }
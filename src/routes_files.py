import os

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File as FastAPIFile,
    Query,
)
from fastapi.responses import Response
from src.db import files_db
from src.auth import get_current_user, get_admin_user
from src.file_permissions import get_file_secure
from src.file_upload import save_upload_file

router = APIRouter(prefix="/files", tags=["files"])


@router.get("/my")
def get_my_files(current_user: dict = Depends(get_current_user)):
    user_files = [f for f in files_db if f.owner == current_user["username"]]
    return {"files": [f.model_dump() for f in user_files]}


@router.get("/all")
def get_all_files(admin: dict = Depends(get_admin_user)):
    return {"files": [f.model_dump() for f in files_db]}


@router.get("/{file_id}")
def get_file(file=Depends(get_file_secure)):
    return file.model_dump()


@router.delete("/{file_id}")
def delete_file(
    file=Depends(get_file_secure), current_user: dict = Depends(get_current_user)
):
    files_db.remove(file)
    return {"message": f"File '{file.filename}' deleted successfully"}


@router.post("/upload")
async def upload_file(
    file: UploadFile = FastAPIFile(...),
    encrypt: bool = Query(False, description="Шифровать файл на сервере"),
    current_user: dict = Depends(get_current_user),
):
    result = await save_upload_file(file, current_user, encrypt)
    return result


@router.get("/{file_id}/download")
async def download_file(
    file=Depends(get_file_secure), current_user: dict = Depends(get_current_user)
):
    if not os.path.exists(file.path):
        raise HTTPException(status_code=404, detail="File not found on disk")

    with open(file.path, "rb") as f:
        file_content = f.read()

    if file.is_encrypted:
        from src.encryption import decrypt_data

        try:
            file_content = decrypt_data(file_content)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Decryption failed: {str(e)}")

    return Response(
        content=file_content,
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f"attachment; filename*=UTF-8''{file.original_name}"
        },
    )

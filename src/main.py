from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from src.schemas import UserCreate, LoginRequest
from src.db import users_db
from src.routes_files import router as files_router

app = FastAPI(title="Secure File Manager")
app.add_middleware(SessionMiddleware, secret_key="your-super-secret-key-change-this")
app.include_router(files_router)
templates = Jinja2Templates(directory="templates")

@app.post("/registration")
async def register(user: UserCreate):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    from src.schemas import UserInDB
    users_db[user.username] = UserInDB(
        username=user.username,
        role="user", 
        password=user.password  
    )
    
    return {
        "msg": "User created",
        "user": user.username,
        "email": user.email
    }

@app.post("/login")
def login(request: Request, login_data: LoginRequest):
    user = users_db.get(login_data.username)
    if not user or user.password != login_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    request.session["user"] = {"username": user.username, "role": user.role}
    return {"message": "Logged in successfully"}

@app.post("/logout")
def logout(request: Request):
    request.session.clear()
    return {"message": "Logged out"}

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")
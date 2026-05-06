from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import traceback

from src.schemas import UserCreate, LoginRequest
from src.db import users_db
from src.routes_files import router as files_router
from src.logger import get_logger

app = FastAPI(title="Secure File Manager")
logger = get_logger()

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}\n{traceback.format_exc()}")
    return JSONResponse(
        status_code=500,
        content={"detail": "We are sorry, something went wrong."}
    )

app.add_middleware(SessionMiddleware, secret_key="your-super-secret-key-change-this")
app.include_router(files_router)
templates = Jinja2Templates(directory="templates")

@app.post("/registration")
async def register(user: UserCreate):
    if user.username in users_db:
        logger.warning(f"Registration failed: username '{user.username}' already exists")
        raise HTTPException(status_code=400, detail="Username already exists")
    
    from src.schemas import UserInDB
    users_db[user.username] = UserInDB(
        username=user.username,
        role="user", 
        password=user.password  
    )
    
    logger.info(f"New user registered: '{user.username}'")
    return {
        "msg": "User created",
        "user": user.username,
        "email": user.email
    }

@app.post("/login")
def login(request: Request, login_data: LoginRequest):
    logger.info(f"Login attempt for user: {login_data.username}")
    
    user = users_db.get(login_data.username)
    if not user or user.password != login_data.password:
        logger.warning(f"Failed login attempt for user: {login_data.username} - invalid credentials")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    request.session["user"] = {"username": user.username, "role": user.role}
    logger.info(f"User '{user.username}' logged in successfully (role: {user.role})")
    return {"message": "Logged in successfully"}

@app.post("/logout")
def logout(request: Request):
    username = request.session.get("user", {}).get("username", "unknown")
    logger.info(f"User '{username}' logged out")
    request.session.clear()
    return {"message": "Logged out"}

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

@app.get("/cause_error")
async def cause_error():
    logger.warning("Test error endpoint called")
    1 / 0
    return {"message": "You shouldn't see this"}
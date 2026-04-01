from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

comments = []

@app.middleware("http")
async def add_csp_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self'; "
        "img-src 'self' data:;"
    )
    return response

@app.get("/comments")
def get_comments(request: Request):
    return templates.TemplateResponse("comments_csp.html", {
        "request": request,
        "comments": comments
    })

@app.post("/comments")
def post_comment(comment: str = Form(...)):
    comments.append(comment)
    return RedirectResponse(url="/comments", status_code=303)
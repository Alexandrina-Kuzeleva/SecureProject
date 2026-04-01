from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import bleach

app = FastAPI()
templates = Jinja2Templates(directory="templates")

comments = []

ALLOWED_TAGS = ['b', 'i', 'u', 'em', 'strong']

def sanitize(text: str) -> str:
    return bleach.clean(
        text,
        tags=ALLOWED_TAGS,
        attributes={},  
        strip=True  
    )

@app.get("/comments")
def get_comments(request: Request):
    return templates.TemplateResponse("comments.html", {
        "request": request,
        "comments": comments
    })

@app.post("/comments")
def post_comment(comment: str = Form(...)):
    clean_comment = sanitize(comment)
    comments.append(clean_comment)
    return RedirectResponse(url="/comments", status_code=303)
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

comments = []


@app.get("/comments")
def get_comments(request: Request):
    return templates.TemplateResponse(
        "comments.html", {"request": request, "comments": comments}
    )


@app.post("/comments")
def post_comment(comment: str = Form(...)):
    comments.append(comment)
    return RedirectResponse(url="/comments", status_code=303)

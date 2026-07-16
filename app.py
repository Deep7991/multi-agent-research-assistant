from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from graph import graph

app = FastAPI(title="Multi-Agent Research Assistant")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.post("/generate")
async def generate(data: dict):

    topic = data["topic"]

    initial_state = {
        "topic": topic,
        "research_notes": "",
        "report": "",
        "feedback": "",
        "score": 0,
        "approved": False,
        "revision_count": 0
    }

    result = graph.invoke(initial_state)

    return {
        "topic": topic,
        "score": result["score"],
        "iterations": result["revision_count"],
        "approved": result["approved"],
        "report": result["report"],
        "feedback": result["feedback"]
    }
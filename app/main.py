from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks


with open("README.md", "r") as file:
    next(file)
    description = file.read()

VERSION = "0.0.1"
API = FastAPI(
    title='Classroom Toolkit API',
    description=description,
    version=VERSION,
    docs_url='/',
)
API.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@API.get("/version", tags=["General"])
async def version():
    """<h3>Version</h3>
    Returns the current version of the API
    <pre><code>
    @return: String </code></pre>"""
    return VERSION
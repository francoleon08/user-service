from fastapi import FastAPI
from .controller import routes

app = FastAPI()
app.include_router(routes.app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/users/")
def root():
    return [{"Hello": "Register"}]




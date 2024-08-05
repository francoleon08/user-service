from fastapi import FastAPI
from .controller import routes

app = FastAPI()
app.include_router(routes.app)


@app.get("/users/")
def root():
    return [{"Hello": "Register"}]




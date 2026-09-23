from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from tasks.routes import router as tasks_routs
from users.models import UserModel
from users.routes import router as users_routs
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from auth.basic_auth import get_current_username

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}

@asynccontextmanager
async def lifespan(app: FastAPI) :
    print("app started")
    yield
    print("app stoped")


app = FastAPI(lifespan = lifespan)
security = HTTPBasic()
app.include_router(tasks_routs)
app.include_router(users_routs)

@app.get("/public")
def public_route():
    return {"message": "this is public route"}

@app.get("/private")
def private_route(user:UserModel = Depends(get_current_username)):
    print(user)
    return {"message": "this is private route"}

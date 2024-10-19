from fastapi import FastAPI
from app.routers import users, logs, auth

app = FastAPI()

# Регистрируем маршруты
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(logs.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI backend for project management"}

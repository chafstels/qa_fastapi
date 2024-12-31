from fastapi import FastAPI
from app.routers import users, logs, auth
import uvicorn

app = FastAPI()

# Регистрируем маршруты
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(logs.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI backend for project management"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
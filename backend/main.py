from fastapi import FastAPI
from database.database import engine, Base
from backend.api import routes

# This automatically creates your database tables!
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student KPI Agent API")

# Connects the API routes we just made
app.include_router(routes.router)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "KPI Agent API is running!"}
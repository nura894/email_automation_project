# app/main.py
from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.router import auth, main2


app = FastAPI(title= "email_automation")

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(main2.router)


@app.get("/")
def root():
    return {"status": "API running"}

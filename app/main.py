# app/main.py
from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.router import auth, main2
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title= "Email Automation Api")

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(main2.router)


@app.get("/")
def root():
    return {"status": "API running"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
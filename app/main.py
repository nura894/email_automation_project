# app/main.py
from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.router import auth, main2
from fastapi.middleware.cors import CORSMiddleware


<<<<<<< HEAD
app = FastAPI(title= "Email Automation Api")
=======
app = FastAPI(title= "email_automation")
>>>>>>> 84ab6db0abce1883026372f0f3cb1ee1b5810669

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
from fastapi import FastAPI
from core.database import engine
from models.users import  Base
from routes.register import router as register_router
from routes.login import router as login_router
from routes.translate import router as translate_router
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Secure Translation Platform API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





@app.get("/")
def read_root():
    return {"message": "Welcome to the Secure Translation Platform API"}


app.include_router(register_router)
app.include_router(login_router)
app.include_router(translate_router)
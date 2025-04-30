from fastapi import FastAPI
from routers import users
from routers import auth
from dotenv import load_dotenv
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

load_dotenv()

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)


@app.get("/hc")
def read_root():
    return True


# inicie com "uvicorn main:app --reload"

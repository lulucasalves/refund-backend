from fastapi import FastAPI
from routers import auth, currency
from dotenv import load_dotenv
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

load_dotenv()

app = FastAPI()

app.include_router(auth.router)
app.include_router(currency.router)


@app.get("/hc")
def read_root():
    return True


# inicie com "uvicorn main:app --reload"
# gerar requirements "pip freeze > requirements.txt"

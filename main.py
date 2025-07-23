import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))
from fastapi import FastAPI
from routes.routes import router

app = FastAPI()

app.include_router(router)

print("Wave Model API is running on port 8000")

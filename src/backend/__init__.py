import uvicorn
from dotenv import load_dotenv
import os

load_dotenv()

PORT = int(os.getenv("PORT"))

def main() -> None:
    print("Hello from backend!")
    uvicorn.run(app="app:app", host="0.0.0.0", port=PORT, reload=True)
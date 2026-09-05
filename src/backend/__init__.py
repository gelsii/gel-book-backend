import uvicorn

def main() -> None:
    print("Hello from backend!")
    uvicorn.run(app="app:app", host="0.0.0.0", port=8080, reload=True)
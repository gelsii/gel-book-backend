from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.auth import auth_router
from routes.posts import posts_router
from routes.profile_user import profile_router
from routes.global_chat import chat_router


app = FastAPI()

origin_cors = [
    "http://localhost",
    "http://localhost:5173",
    "https://gel-book-frontend.onrender.com"
]

app.add_middleware(CORSMiddleware, allow_origins=origin_cors, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(router=auth_router)
app.include_router(router=posts_router)
app.include_router(router=profile_router)
app.include_router(router=chat_router)

@app.get('/api/users')
def get_all_users():
    return { "users": "Hiiii"}



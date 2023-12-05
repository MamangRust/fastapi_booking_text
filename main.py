import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router.auth_router import auth_router
from router.user_router import user_router
from router.book_router import book_router
from router.booking_router import booking_router


app = FastAPI()


origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def hello():
    return "Hello"


app.include_router(auth_router, prefix="/api")
app.include_router(user_router, prefix="/api")
app.include_router(book_router, prefix="/api")
app.include_router(booking_router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)

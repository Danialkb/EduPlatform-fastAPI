import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from users.routers import router as user_router
from courses.routers import router as course_router
from course_modules.routers import router as course_module_router
from lessons.routers import router as lesson_router

app = FastAPI(
    title="edu-platform"
)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def home():
    return {"message": "Hello from FastAPI"}

app.include_router(user_router)
app.include_router(course_router)
app.include_router(course_module_router)
app.include_router(lesson_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

import uvicorn
from fastapi import FastAPI

from users.routers import router as user_router
from courses.routers import router as course_router

app = FastAPI(
    title="edu-platform"
)

app.include_router(user_router)
app.include_router(course_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

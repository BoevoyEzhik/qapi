import uvicorn
from fastapi import FastAPI

from app.api.answer import answer_router
from app.api.question import questions_router
from app.logging_config import setup_logging

setup_logging()

app = FastAPI()
app.include_router(answer_router)
app.include_router(questions_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_config=None)

import uuid
from datetime import datetime

from pydantic import BaseModel, field_validator


class AnswerBase(BaseModel):
    text: str
    user_id: uuid.UUID


class AnswerCreate(AnswerBase):
    @field_validator("text")
    @classmethod
    def text_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Text must not be empty or whitespace")
        return v.strip()

    @field_validator("user_id")
    @classmethod
    def user_id_must_not_be_empty(cls, v):
        if not v:
            raise ValueError("User_id required")
        return v


class AnswerResponse(AnswerBase):
    id: int
    created_at: datetime
    question_id: int

    model_config = {"from_attributes": True}

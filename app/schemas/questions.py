from datetime import datetime

from pydantic import BaseModel, field_validator


class QuestionBase(BaseModel):
    text: str


class QuestionCreate(QuestionBase):
    @field_validator("text")
    @classmethod
    def text_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Text must not be empty or whitespace")
        return v.strip()


class QuestionResponse(QuestionBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}

import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Answer(Base):
    __tablename__ = "answers"

    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id", ondelete="CASCADE")
    )
    user_id: Mapped[uuid.UUID] = mapped_column()
    text: Mapped[str] = mapped_column()
    question: Mapped["Question"] = relationship(  # noqa F821
        "Question", back_populates="answers"
    )

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Question(Base):
    __tablename__ = "questions"

    text: Mapped[str] = mapped_column()
    answers: Mapped[list["Answer"]] = relationship(  # noqa F821
        "Answer",
        back_populates="question",
        lazy="select",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

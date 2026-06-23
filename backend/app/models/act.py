from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class ACTScore(Base):
    __tablename__ = "act_scores"

    __table_args__ = (
        UniqueConstraint("student_id", "test_date", name="uq_act_student_date"),
    )

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)

    test_date = Column(Date, nullable=False)
    test_type = Column(String(32), nullable=False, default="ACT")  # "ACT" | "ACT School Day"
    registration_number = Column(String(32), nullable=True)

    english_score = Column(Integer, nullable=True)
    math_score = Column(Integer, nullable=True)
    reading_score = Column(Integer, nullable=True)
    science_score = Column(Integer, nullable=True)
    composite_score = Column(Integer, nullable=True)
    writing_score = Column(Integer, nullable=True)
    ela_score = Column(Integer, nullable=True)
    stem_score = Column(Integer, nullable=True)

    english_percentile = Column(Integer, nullable=True)
    math_percentile = Column(Integer, nullable=True)
    reading_percentile = Column(Integer, nullable=True)
    science_percentile = Column(Integer, nullable=True)
    composite_percentile = Column(Integer, nullable=True)

    source_file = Column(String(255), nullable=True)
    imported_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    student = relationship("Student", back_populates="act_scores")

    def __repr__(self) -> str:
        return f"<ACTScore student_id={self.student_id} date={self.test_date} composite={self.composite_score}>"
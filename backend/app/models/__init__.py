from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class DIBELSScore(Base):
    __tablename__ = "dibels_scores"

    __table_args__ = (
        UniqueConstraint(
            "student_id", "term_name", "measure", "test_date",
            name="uq_dibels_student_term_measure_date",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)

    test_date = Column(Date, nullable=False)
    term_name = Column(String(64), nullable=False)
    season = Column(String(16), nullable=True)
    school_year = Column(String(16), nullable=True)

    measure = Column(String(16), nullable=False)
    edition = Column(String(16), nullable=False, default="DIBELS 8")

    score = Column(Integer, nullable=True)
    accuracy = Column(Integer, nullable=True)
    benchmark_status = Column(String(32), nullable=True)
    percentile = Column(Integer, nullable=True)
    grade_at_testing = Column(Integer, nullable=True)

    source_file = Column(String(255), nullable=True)
    imported_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    student = relationship("Student", back_populates="dibels_scores")

    def __repr__(self) -> str:
        return f"<DIBELSScore student_id={self.student_id} measure={self.measure} term={self.term_name} score={self.score}>"
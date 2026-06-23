from sqlalchemy import Column, Integer, String, Date, DateTime, Numeric, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class MAPScore(Base):
    __tablename__ = "map_scores"
    __table_args__ = (UniqueConstraint("student_id", "term_name", "subject", "test_date", name="uq_map_student_term_subject_date"),)
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    test_date = Column(Date, nullable=False)
    term_name = Column(String(64), nullable=False)
    season = Column(String(16), nullable=True)
    school_year = Column(String(16), nullable=True)
    subject = Column(String(64), nullable=False)
    rit_score = Column(Numeric(6, 1), nullable=True)
    percentile = Column(Integer, nullable=True)
    standard_error = Column(Numeric(4, 1), nullable=True)
    lexile_low = Column(Integer, nullable=True)
    lexile_high = Column(Integer, nullable=True)
    quantile_low = Column(Integer, nullable=True)
    quantile_high = Column(Integer, nullable=True)
    norm_rit_mean = Column(Numeric(6, 1), nullable=True)
    norm_percentile = Column(Integer, nullable=True)
    growth_rit = Column(Numeric(5, 1), nullable=True)
    projected_growth = Column(Numeric(5, 1), nullable=True)
    met_projected_growth = Column(String(8), nullable=True)
    grade_at_testing = Column(Integer, nullable=True)
    source_file = Column(String(255), nullable=True)
    imported_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    student = relationship("Student", back_populates="map_scores")

from sqlalchemy import Column, Integer, String, Date, DateTime, Numeric, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class CanvasCourse(Base):
    __tablename__ = "canvas_courses"
    id = Column(Integer, primary_key=True, index=True)
    canvas_course_id = Column(Integer, unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    course_code = Column(String(64), nullable=True)
    sis_course_id = Column(String(128), nullable=True, index=True)
    term_name = Column(String(64), nullable=True)
    school_year = Column(String(16), nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    workflow_state = Column(String(32), nullable=True)
    synced_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    enrollments = relationship("CanvasEnrollment", back_populates="course", cascade="all, delete-orphan")

class CanvasEnrollment(Base):
    __tablename__ = "canvas_enrollments"
    __table_args__ = (UniqueConstraint("student_id", "canvas_course_id", name="uq_enrollment_student_course"),)
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    canvas_course_id = Column(Integer, ForeignKey("canvas_courses.canvas_course_id", ondelete="CASCADE"), nullable=False, index=True)
    canvas_enrollment_id = Column(Integer, unique=True, index=True, nullable=True)
    enrollment_type = Column(String(32), nullable=False, default="StudentEnrollment")
    current_grade = Column(String(4), nullable=True)
    current_score = Column(Numeric(5, 2), nullable=True)
    final_grade = Column(String(4), nullable=True)
    final_score = Column(Numeric(5, 2), nullable=True)
    enrollment_state = Column(String(16), nullable=True)
    synced_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    student = relationship("Student", back_populates="canvas_enrollments")
    course = relationship("CanvasCourse", back_populates="enrollments")

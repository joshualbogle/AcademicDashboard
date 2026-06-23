from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from datetime import datetime, date
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel

from app.core.permissions import require_any_group
from app.core.roles import Groups
from app.database import get_db
from app.models.canvas import CanvasCourse, CanvasEnrollment

router = APIRouter()

_readers = [Groups.ADMINS, Groups.COUNSELORS, Groups.HS, Groups.MS, Groups.LS]


# ---------------------------------------------------------------------------
# Schemas (inline — small enough not to warrant a separate file yet)
# ---------------------------------------------------------------------------

class CanvasCourseRead(BaseModel):
    id: int
    canvas_course_id: int
    name: str
    course_code: Optional[str] = None
    sis_course_id: Optional[str] = None
    term_name: Optional[str] = None
    school_year: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    workflow_state: Optional[str] = None
    synced_at: datetime

    model_config = {"from_attributes": True}


class CanvasEnrollmentRead(BaseModel):
    id: int
    student_id: int
    canvas_course_id: int
    enrollment_type: str
    current_grade: Optional[str] = None
    current_score: Optional[Decimal] = None
    final_grade: Optional[str] = None
    final_score: Optional[Decimal] = None
    enrollment_state: Optional[str] = None
    synced_at: datetime

    model_config = {"from_attributes": True}


class StudentCourseRead(CanvasEnrollmentRead):
    course_name: str
    course_code: Optional[str] = None
    term_name: Optional[str] = None
    school_year: Optional[str] = None

    model_config = {"from_attributes": False}


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/courses", response_model=list[CanvasCourseRead])
def list_courses(
    school_year: Optional[str] = Query(None, description="e.g. 2024-2025"),
    active_only: bool = Query(False),
    db: Session = Depends(get_db),
    current_user=Depends(require_any_group(_readers)),
):
    q = db.query(CanvasCourse)
    if school_year:
        q = q.filter(CanvasCourse.school_year == school_year)
    if active_only:
        q = q.filter(CanvasCourse.workflow_state == "available")
    return q.order_by(CanvasCourse.name).all()


@router.get("/courses/{canvas_course_id}", response_model=CanvasCourseRead)
def get_course(
    canvas_course_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_any_group(_readers)),
):
    course = db.query(CanvasCourse).filter(CanvasCourse.canvas_course_id == canvas_course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return course


@router.get("/students/{student_id}/courses", response_model=list[StudentCourseRead])
def get_student_courses(
    student_id: int,
    school_year: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(require_any_group(_readers)),
):
    """All Canvas courses a student is enrolled in, with current grades."""
    q = (
        db.query(CanvasEnrollment, CanvasCourse)
        .join(CanvasCourse, CanvasEnrollment.canvas_course_id == CanvasCourse.canvas_course_id)
        .filter(CanvasEnrollment.student_id == student_id)
        .filter(CanvasEnrollment.enrollment_type == "StudentEnrollment")
    )
    if school_year:
        q = q.filter(CanvasCourse.school_year == school_year)

    results = []
    for enrollment, course in q.order_by(CanvasCourse.name).all():
        results.append(StudentCourseRead(
            id=enrollment.id,
            student_id=enrollment.student_id,
            canvas_course_id=enrollment.canvas_course_id,
            enrollment_type=enrollment.enrollment_type,
            current_grade=enrollment.current_grade,
            current_score=enrollment.current_score,
            final_grade=enrollment.final_grade,
            final_score=enrollment.final_score,
            enrollment_state=enrollment.enrollment_state,
            synced_at=enrollment.synced_at,
            course_name=course.name,
            course_code=course.course_code,
            term_name=course.term_name,
            school_year=course.school_year,
        ))
    return results

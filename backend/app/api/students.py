from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.permissions import require_any_group
from app.core.roles import Groups
from app.database import get_db
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentRead, StudentSummary, StudentUpdate

router = APIRouter()

# Any authenticated school-division staff can read students.
_readers = [Groups.ADMINS, Groups.COUNSELORS, Groups.HS, Groups.MS, Groups.LS]
_writers = [Groups.ADMINS, Groups.COUNSELORS]


@router.get("/", response_model=list[StudentSummary])
def list_students(
    division: Optional[str] = Query(None, description="Filter by division: LS, MS, HS"),
    grade: Optional[int] = Query(None, description="Filter by grade level"),
    active_only: bool = Query(True, description="Return only active students"),
    search: Optional[str] = Query(None, description="Search by name or student ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user=Depends(require_any_group(_readers)),
):
    q = db.query(Student)

    if active_only:
        q = q.filter(Student.is_active == True)  # noqa: E712
    if division:
        q = q.filter(Student.division == division.upper())
    if grade is not None:
        q = q.filter(Student.grade == grade)
    if search:
        term = f"%{search}%"
        q = q.filter(
            Student.first_name.ilike(term)
            | Student.last_name.ilike(term)
            | Student.preferred_name.ilike(term)
            | Student.student_id.ilike(term)
        )

    q = q.order_by(Student.last_name, Student.first_name)
    return q.offset(skip).limit(limit).all()


@router.get("/{student_id}", response_model=StudentRead)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_any_group(_readers)),
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student


@router.post("/", response_model=StudentRead, status_code=status.HTTP_201_CREATED)
def create_student(
    payload: StudentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_any_group(_writers)),
):
    existing = db.query(Student).filter(Student.student_id == payload.student_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Student with ID {payload.student_id} already exists",
        )

    student = Student(**payload.model_dump())
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


@router.patch("/{student_id}", response_model=StudentRead)
def update_student(
    student_id: int,
    payload: StudentUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_any_group(_writers)),
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(student, field, value)

    db.commit()
    db.refresh(student)
    return student


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def deactivate_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_any_group([Groups.ADMINS])),
):
    """Soft-delete: sets is_active=False rather than deleting the row."""
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    student.is_active = False
    db.commit()
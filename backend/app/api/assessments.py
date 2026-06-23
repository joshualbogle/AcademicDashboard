from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.permissions import require_any_group
from app.core.roles import Groups
from app.database import get_db
from app.models.student import Student
from app.models.sat import SATScore
from app.models.psat import PSATScore
from app.models.act import ACTScore
from app.models.map import MAPScore
from app.models.dibels import DIBELSScore
from app.schemas.assessment import (
    SATScoreRead,
    PSATScoreRead,
    ACTScoreRead,
    MAPScoreRead,
    DIBELSScoreRead,
    StudentAssessmentsRead,
)

router = APIRouter()

_readers = [Groups.ADMINS, Groups.COUNSELORS, Groups.HS, Groups.MS, Groups.LS]


def _get_student_or_404(student_id: int, db: Session) -> Student:
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student


# ---------------------------------------------------------------------------
# Aggregate endpoint — all assessment types for one student
# ---------------------------------------------------------------------------

@router.get("/students/{student_id}", response_model=StudentAssessmentsRead)
def get_student_assessments(
    student_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_any_group(_readers)),
):
    """Return all assessment scores for a single student."""
    _get_student_or_404(student_id, db)

    return StudentAssessmentsRead(
        student_id=student_id,
        sat=db.query(SATScore).filter(SATScore.student_id == student_id).order_by(SATScore.test_date).all(),
        psat=db.query(PSATScore).filter(PSATScore.student_id == student_id).order_by(PSATScore.test_date).all(),
        act=db.query(ACTScore).filter(ACTScore.student_id == student_id).order_by(ACTScore.test_date).all(),
        map=db.query(MAPScore).filter(MAPScore.student_id == student_id).order_by(MAPScore.test_date).all(),
        dibels=db.query(DIBELSScore).filter(DIBELSScore.student_id == student_id).order_by(DIBELSScore.test_date).all(),
    )


# ---------------------------------------------------------------------------
# Per-type list endpoints (school-wide, filterable by student)
# ---------------------------------------------------------------------------

@router.get("/sat", response_model=list[SATScoreRead])
def list_sat_scores(
    student_id: int | None = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(require_any_group(_readers)),
):
    q = db.query(SATScore)
    if student_id:
        q = q.filter(SATScore.student_id == student_id)
    return q.order_by(SATScore.test_date.desc()).all()


@router.get("/psat", response_model=list[PSATScoreRead])
def list_psat_scores(
    student_id: int | None = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(require_any_group(_readers)),
):
    q = db.query(PSATScore)
    if student_id:
        q = q.filter(PSATScore.student_id == student_id)
    return q.order_by(PSATScore.test_date.desc()).all()


@router.get("/act", response_model=list[ACTScoreRead])
def list_act_scores(
    student_id: int | None = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(require_any_group(_readers)),
):
    q = db.query(ACTScore)
    if student_id:
        q = q.filter(ACTScore.student_id == student_id)
    return q.order_by(ACTScore.test_date.desc()).all()


@router.get("/map", response_model=list[MAPScoreRead])
def list_map_scores(
    student_id: int | None = Query(None),
    subject: str | None = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(require_any_group(_readers)),
):
    q = db.query(MAPScore)
    if student_id:
        q = q.filter(MAPScore.student_id == student_id)
    if subject:
        q = q.filter(MAPScore.subject.ilike(f"%{subject}%"))
    return q.order_by(MAPScore.test_date.desc()).all()


@router.get("/dibels", response_model=list[DIBELSScoreRead])
def list_dibels_scores(
    student_id: int | None = Query(None),
    measure: str | None = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(require_any_group(_readers)),
):
    q = db.query(DIBELSScore)
    if student_id:
        q = q.filter(DIBELSScore.student_id == student_id)
    if measure:
        q = q.filter(DIBELSScore.measure.ilike(f"%{measure}%"))
    return q.order_by(DIBELSScore.test_date.desc()).all()

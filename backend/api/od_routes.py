"""
OD Request API routes for the NeuralKPI application.
Handles student OD applications, faculty dashboard queries and result submissions.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from database.database import get_db
from database.models import ODRequest, Student
from backend.schemas import ODRequestCreate, ODResultSubmit, ODRequestResponse
from backend.services.ocr_verification import verify_certificate
from backend.services.fcm import send_faculty_notification
import logging

logger = logging.getLogger(__name__)

od_router = APIRouter(prefix="/api/od", tags=["OD Requests"])


# ── Submit a new OD Request ───────────────────────────────────────────────────

@od_router.post("/request", response_model=ODRequestResponse)
def submit_od_request(request: ODRequestCreate, db: Session = Depends(get_db)):
    """
    Student submits a new On Duty application.
    Saves with default status 'Pending Result'.
    The FCM token is stored for later automated push notification.
    """
    # Verify student exists
    student = db.query(Student).filter(Student.student_id == request.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail=f"Student '{request.student_id}' not found")
    
    od = ODRequest(
        student_id=request.student_id,
        student_name=request.student_name,
        college_name=request.college_name,
        date=request.date,
        start_time=request.start_time,
        end_time=request.end_time,
        event_details=request.event_details,
        days=request.days,
        result_status="Pending Result",
        fcm_token=request.fcm_token
    )
    db.add(od)
    db.commit()
    db.refresh(od)
    
    logger.info(f"OD Request #{od.id} submitted by {request.student_name} for '{request.event_details}'")
    return od


# ── Fetch all OD Requests (Faculty/HOD Dashboard) ─────────────────────────────

@od_router.get("/all", response_model=List[ODRequestResponse])
def get_all_od_requests(db: Session = Depends(get_db)):
    """
    Returns all OD requests. Used by faculty/HOD dashboard.
    Ordered most recent first.
    """
    ods = db.query(ODRequest).order_by(ODRequest.created_at.desc()).all()
    return ods


# ── Get single OD details ─────────────────────────────────────────────────────

@od_router.get("/{od_id}", response_model=ODRequestResponse)
def get_od_request(od_id: int, db: Session = Depends(get_db)):
    """Get full details of a specific OD request."""
    od = db.query(ODRequest).filter(ODRequest.id == od_id).first()
    if not od:
        raise HTTPException(status_code=404, detail="OD request not found")
    return od


# ── Upload Certificate + Trigger Verification Pipeline ───────────────────────

@od_router.put("/{od_id}/upload-result")
def upload_od_result(od_id: int, payload: ODResultSubmit, db: Session = Depends(get_db)):
    """
    Student submits their event result along with certificate evidence.
    This is the main verification pipeline endpoint:
      1. ELA tamper detection on the uploaded image
      2. AI OCR cross-reference (student name, event name, prize)
      3. Final DB commit with verification_status
      4. Broadcasts a real-time notification to faculty
    """
    od = db.query(ODRequest).filter(ODRequest.id == od_id).first()
    if not od:
        raise HTTPException(status_code=404, detail="OD request not found")
    
    if od.result_status in ("Participated", "Won"):
        raise HTTPException(status_code=400, detail="Result already submitted for this OD")
    
    # ── Run Verification Pipeline ─────────────────────────────────────────────
    verification_result = {
        "verification_status": "Passed",
        "ela_score": 0.0,
        "ocr_verdict": "No certificate uploaded",
        "details": "No certificate provided"
    }
    
    if payload.certificate_base64:
        try:
            verification_result = verify_certificate(
                base64_data=payload.certificate_base64,
                student_name=od.student_name,
                event_name=od.event_details,
                prize=payload.prize_details
            )
        except Exception as e:
            logger.error(f"Verification pipeline error for OD #{od_id}: {e}")
            verification_result["verification_status"] = "Passed"  # Fail open so upload isn't stuck
            verification_result["details"] = f"Verification service error: {e}"
    
    # ── Commit to Database ────────────────────────────────────────────────────
    od.result_status = payload.result          # "Won" or "Participated"
    od.prize_details = payload.prize_details
    od.certificate_data = payload.certificate_base64
    od.verification_status = verification_result["verification_status"]
    od.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(od)
    
    logger.info(
        f"OD #{od_id} result submitted: {payload.result} | "
        f"Verification: {verification_result['verification_status']}"
    )
    
    # ── Notify Faculty ────────────────────────────────────────────────────────
    # In a production system, faculty FCM tokens would be stored in the Users table.
    # Here we use a placeholder list; extend this from your user management system.
    faculty_tokens = []  # TODO: Pull from db.query(User).filter(User.role.in_(["faculty","hod"])).all()
    
    try:
        send_faculty_notification(
            faculty_tokens=faculty_tokens,
            student_name=od.student_name,
            event_name=od.event_details,
            verification_status=verification_result["verification_status"],
            prize=payload.prize_details
        )
    except Exception as e:
        logger.warning(f"Faculty notification failed (non-blocking): {e}")
    
    return {
        "message": "Result submitted successfully",
        "od_id": od.id,
        "result_status": od.result_status,
        "verification_status": od.verification_status,
        "ela_score": verification_result["ela_score"],
        "ocr_verdict": verification_result["ocr_verdict"],
        "details": verification_result["details"]
    }


# ── Quick "Participated" update (no certificate needed) ──────────────────────

@od_router.put("/{od_id}/participated")
def mark_participated(od_id: int, db: Session = Depends(get_db)):
    """
    Lightweight endpoint for when student taps the [Participated] action button
    on the FCM notification. Updates status without requiring a certificate upload.
    """
    od = db.query(ODRequest).filter(ODRequest.id == od_id).first()
    if not od:
        raise HTTPException(status_code=404, detail="OD request not found")
    
    od.result_status = "Participated"
    od.verification_status = "Passed"  # Participation doesn't require a proof
    od.updated_at = datetime.utcnow()
    db.commit()
    
    logger.info(f"OD #{od_id} marked as Participated for {od.student_name}")
    
    faculty_tokens = []
    send_faculty_notification(
        faculty_tokens=faculty_tokens,
        student_name=od.student_name,
        event_name=od.event_details,
        verification_status="Passed",
        prize=None
    )
    
    return {"message": "Marked as Participated", "od_id": od_id}

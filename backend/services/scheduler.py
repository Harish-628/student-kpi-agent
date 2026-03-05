"""
APScheduler background task for the NeuralKPI OD workflow.

Runs a check every 5 minutes to find OD events that ended today.
When the current time passes an OD's end_time, sends an FCM push 
notification to the student asking for their result.

Startup: call `start_scheduler()` from backend/main.py
Shutdown: call `shutdown_scheduler()` on app teardown
"""

import logging
from datetime import datetime, date
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

logger = logging.getLogger(__name__)

_scheduler = None


def _check_od_events():
    """
    Core cron job task.
    Queries for OD requests that:
      - Have date == today
      - Have end_time < current time (24-hour HH:MM)
      - Still have result_status == "Pending Result" (not yet handled)
    
    For each match, fires an FCM push notification and updates status to "Awaiting Proof".
    """
    try:
        # Import here to avoid circular imports on startup
        from database.database import SessionLocal
        from database.models import ODRequest
        from backend.services.fcm import send_od_result_notification
        
        db = SessionLocal()
        today_str = date.today().isoformat()               # "2026-03-04"
        current_time_str = datetime.now().strftime("%H:%M")  # "14:30"
        
        pending = db.query(ODRequest).filter(
            ODRequest.date == today_str,
            ODRequest.end_time <= current_time_str,
            ODRequest.result_status == "Pending Result"
        ).all()
        
        if not pending:
            logger.debug(f"[Scheduler] No completed OD events at {current_time_str}")
            db.close()
            return
        
        logger.info(f"[Scheduler] {len(pending)} OD event(s) just ended. Sending FCM alerts...")
        
        for od in pending:
            success = False
            if od.fcm_token:
                success = send_od_result_notification(
                    fcm_token=od.fcm_token,
                    student_name=od.student_name,
                    event_name=od.event_details,
                    od_id=od.id
                )
            else:
                logger.warning(
                    f"[Scheduler] OD #{od.id} ({od.student_name}) "
                    "has no FCM token registered — notification skipped."
                )
                success = True  # Still mark so we don't re-check endlessly
            
            if success:
                od.result_status = "Awaiting Proof"
                logger.info(f"[Scheduler] OD #{od.id} status -> 'Awaiting Proof'")
        
        db.commit()
        db.close()
    
    except Exception as e:
        logger.error(f"[Scheduler] OD cron job failed: {e}", exc_info=True)


def start_scheduler():
    """
    Start the APScheduler background process.
    Should be called once when the FastAPI application starts up.
    """
    global _scheduler
    
    try:
        from apscheduler.schedulers.background import BackgroundScheduler
        _scheduler = BackgroundScheduler()
        _scheduler.add_job(
            func=_check_od_events,
            trigger=IntervalTrigger(minutes=5),
            id="od_event_checker",
            name="OD Event Completion Checker",
            replace_existing=True
        )
        _scheduler.start()
        logger.info("[Scheduler] OD event checker started — running every 5 minutes.")
    except ImportError:
        logger.warning(
            "APScheduler not installed. OD cron jobs are disabled. "
            "Run: pip install apscheduler"
        )
    except Exception as e:
        logger.error(f"[Scheduler] Failed to start: {e}")


def shutdown_scheduler():
    """Gracefully stop the scheduler on app teardown."""
    global _scheduler
    if _scheduler and _scheduler.running:
        _scheduler.shutdown(wait=False)
        logger.info("[Scheduler] OD event checker stopped.")

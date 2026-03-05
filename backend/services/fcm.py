"""
Firebase Cloud Messaging (FCM) service for NeuralKPI OD workflow.
Sends interactive push notifications to student devices when events end.

Setup:
    1. Create a Firebase project at https://console.firebase.google.com
    2. Download the service account JSON key
    3. Set FIREBASE_CREDENTIALS_PATH in your .env file
"""

import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Attempt to import firebase-admin; gracefully degrade if not installed
try:
    import firebase_admin
    from firebase_admin import credentials, messaging
    _FIREBASE_AVAILABLE = True
except ImportError:
    _FIREBASE_AVAILABLE = False
    logger.warning("firebase-admin not installed. FCM notifications will be logged only. Run: pip install firebase-admin")

_firebase_initialized = False


def _init_firebase():
    """Initialize the Firebase Admin SDK once."""
    global _firebase_initialized
    if _firebase_initialized or not _FIREBASE_AVAILABLE:
        return
    
    cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH", "firebase_credentials.json")
    if not os.path.exists(cred_path):
        logger.warning(f"Firebase credentials file not found at '{cred_path}'. FCM will be simulated.")
        return
    
    try:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        _firebase_initialized = True
        logger.info("Firebase Admin SDK initialized successfully.")
    except Exception as e:
        logger.error(f"Firebase initialization failed: {e}")


def send_od_result_notification(
    fcm_token: str,
    student_name: str,
    event_name: str,
    od_id: int
) -> bool:
    """
    Send an interactive push notification asking the student for their event result.
    
    The notification includes two action buttons: [Won] and [Participated].
    Each button deep-links to the NeuralKPI app with the appropriate action URL.
    
    Args:
        fcm_token: The student's FCM device token
        student_name: Student's name for the notification body
        event_name: Name of the event that just ended
        od_id: The OD request ID for the deep-link parameter
        
    Returns:
        True if the notification was sent (or simulated), False on error
    """
    _init_firebase()
    
    deep_link_won = f"http://localhost:8080/dashboard.html?action=claim_prize&od_id={od_id}"
    deep_link_participated = f"http://localhost:8080/dashboard.html?action=verify_participation&od_id={od_id}&result=Participated"
    
    notification_payload = {
        "title": "🎓 Event Completed!",
        "body": f"Your event '{event_name}' has ended. What was the result?",
        "od_id": str(od_id),
        "deep_link_won": deep_link_won,
        "deep_link_participated": deep_link_participated
    }
    
    # If Firebase is not configured, log the simulated notification
    if not _firebase_initialized or not _FIREBASE_AVAILABLE:
        logger.info(f"[FCM SIMULATED] Would send to token: {fcm_token[:20]}...")
        logger.info(f"[FCM SIMULATED] Payload: {notification_payload}")
        return True
    
    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title=notification_payload["title"],
                body=notification_payload["body"]
            ),
            data={
                "od_id": str(od_id),
                "action": "od_result_request",
                "deep_link_won": deep_link_won,
                "deep_link_participated": deep_link_participated
            },
            android=messaging.AndroidConfig(
                notification=messaging.AndroidNotification(
                    click_action="FLUTTER_NOTIFICATION_CLICK",
                    # Action buttons for Android (requires notification channels setup in the app)
                )
            ),
            token=fcm_token
        )
        response = messaging.send(message)
        logger.info(f"FCM notification sent. Message ID: {response}")
        return True
    except Exception as e:
        logger.error(f"FCM send failed for OD {od_id}: {e}")
        return False


def send_faculty_notification(
    faculty_tokens: list,
    student_name: str,
    event_name: str,
    verification_status: str,
    prize: Optional[str] = None
) -> None:
    """
    Notify all faculty members of a certificate upload with the AI verification status.
    
    Args:
        faculty_tokens: List of FCM tokens for faculty devices
        student_name: The student who uploaded the certificate
        event_name: The OD event
        verification_status: ELA+AI outcome (e.g. "Passed", "Flagged_Image_Altered")
        prize: Prize won, if any
    """
    _init_firebase()
    
    status_emoji = {
        "Passed": "✅",
        "Flagged_Image_Altered": "🚨",
        "Flagged_Text_Mismatch": "⚠️"
    }.get(verification_status, "🔍")
    
    prize_str = f" — {prize}" if prize else ""
    body = (f"{student_name} has uploaded their certificate for '{event_name}'{prize_str}.\n"
            f"{status_emoji} AI Status: {verification_status.replace('_', ' ')}")
    
    if not _firebase_initialized or not _FIREBASE_AVAILABLE:
        logger.info(f"[FCM SIMULATED - Faculty] {body}")
        return
    
    if not faculty_tokens:
        logger.warning("No faculty FCM tokens registered — cannot broadcast.")
        return
    
    try:
        multicast = messaging.MulticastMessage(
            notification=messaging.Notification(
                title="📋 OD Certificate Uploaded",
                body=body
            ),
            data={"verification_status": verification_status},
            tokens=faculty_tokens
        )
        response = messaging.send_each_for_multicast(multicast)
        logger.info(f"Faculty multicast sent: {response.success_count} success, {response.failure_count} failed")
    except Exception as e:
        logger.error(f"Faculty FCM broadcast failed: {e}")

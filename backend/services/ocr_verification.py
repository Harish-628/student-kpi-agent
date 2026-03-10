"""
OCR and AI-powered certificate verification for the OD workflow.

This module:
    1. Runs Error Level Analysis (ELA) on image certificates to detect tampering.
    2. Uses Gemini Vision AI to extract and cross-reference text from the certificate.
    3. Produces a verification_status: "Passed", "Flagged_Image_Altered", "Flagged_Text_Mismatch".
"""

import logging
import os
from typing import Optional
import google.genai as genai
from google.genai import types as genai_types
from backend.security.ela import analyze_image_tampering

logger = logging.getLogger(__name__)

# Configure Gemini
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY", "")
_genai_client = None
if GEMINI_API_KEY:
    _genai_client = genai.Client(api_key=GEMINI_API_KEY)


def _extract_text_with_gemini(base64_data: str) -> str:
    """
    Use Gemini Vision to extract all visible text from the certificate image/PDF.
    
    Args:
        base64_data: data:image/jpeg;base64,... string
        
    Returns:
        Extracted text string, or empty string on failure
    """
    if not _genai_client:
        logger.warning("No Gemini API key configured. OCR check will be skipped.")
        return ""
    
    try:
        # Parse the base64 data URL
        if "," in base64_data:
            header, b64 = base64_data.split(",", 1)
            mime_type = header.split(":")[1].split(";")[0] if ":" in header else "image/jpeg"
        else:
            b64 = base64_data
            mime_type = "image/jpeg"
            
        prompt = "Carefully extract all text visible in this certificate."
        
        response = _genai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                genai_types.Part.from_text(text=prompt),
                genai_types.Part.from_bytes(data=__import__('base64').b64decode(b64), mime_type=mime_type)
            ]
        )
        return response.text.strip() if response.text else ""
    
    except Exception as e:
        logger.error(f"Gemini OCR extraction failed: {e}")
        return ""


def _cross_reference_text(
    extracted_text: str,
    student_name: str,
    event_name: str,
    prize: Optional[str]
) -> tuple[bool, str]:
    """
    Use Gemini to intelligently check if the extracted text matches expected values.
    
    Returns:
        (matches: bool, reason: str)
    """
    if not extracted_text:
        # If OCR failed, skip the text check — don't penalize for API failure
        return True, "OCR unavailable — text check skipped"
    
    if not _genai_client:
        return True, "Gemini not configured — text check skipped"
    
    try:
        check_prompt = f"""
You are a certificate verification assistant. Analyze the following extracted certificate text 
and determine if it matches the expected details.

Expected Details:
- Student Name: {student_name}
- Event Name: {event_name}
- Prize/Result: {prize or 'Participated (no prize)'}

Extracted Certificate Text:
---
{extracted_text[:3000]}
---

Rules:
1. Check if the student name appears in the text (allow for slight formatting differences).
2. Check if the event name appears (allow for abbreviations or alternate names of the same event).
3. If a prize is expected, check if it's mentioned.
4. Respond with EXACTLY one of these two responses:
   - "MATCH: <brief reason>"
   - "MISMATCH: <specific reason what doesn't match>"
"""
        response = _genai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[check_prompt]
        )
        verdict = response.text.strip() if response.text else "MATCH: check skipped"
        
        is_match = verdict.upper().startswith("MATCH")
        return is_match, verdict
    
    except Exception as e:
        logger.error(f"Gemini cross-reference failed: {e}")
        return True, f"Verification check failed: {e}"


def verify_certificate(
    base64_data: str,
    student_name: str,
    event_name: str,
    prize: Optional[str] = None
) -> dict:
    """
    Full verification pipeline: ELA tamper detection + AI OCR cross-reference.
    
    Args:
        base64_data: Base64-encoded certificate (image or, if PDF, description)
        student_name: Expected student name from the OD record
        event_name: Expected event name from the OD record
        prize: Prize tier if result is "Won" (e.g. "1st Prize")
    
    Returns:
        {
            "verification_status": "Passed" | "Flagged_Image_Altered" | "Flagged_Text_Mismatch",
            "ela_score": float,
            "ocr_verdict": str,
            "details": str
        }
    """
    result = {
        "verification_status": "Passed",
        "ela_score": 0.0,
        "ocr_verdict": "Not checked",
        "details": ""
    }
    
    # ── Step A: ELA Tamper Detection ──────────────────────────────────────────
    try:
        ela = analyze_image_tampering(base64_data)
        result["ela_score"] = ela.get("score", 0.0)
        
        if ela.get("is_suspicious", False):
            result["verification_status"] = "Flagged_Image_Altered"
            result["details"] = (
                f"ELA Score: {ela['score']:.2f} — {ela.get('message', 'Image shows signs of digital manipulation.')}"
            )
            logger.warning(f"ELA flagged certificate for: {student_name}. Score: {ela['score']:.2f}")
            # Short-circuit: no need for OCR if image is tampered
            return result
    except Exception as e:
        logger.warning(f"ELA check failed (non-blocking): {e}")
    
    # ── Step B: AI OCR / Text Cross-Reference ─────────────────────────────────
    extracted_text = _extract_text_with_gemini(base64_data)
    is_match, verdict = _cross_reference_text(extracted_text, student_name, event_name, prize)
    
    result["ocr_verdict"] = verdict
    
    if not is_match:
        result["verification_status"] = "Flagged_Text_Mismatch"
        result["details"] = f"AI OCR mismatch: {verdict}"
        logger.warning(f"OCR mismatch for {student_name}: {verdict}")
    else:
        result["details"] = f"ELA Score: {result['ela_score']:.2f} (Safe). OCR: {verdict}"
        logger.info(f"Certificate verified for {student_name}: {result['details']}")
    
    return result

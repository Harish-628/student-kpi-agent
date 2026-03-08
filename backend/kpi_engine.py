"""
KPI Engine for calculating student KPI scores and career readiness predictions.
"""
import os

def calculate_kpi_score(kpi_data):
    """
    Calculates a total KPI score based on 11 categories weighted into a 100-point scale.
    High (10 max): internships, certifications, hackathons, publications, projects, research_papers, patents
    Medium (5 max): workshops, club_activities, industrial_visits, value_added_courses
    
    Args:
        kpi_data (dict): A dictionary containing activity counts.
    
    Returns:
        float: The weighted KPI score (0-100)
    """
    # Define max points available for each category (saturation logic: each is a threshold)
    weights = {
        # High impact categories (10 points each)
        'internships': 10,
        'certifications': 10,
        'hackathons': 10,
        'publications': 10,
        'projects': 10,
        'research_papers': 10,
        'patents': 10,
        # Medium impact categories (5 points each)
        'workshops': 5,
        'club_activities': 5,
        'industrial_visits': 5,
        'value_added_courses': 5
    }
    
    raw_total = 0
    # The max raw score possible is (7 * 10) + (4 * 5) = 90
    max_possible_raw = 90

    # For each category, if the count is > 0, we give the student the full weight
    # This represents a 'checked' box in their academic profile for that achievement type.
    for activity, weight in weights.items():
        count = kpi_data.get(activity, 0)
        if count > 0:
            raw_total += weight
            
    # Normalize to 100-point scale
    normalized_score = (raw_total / max_possible_raw) * 100
    
    return round(normalized_score, 1)


def predict_career_readiness(score):
    """
    Predicts career readiness based on the new 100-point KPI scale.
    """
    if score >= 80:
        return "⭐ Industry Ready"
    elif 60 <= score < 80:
        return "✅ Approaching Ready"
    elif 40 <= score < 60:
        return "📈 Developing"
    else:
        return "⚠️ Needs Support"

# --- Basic Test Suite for verification ---
if __name__ == "__main__":
    test_cases = [
        # Zero case
        ({}, 0.0, "⚠️ Needs Support"),
        # Single high-impact activity
        ({"internships": 1}, 11.1, "⚠️ Needs Support"),
        # Multiple combined
        ({
            "internships": 1,
            "certifications": 3,
            "hackathons": 2,
            "projects": 1
        }, 44.4, "📈 Developing"),
        # High performer
        ({
            "internships": 2,
            "certifications": 5,
            "hackathons": 1,
            "publications": 1,
            "projects": 2,
            "research_papers": 1,
            "patents": 1,
            "workshops": 3,
            "club_activities": 1
        }, 88.9, "⭐ Industry Ready"),
        # Full score
        ({k: 1 for k in [
            'internships', 'certifications', 'hackathons', 'publications', 
            'projects', 'research_papers', 'patents', 'workshops', 
            'club_activities', 'industrial_visits', 'value_added_courses'
        ]}, 100.0, "⭐ Industry Ready")
    ]
    
    print("--- KPI Engine Regression Test ---")
    import sys
    # Set encoding to utf-8 for the test output to handle emojis on Windows
    # (Note: this purely affects the test execution output)
    for i, (data, expected_score, expected_readiness) in enumerate(test_cases, 1):
        actual_score = calculate_kpi_score(data)
        actual_readiness = predict_career_readiness(actual_score)
        
        # Guard against console encoding issues during the test
        try:
            readable_readiness = actual_readiness
            status = "PASSED" if (abs(actual_score - expected_score) < 0.1 and actual_readiness == expected_readiness) else "FAILED"
            print(f"Test {i}: Score={actual_score}, Readiness='{readable_readiness}' -> {status}")
        except UnicodeEncodeError:
            status = "PASSED" if (abs(actual_score - expected_score) < 0.1 and actual_readiness == expected_readiness) else "FAILED"
            print(f"Test {i}: Score={actual_score}, Readiness='[Unicode/Emoji]' -> {status}")

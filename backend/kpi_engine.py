"""
KPI Engine for calculating student KPI scores and career readiness predictions.
"""
import os

def calculate_kpi_score(kpi_data):
    """
    Calculates a total KPI score based on weighted project activities.
    
    Args:
        kpi_data (dict): A dictionary containing activity counts with the following keys:
            - internships: Number of internships completed
            - hackathons: Number of hackathons participated in
            - certifications: Number of certifications obtained
            - projects: Number of projects completed
            - publications: Number of publications
            - workshops: Number of workshops attended
            - industrial_visits: Number of industrial visits attended
            - club_activities: Number of club activities participated in
    
    Returns:
        float: The weighted KPI score
    
    Example:
        >>> data = {
        ...     'internships': 2,
        ...     'hackathons': 1,
        ...     'certifications': 3,
        ...     'projects': 4,
        ...     'publications': 1,
        ...     'workshops': 2,
        ...     'industrial_visits': 1,
        ...     'club_activities': 5
        ... }
        >>> score = calculate_kpi_score(data)
    """
    # Define weights for each activity dynamically using environment variables
    weights = {
        'internships': float(os.getenv('KPI_WEIGHT_INTERNSHIPS', '25')),
        'certifications': float(os.getenv('KPI_WEIGHT_CERTIFICATIONS', '15')),
        'hackathons': float(os.getenv('KPI_WEIGHT_HACKATHONS', '20')),
        'publications': float(os.getenv('KPI_WEIGHT_PUBLICATIONS', '25')),
        'workshops': float(os.getenv('KPI_WEIGHT_WORKSHOPS', '5')),
        'projects': float(os.getenv('KPI_WEIGHT_PROJECTS', '10')),
        'industrial_visits': 10,
        'club_activities': 5
    }
    
    total_score = 0
    
    # Calculate weighted score for each activity
    for activity, weight in weights.items():
        count = kpi_data.get(activity, 0)
        total_score += count * weight
    
    return total_score


def predict_career_readiness(score):
    """
    Predicts the level of career readiness based on a KPI score.
    
    Args:
        score (float): The KPI score to evaluate
    
    Returns:
        str: One of three readiness levels:
            - "High readiness" if score >= 80
            - "Medium readiness" if 50 <= score < 80
            - "Low readiness" if score < 50
    
    Example:
        >>> predict_career_readiness(85)
        'High readiness'
        >>> predict_career_readiness(65)
        'Medium readiness'
        >>> predict_career_readiness(30)
        'Low readiness'
    """
    if score >= 80:
        return "High readiness"
    elif 50 <= score < 80:
        return "Medium readiness"
    else:
        return "Low readiness"

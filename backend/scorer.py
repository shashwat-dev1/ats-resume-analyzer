"""
Scoring aggregation module for ATS Resume Analyzer.
Combines various analysis metrics into final scores.
"""


def calculate_ats_score(section_analysis, skill_analysis, verb_analysis, ats_compatibility):
    """
    Calculate overall ATS score (0-100).
    
    Weighting:
    - Section completeness: 30%
    - Skill keyword density: 25%
    - Action verb usage: 20%
    - ATS compatibility: 25%
    
    Args:
        section_analysis: Section analysis results
        skill_analysis: Skill density analysis
        verb_analysis: Action verb analysis
        ats_compatibility: ATS compatibility check
    
    Returns:
        Overall ATS score (0-100)
    """
    # Calculate section completeness score
    critical_sections = ['skills', 'education', 'experience']
    important_sections = ['objective', 'summary', 'projects']
    
    section_score = 0
    total_weight = 0
    
    for section_name, analysis in section_analysis.items():
        if section_name in critical_sections:
            weight = 10
        elif section_name in important_sections:
            weight = 5
        else:
            weight = 2
        
        section_score += analysis['score'] * weight
        total_weight += weight
    
    section_completeness = (section_score / total_weight) if total_weight > 0 else 0
    
    # Get individual scores
    skill_density_score = skill_analysis['density_score']
    action_verb_score = verb_analysis['verb_score']
    compatibility_score = ats_compatibility['score']
    
    # Calculate weighted average
    ats_score = (
        section_completeness * 0.30 +
        skill_density_score * 0.25 +
        action_verb_score * 0.20 +
        compatibility_score * 0.25
    )
    
    return round(ats_score, 2)


def calculate_jd_match(tfidf_similarity, skill_overlap):
    """
    Calculate job description match score (0-100).
    
    Combines:
    - TF-IDF similarity: 60%
    - Skill overlap: 40%
    
    Args:
        tfidf_similarity: TF-IDF cosine similarity score
        skill_overlap: Skill overlap analysis
    
    Returns:
        JD match score (0-100)
    """
    overlap_percentage = skill_overlap['overlap_percentage']
    
    jd_match = (
        tfidf_similarity * 0.60 +
        overlap_percentage * 0.40
    )
    
    return round(jd_match, 2)


def generate_section_scores(section_analysis):
    """
    Generate formatted section scores for display.
    
    Args:
        section_analysis: Section analysis results
    
    Returns:
        Dictionary of section scores
    """
    section_scores = {}
    
    for section_name, analysis in section_analysis.items():
        if analysis['present'] or analysis['importance'] in ['critical', 'important']:
            section_scores[section_name] = {
                'present': analysis['present'],
                'score': analysis['score'],
                'observation': analysis['observation'],
                'importance': analysis['importance']
            }
    
    return section_scores


def get_score_interpretation(ats_score, jd_match_score=None):
    """
    Get human-readable interpretation of scores.
    
    Args:
        ats_score: ATS score (0-100)
        jd_match_score: Optional JD match score
    
    Returns:
        Dictionary with interpretations
    """
    # ATS score interpretation
    if ats_score >= 80:
        ats_interpretation = "Excellent - Your resume is highly ATS-compatible"
        ats_level = "excellent"
    elif ats_score >= 60:
        ats_interpretation = "Good - Your resume should pass most ATS systems"
        ats_level = "good"
    elif ats_score >= 40:
        ats_interpretation = "Fair - Consider improvements to increase ATS compatibility"
        ats_level = "fair"
    else:
        ats_interpretation = "Needs Improvement - Significant changes recommended"
        ats_level = "poor"
    
    result = {
        'ats_interpretation': ats_interpretation,
        'ats_level': ats_level
    }
    
    # JD match interpretation (if provided)
    if jd_match_score is not None:
        if jd_match_score >= 75:
            jd_interpretation = "Strong Match - Your resume aligns well with the job description"
            jd_level = "excellent"
        elif jd_match_score >= 60:
            jd_interpretation = "Good Match - Your resume is relevant to the position"
            jd_level = "good"
        elif jd_match_score >= 40:
            jd_interpretation = "Moderate Match - Consider highlighting relevant skills"
            jd_level = "fair"
        else:
            jd_interpretation = "Weak Match - Your resume may not align with this position"
            jd_level = "poor"
        
        result['jd_interpretation'] = jd_interpretation
        result['jd_level'] = jd_level
    
    return result

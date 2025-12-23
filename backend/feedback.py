"""
Rule-based feedback and recommendation engine for ATS Resume Analyzer.
Generates actionable insights based on analysis results.
"""


def generate_recommendations(ats_score, section_analysis, skill_analysis, verb_analysis, 
                            ats_compatibility, jd_analysis=None):
    """
    Generate actionable recommendations based on analysis.
    
    Args:
        ats_score: Overall ATS score
        section_analysis: Section analysis results
        skill_analysis: Skill density analysis
        verb_analysis: Action verb analysis
        ats_compatibility: ATS compatibility check
        jd_analysis: Optional JD match analysis
    
    Returns:
        List of recommendations (prioritized)
    """
    recommendations = []
    
    # Critical recommendations (missing critical sections)
    critical_sections = ['skills', 'education', 'experience']
    for section in critical_sections:
        if section in section_analysis and not section_analysis[section]['present']:
            recommendations.append({
                'priority': 'critical',
                'category': 'missing_section',
                'message': f"Add a {section.title()} section - this is essential for ATS parsing"
            })
    
    # Important recommendations (missing important sections)
    important_sections = ['objective', 'summary', 'projects']
    for section in important_sections:
        if section in section_analysis and not section_analysis[section]['present']:
            recommendations.append({
                'priority': 'important',
                'category': 'missing_section',
                'message': f"Consider adding a {section.title()} section to strengthen your resume"
            })
    
    # Skill-related recommendations
    if skill_analysis['skill_count'] < 5:
        recommendations.append({
            'priority': 'critical',
            'category': 'skills',
            'message': "Add more technical skills - aim for at least 8-10 relevant skills"
        })
    elif skill_analysis['skill_count'] < 10:
        recommendations.append({
            'priority': 'important',
            'category': 'skills',
            'message': "Expand your skills section with more relevant technologies"
        })
    
    # Action verb recommendations
    if verb_analysis['verb_count'] < 3:
        recommendations.append({
            'priority': 'important',
            'category': 'action_verbs',
            'message': "Use stronger action verbs like 'achieved', 'led', 'implemented', 'optimized'"
        })
    elif verb_analysis['verb_count'] < 6:
        recommendations.append({
            'priority': 'suggested',
            'category': 'action_verbs',
            'message': "Increase use of action verbs to make your accomplishments more impactful"
        })
    
    # ATS compatibility recommendations
    if not ats_compatibility['is_compatible']:
        for issue in ats_compatibility['issues']:
            recommendations.append({
                'priority': 'important',
                'category': 'ats_compatibility',
                'message': issue
            })
    
    # Section quality recommendations
    for section_name, analysis in section_analysis.items():
        if analysis['present'] and analysis['score'] < 60:
            if section_name == 'experience':
                recommendations.append({
                    'priority': 'important',
                    'category': 'section_quality',
                    'message': "Expand your Experience section with more detailed accomplishments and metrics"
                })
            elif section_name == 'skills':
                recommendations.append({
                    'priority': 'important',
                    'category': 'section_quality',
                    'message': "List more specific skills and technologies in your Skills section"
                })
    
    # JD-specific recommendations
    if jd_analysis:
        missing_skills = jd_analysis.get('missing_skills', [])
        if len(missing_skills) > 0:
            # Show top 5 missing skills
            top_missing = missing_skills[:5]
            recommendations.append({
                'priority': 'critical',
                'category': 'jd_match',
                'message': f"Add these job-relevant skills if you have them: {', '.join(top_missing)}"
            })
        
        overlap_percentage = jd_analysis.get('overlap_percentage', 0)
        if overlap_percentage < 40:
            recommendations.append({
                'priority': 'important',
                'category': 'jd_match',
                'message': "Your resume has limited overlap with the job description - tailor it to match key requirements"
            })
    
    # General recommendations based on overall score
    if ats_score < 60:
        recommendations.append({
            'priority': 'important',
            'category': 'general',
            'message': "Use a simple, clean format with clear section headings"
        })
        recommendations.append({
            'priority': 'suggested',
            'category': 'general',
            'message': "Avoid tables, images, and complex formatting that ATS systems may not parse correctly"
        })
    
    # Sort by priority
    priority_order = {'critical': 0, 'important': 1, 'suggested': 2}
    recommendations.sort(key=lambda x: priority_order.get(x['priority'], 3))
    
    return recommendations


def identify_strengths(section_analysis, skill_analysis, verb_analysis, ats_compatibility):
    """
    Identify strong points in the resume.
    
    Args:
        section_analysis: Section analysis results
        skill_analysis: Skill density analysis
        verb_analysis: Action verb analysis
        ats_compatibility: ATS compatibility check
    
    Returns:
        List of strengths
    """
    strengths = []
    
    # Check for strong sections
    for section_name, analysis in section_analysis.items():
        if analysis['present'] and analysis['score'] >= 80:
            strengths.append(f"Strong {section_name.title()} section")
    
    # Check skill density
    if skill_analysis['skill_count'] >= 10:
        strengths.append(f"Comprehensive skills coverage ({skill_analysis['skill_count']} skills identified)")
    
    # Check action verbs
    if verb_analysis['verb_count'] >= 8:
        strengths.append(f"Excellent use of action verbs ({verb_analysis['verb_count']} strong verbs)")
    
    # Check ATS compatibility
    if ats_compatibility['score'] >= 90:
        strengths.append("Highly ATS-compatible format")
    
    return strengths


def generate_summary(ats_score, jd_match_score, recommendations, strengths):
    """
    Generate executive summary of the analysis.
    
    Args:
        ats_score: ATS score
        jd_match_score: JD match score (optional)
        recommendations: List of recommendations
        strengths: List of strengths
    
    Returns:
        Summary text
    """
    summary_parts = []
    
    # Overall assessment
    if ats_score >= 75:
        summary_parts.append("Your resume is well-optimized for ATS systems.")
    elif ats_score >= 60:
        summary_parts.append("Your resume is generally ATS-friendly with room for improvement.")
    else:
        summary_parts.append("Your resume needs significant improvements for ATS compatibility.")
    
    # JD match (if available)
    if jd_match_score is not None:
        if jd_match_score >= 70:
            summary_parts.append(f"It shows a strong match ({jd_match_score}%) with the job description.")
        elif jd_match_score >= 50:
            summary_parts.append(f"It has a moderate match ({jd_match_score}%) with the job description.")
        else:
            summary_parts.append(f"It has limited alignment ({jd_match_score}%) with the job description.")
    
    # Highlight top strength
    if strengths:
        summary_parts.append(f"Key strength: {strengths[0]}.")
    
    # Highlight top recommendation
    critical_recs = [r for r in recommendations if r['priority'] == 'critical']
    if critical_recs:
        summary_parts.append(f"Priority action: {critical_recs[0]['message']}.")
    
    return " ".join(summary_parts)

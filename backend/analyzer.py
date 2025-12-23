"""
Core analysis engine for ATS Resume Analyzer.
Implements NLP-based scoring for section quality, skill density, action verbs, and JD matching.
"""

import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


# Common technical skills database
COMMON_SKILLS = {
    'programming': [
        'python', 'java', 'javascript', 'typescript', 'c', 'cpp', 'csharp', 'ruby', 'php', 'swift',
        'kotlin', 'go', 'rust', 'scala', 'r', 'matlab', 'perl', 'shell', 'bash', 'powershell'
    ],
    'web': [
        'html', 'css', 'react', 'angular', 'vue', 'nodejs', 'express', 'django', 'flask', 'fastapi',
        'spring', 'asp.net', 'jquery', 'bootstrap', 'tailwind', 'sass', 'webpack', 'nextjs', 'gatsby'
    ],
    'database': [
        'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'cassandra', 'oracle', 'sqlite',
        'dynamodb', 'elasticsearch', 'neo4j', 'firebase', 'mariadb'
    ],
    'cloud': [
        'aws', 'azure', 'gcp', 'google cloud platform', 'amazon web services', 'docker', 'kubernetes',
        'terraform', 'ansible', 'jenkins', 'gitlab', 'github actions', 'circleci', 'heroku'
    ],
    'data_science': [
        'machine learning', 'deep learning', 'artificial intelligence', 'natural language processing',
        'computer vision', 'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy',
        'matplotlib', 'seaborn', 'tableau', 'power bi', 'spark', 'hadoop', 'data analysis'
    ],
    'mobile': [
        'android', 'ios', 'react native', 'flutter', 'xamarin', 'swift', 'kotlin', 'mobile development'
    ],
    'soft_skills': [
        'leadership', 'communication', 'teamwork', 'problem solving', 'analytical', 'critical thinking',
        'time management', 'project management', 'agile', 'scrum', 'collaboration', 'presentation'
    ]
}

# Strong action verbs for resume
ACTION_VERBS = [
    'achieved', 'accomplished', 'administered', 'analyzed', 'architected', 'automated', 'built',
    'collaborated', 'created', 'delivered', 'designed', 'developed', 'directed', 'drove',
    'enhanced', 'established', 'executed', 'generated', 'implemented', 'improved', 'increased',
    'initiated', 'launched', 'led', 'managed', 'optimized', 'orchestrated', 'organized',
    'pioneered', 'planned', 'produced', 'reduced', 'resolved', 'spearheaded', 'streamlined',
    'strengthened', 'transformed', 'upgraded'
]


def analyze_sections(sections):
    """
    Analyze each resume section for completeness and quality.
    
    Args:
        sections: Dictionary of section names and content
    
    Returns:
        Dictionary with section analysis results
    """
    analysis = {}
    
    critical_sections = ['skills', 'education', 'experience']
    important_sections = ['objective', 'summary', 'projects']
    optional_sections = ['internships', 'achievements', 'certifications']
    
    for section_name, content in sections.items():
        is_present = bool(content and len(content.strip()) > 10)
        
        # Determine importance
        if section_name in critical_sections:
            importance = 'critical'
        elif section_name in important_sections:
            importance = 'important'
        else:
            importance = 'optional'
        
        # Calculate quality score based on content length and structure
        quality_score = 0
        observation = ""
        
        if is_present:
            word_count = len(content.split())
            
            if section_name == 'skills':
                # Skills section should have multiple items
                skill_count = len(re.findall(r'[,\n•\-]', content)) + 1
                if skill_count >= 10:
                    quality_score = 90
                    observation = "Strong technical skills listed"
                elif skill_count >= 5:
                    quality_score = 70
                    observation = "Good skills coverage"
                else:
                    quality_score = 50
                    observation = "Limited skills listed"
            
            elif section_name in ['experience', 'internships']:
                # Experience should have detailed descriptions
                if word_count >= 100:
                    quality_score = 90
                    observation = "Well-detailed experience"
                elif word_count >= 50:
                    quality_score = 70
                    observation = "Adequate experience details"
                else:
                    quality_score = 50
                    observation = "Brief experience description"
            
            elif section_name == 'education':
                # Education should mention degree and institution
                if word_count >= 20:
                    quality_score = 85
                    observation = "Complete education details"
                else:
                    quality_score = 60
                    observation = "Basic education info"
            
            elif section_name in ['projects', 'achievements']:
                if word_count >= 50:
                    quality_score = 85
                    observation = f"Strong {section_name} section"
                else:
                    quality_score = 60
                    observation = f"Brief {section_name} description"
            
            else:
                quality_score = 70 if word_count >= 20 else 50
                observation = "Section present"
        else:
            quality_score = 0
            observation = "Section missing"
        
        analysis[section_name] = {
            'present': is_present,
            'importance': importance,
            'score': quality_score,
            'observation': observation,
            'word_count': len(content.split()) if is_present else 0
        }
    
    return analysis


def calculate_skill_density(text, sections):
    """
    Calculate skill keyword density in resume.
    
    Args:
        text: Preprocessed resume text
        sections: Detected sections
    
    Returns:
        Dictionary with skill analysis
    """
    text_lower = text.lower()
    
    # Extract all skills from common skills database
    all_skills = []
    for category, skills in COMMON_SKILLS.items():
        all_skills.extend(skills)
    
    # Find skills mentioned in resume
    found_skills = []
    for skill in all_skills:
        # Use word boundary to avoid partial matches
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.append(skill)
    
    # Calculate density score
    skill_count = len(found_skills)
    
    if skill_count >= 15:
        density_score = 95
    elif skill_count >= 10:
        density_score = 80
    elif skill_count >= 5:
        density_score = 60
    else:
        density_score = 30
    
    return {
        'found_skills': found_skills,
        'skill_count': skill_count,
        'density_score': density_score
    }


def detect_action_verbs(text):
    """
    Detect strong action verbs in resume.
    
    Args:
        text: Resume text
    
    Returns:
        Dictionary with action verb analysis
    """
    text_lower = text.lower()
    
    found_verbs = []
    for verb in ACTION_VERBS:
        pattern = r'\b' + re.escape(verb) + r'\b'
        if re.search(pattern, text_lower):
            found_verbs.append(verb)
    
    verb_count = len(found_verbs)
    
    # Score based on action verb usage
    if verb_count >= 10:
        verb_score = 95
        observation = "Excellent use of action verbs"
    elif verb_count >= 6:
        verb_score = 80
        observation = "Good action verb usage"
    elif verb_count >= 3:
        verb_score = 60
        observation = "Moderate action verb usage"
    else:
        verb_score = 30
        observation = "Limited action verbs"
    
    return {
        'found_verbs': found_verbs,
        'verb_count': verb_count,
        'verb_score': verb_score,
        'observation': observation
    }


def check_ats_compatibility(text):
    """
    Check for ATS compatibility issues.
    
    Args:
        text: Raw resume text
    
    Returns:
        Dictionary with compatibility analysis
    """
    issues = []
    score = 100
    
    # Check for excessive special characters (might indicate tables/graphics)
    special_char_count = len(re.findall(r'[│┤├┼┬┴╪═║╔╗╚╝]', text))
    if special_char_count > 10:
        issues.append("Contains table formatting that may not parse well")
        score -= 20
    
    # Check for very short lines (might indicate columns)
    lines = text.split('\n')
    short_lines = sum(1 for line in lines if 0 < len(line.strip()) < 20)
    if short_lines > len(lines) * 0.3:
        issues.append("Multiple short lines detected - avoid multi-column layouts")
        score -= 15
    
    # Check for excessive capitalization
    if text.isupper():
        issues.append("Excessive capitalization - use mixed case")
        score -= 10
    
    # Check for reasonable length
    word_count = len(text.split())
    if word_count < 100:
        issues.append("Resume appears too short")
        score -= 20
    elif word_count > 1500:
        issues.append("Resume may be too long - consider condensing")
        score -= 10
    
    return {
        'score': max(score, 0),
        'issues': issues,
        'is_compatible': score >= 70
    }


def compute_tfidf_similarity(resume_text, jd_text):
    """
    Calculate TF-IDF cosine similarity between resume and job description.
    
    Args:
        resume_text: Preprocessed resume text
        jd_text: Preprocessed job description text
    
    Returns:
        Similarity score (0-100)
    """
    try:
        vectorizer = TfidfVectorizer(max_features=500, stop_words='english')
        
        # Create TF-IDF matrix
        tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
        
        # Calculate cosine similarity
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        
        # Convert to percentage
        similarity_score = round(similarity * 100, 2)
        
        return similarity_score
    except Exception as e:
        print(f"Error calculating TF-IDF similarity: {e}")
        return 0


def find_skill_overlap(resume_text, jd_text):
    """
    Find skill overlap between resume and job description.
    
    Args:
        resume_text: Resume text
        jd_text: Job description text
    
    Returns:
        Dictionary with skill overlap analysis
    """
    resume_lower = resume_text.lower()
    jd_lower = jd_text.lower()
    
    # Extract all skills
    all_skills = []
    for category, skills in COMMON_SKILLS.items():
        all_skills.extend(skills)
    
    # Find skills in resume and JD
    resume_skills = set()
    jd_skills = set()
    
    for skill in all_skills:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, resume_lower):
            resume_skills.add(skill)
        if re.search(pattern, jd_lower):
            jd_skills.add(skill)
    
    # Calculate overlap
    matching_skills = resume_skills.intersection(jd_skills)
    missing_skills = jd_skills - resume_skills
    
    if len(jd_skills) > 0:
        overlap_percentage = round((len(matching_skills) / len(jd_skills)) * 100, 2)
    else:
        overlap_percentage = 0
    
    return {
        'resume_skills': list(resume_skills),
        'jd_skills': list(jd_skills),
        'matching_skills': list(matching_skills),
        'missing_skills': list(missing_skills),
        'overlap_percentage': overlap_percentage
    }

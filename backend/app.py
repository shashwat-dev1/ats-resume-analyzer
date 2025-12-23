"""
Flask API for ATS Resume Analyzer.
Main application with file upload and analysis endpoints.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import io

# Import analysis modules
from parser import extract_text, detect_sections, preprocess_text, normalize_skills
from analyzer import (
    analyze_sections, calculate_skill_density, detect_action_verbs,
    check_ats_compatibility, compute_tfidf_similarity, find_skill_overlap
)
from scorer import (
    calculate_ats_score, calculate_jd_match, generate_section_scores,
    get_score_interpretation
)
from feedback import generate_recommendations, identify_strengths, generate_summary

app = Flask(__name__)
CORS(app)

# Configuration
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_file_extension(filename):
    """Get file extension."""
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else ''


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'message': 'ATS Resume Analyzer API is running'})


@app.route('/api/analyze', methods=['POST'])
def analyze_resume():
    """
    Main analysis endpoint.
    Accepts resume (required) and job description (optional).
    Returns comprehensive analysis with scores and recommendations.
    """
    try:
        # Validate resume file
        if 'resume' not in request.files:
            return jsonify({'error': 'Resume file is required'}), 400
        
        resume_file = request.files['resume']
        
        if resume_file.filename == '':
            return jsonify({'error': 'No resume file selected'}), 400
        
        if not allowed_file(resume_file.filename):
            return jsonify({'error': 'Invalid resume file type. Allowed: PDF, DOCX'}), 400
        
        # Get job description (optional)
        jd_file = request.files.get('job_description')
        has_jd = jd_file is not None and jd_file.filename != ''
        
        if has_jd and not allowed_file(jd_file.filename):
            return jsonify({'error': 'Invalid job description file type. Allowed: PDF, DOCX, TXT'}), 400
        
        # Extract text from resume
        resume_ext = get_file_extension(resume_file.filename)
        resume_stream = io.BytesIO(resume_file.read())
        
        try:
            resume_text = extract_text(resume_stream, resume_ext)
        except Exception as e:
            return jsonify({'error': f'Failed to extract resume text: {str(e)}'}), 400
        
        if not resume_text or len(resume_text.strip()) < 50:
            return jsonify({'error': 'Resume appears to be empty or too short'}), 400
        
        # Extract text from job description (if provided)
        jd_text = None
        if has_jd:
            jd_ext = get_file_extension(jd_file.filename)
            jd_stream = io.BytesIO(jd_file.read())
            
            try:
                if jd_ext == 'txt':
                    jd_text = jd_stream.read().decode('utf-8', errors='ignore')
                else:
                    jd_text = extract_text(jd_stream, jd_ext)
            except Exception as e:
                return jsonify({'error': f'Failed to extract job description text: {str(e)}'}), 400
        
        # Detect sections in resume
        sections = detect_sections(resume_text)
        
        # Preprocess text
        resume_processed = preprocess_text(resume_text)
        resume_normalized = normalize_skills(resume_text)
        
        # Analyze sections
        section_analysis = analyze_sections(sections)
        
        # Calculate skill density
        skill_analysis = calculate_skill_density(resume_normalized, sections)
        
        # Detect action verbs
        verb_analysis = detect_action_verbs(resume_text)
        
        # Check ATS compatibility
        ats_compatibility = check_ats_compatibility(resume_text)
        
        # Calculate ATS score
        ats_score = calculate_ats_score(
            section_analysis,
            skill_analysis,
            verb_analysis,
            ats_compatibility
        )
        
        # Prepare response
        response = {
            'ats_score': ats_score,
            'sections': generate_section_scores(section_analysis),
            'skills': {
                'found_skills': skill_analysis['found_skills'],
                'skill_count': skill_analysis['skill_count']
            },
            'action_verbs': {
                'found_verbs': verb_analysis['found_verbs'],
                'verb_count': verb_analysis['verb_count']
            },
            'ats_compatibility': {
                'is_compatible': ats_compatibility['is_compatible'],
                'issues': ats_compatibility['issues']
            }
        }
        
        # JD analysis (if provided)
        jd_analysis = None
        if has_jd and jd_text:
            jd_processed = preprocess_text(jd_text)
            jd_normalized = normalize_skills(jd_text)
            
            # Calculate TF-IDF similarity
            tfidf_similarity = compute_tfidf_similarity(
                resume_processed['text'],
                jd_processed['text']
            )
            
            # Find skill overlap
            skill_overlap = find_skill_overlap(resume_normalized, jd_normalized)
            
            # Calculate JD match score
            jd_match_score = calculate_jd_match(tfidf_similarity, skill_overlap)
            
            jd_analysis = {
                'overlap_percentage': skill_overlap['overlap_percentage'],
                'missing_skills': skill_overlap['missing_skills']
            }
            
            response['jd_match_score'] = jd_match_score
            response['jd_analysis'] = {
                'tfidf_similarity': tfidf_similarity,
                'matching_skills': skill_overlap['matching_skills'],
                'missing_skills': skill_overlap['missing_skills'],
                'overlap_percentage': skill_overlap['overlap_percentage']
            }
        
        # Generate recommendations
        recommendations = generate_recommendations(
            ats_score,
            section_analysis,
            skill_analysis,
            verb_analysis,
            ats_compatibility,
            jd_analysis
        )
        
        response['recommendations'] = recommendations
        
        # Identify strengths
        strengths = identify_strengths(
            section_analysis,
            skill_analysis,
            verb_analysis,
            ats_compatibility
        )
        
        response['strengths'] = strengths
        
        # Generate summary
        jd_match_score = response.get('jd_match_score')
        summary = generate_summary(ats_score, jd_match_score, recommendations, strengths)
        response['summary'] = summary
        
        # Add score interpretations
        interpretations = get_score_interpretation(ats_score, jd_match_score)
        response['interpretations'] = interpretations
        
        return jsonify(response), 200
    
    except Exception as e:
        print(f"Error in analyze_resume: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.route('/', methods=['GET'])
def index():
    """Root endpoint."""
    return jsonify({
        'message': 'ATS Resume Analyzer API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/api/health',
            'analyze': '/api/analyze (POST)'
        }
    })


if __name__ == '__main__':
    print("Starting ATS Resume Analyzer API...")
    print("Server running on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

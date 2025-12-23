"""
Quick test script to verify backend setup and basic functionality.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    try:
        import parser
        import analyzer
        import scorer
        import feedback
        import app
        print("✓ All modules imported successfully")
        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False

def test_text_processing():
    """Test basic text processing functions."""
    print("\nTesting text processing...")
    try:
        from parser import preprocess_text, normalize_skills
        
        sample_text = "I have experience with Python, ML, and JavaScript development."
        
        # Test preprocessing
        processed = preprocess_text(sample_text)
        assert 'tokens' in processed
        assert 'text' in processed
        print(f"✓ Preprocessed text: {len(processed['tokens'])} tokens")
        
        # Test skill normalization
        normalized = normalize_skills(sample_text)
        assert 'machine learning' in normalized.lower()
        assert 'javascript' in normalized.lower()
        print("✓ Skill normalization working")
        
        return True
    except Exception as e:
        print(f"✗ Text processing error: {e}")
        return False

def test_section_detection():
    """Test section detection logic."""
    print("\nTesting section detection...")
    try:
        from parser import detect_sections
        
        sample_resume = """
        SKILLS
        Python, JavaScript, React, Flask
        
        EXPERIENCE
        Software Engineer at Tech Corp
        Developed web applications
        
        EDUCATION
        BS in Computer Science
        """
        
        sections = detect_sections(sample_resume)
        assert sections['skills'] != ''
        assert sections['experience'] != ''
        assert sections['education'] != ''
        print(f"✓ Detected {sum(1 for s in sections.values() if s)} sections")
        
        return True
    except Exception as e:
        print(f"✗ Section detection error: {e}")
        return False

def test_analysis():
    """Test analysis functions."""
    print("\nTesting analysis functions...")
    try:
        from analyzer import analyze_sections, calculate_skill_density, detect_action_verbs
        
        sections = {
            'skills': 'Python, JavaScript, React, Node.js, MongoDB',
            'experience': 'Led development of web applications. Achieved 50% performance improvement.',
            'education': 'BS Computer Science, MIT'
        }
        
        # Test section analysis
        section_analysis = analyze_sections(sections)
        assert 'skills' in section_analysis
        assert section_analysis['skills']['present'] == True
        print(f"✓ Section analysis: {len(section_analysis)} sections analyzed")
        
        # Test skill density
        text = "python javascript react nodejs mongodb flask django"
        skill_analysis = calculate_skill_density(text, sections)
        assert skill_analysis['skill_count'] > 0
        print(f"✓ Skill density: {skill_analysis['skill_count']} skills found")
        
        # Test action verbs
        text = "Led team, achieved goals, implemented solutions, optimized performance"
        verb_analysis = detect_action_verbs(text)
        assert verb_analysis['verb_count'] > 0
        print(f"✓ Action verbs: {verb_analysis['verb_count']} verbs found")
        
        return True
    except Exception as e:
        print(f"✗ Analysis error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_scoring():
    """Test scoring functions."""
    print("\nTesting scoring functions...")
    try:
        from scorer import calculate_ats_score
        
        section_analysis = {
            'skills': {'score': 85, 'present': True},
            'experience': {'score': 90, 'present': True},
            'education': {'score': 80, 'present': True}
        }
        
        skill_analysis = {'density_score': 75}
        verb_analysis = {'verb_score': 80}
        ats_compatibility = {'score': 85}
        
        ats_score = calculate_ats_score(
            section_analysis,
            skill_analysis,
            verb_analysis,
            ats_compatibility
        )
        
        assert 0 <= ats_score <= 100
        print(f"✓ ATS Score calculation: {ats_score}/100")
        
        return True
    except Exception as e:
        print(f"✗ Scoring error: {e}")
        return False

def test_recommendations():
    """Test recommendation generation."""
    print("\nTesting recommendation generation...")
    try:
        from feedback import generate_recommendations
        
        section_analysis = {
            'skills': {'score': 50, 'present': True},
            'experience': {'score': 90, 'present': True},
            'projects': {'score': 0, 'present': False}
        }
        
        skill_analysis = {'skill_count': 3}
        verb_analysis = {'verb_count': 2}
        ats_compatibility = {'score': 70, 'is_compatible': True, 'issues': []}
        
        recommendations = generate_recommendations(
            60,
            section_analysis,
            skill_analysis,
            verb_analysis,
            ats_compatibility
        )
        
        assert len(recommendations) > 0
        print(f"✓ Generated {len(recommendations)} recommendations")
        
        return True
    except Exception as e:
        print(f"✗ Recommendation error: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("ATS Resume Analyzer - Backend Test Suite")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_text_processing,
        test_section_detection,
        test_analysis,
        test_scoring,
        test_recommendations
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    print(f"Test Results: {sum(results)}/{len(results)} passed")
    print("=" * 60)
    
    if all(results):
        print("\n✓ All tests passed! Backend is ready to use.")
        return 0
    else:
        print("\n✗ Some tests failed. Please check the errors above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())

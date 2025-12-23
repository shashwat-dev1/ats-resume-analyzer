"""
Text extraction and section detection module for ATS Resume Analyzer.
Handles PDF and DOCX files, detects resume sections using rule-based heuristics.
"""

import re
import pdfplumber
from docx import Document
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

# Download required NLTK data (will be cached after first run)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)


def extract_text_from_pdf(file_stream):
    """Extract text from PDF file."""
    text = ""
    try:
        with pdfplumber.open(file_stream) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        raise ValueError(f"Error extracting text from PDF: {str(e)}")
    return text


def extract_text_from_docx(file_stream):
    """Extract text from DOCX file."""
    text = ""
    try:
        doc = Document(file_stream)
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
    except Exception as e:
        raise ValueError(f"Error extracting text from DOCX: {str(e)}")
    return text


def extract_text(file_stream, file_type):
    """
    Extract text from uploaded file based on type.
    
    Args:
        file_stream: File-like object
        file_type: 'pdf' or 'docx'
    
    Returns:
        Extracted text as string
    """
    if file_type == 'pdf':
        return extract_text_from_pdf(file_stream)
    elif file_type in ['docx', 'doc']:
        return extract_text_from_docx(file_stream)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")


def detect_sections(text):
    """
    Detect resume sections using rule-based pattern matching.
    
    Args:
        text: Raw resume text
    
    Returns:
        Dictionary with section names as keys and content as values
    """
    sections = {
        'objective': '',
        'summary': '',
        'skills': '',
        'education': '',
        'experience': '',
        'internships': '',
        'projects': '',
        'achievements': '',
        'certifications': '',
        'contact': ''
    }
    
    # Section header patterns (case-insensitive)
    section_patterns = {
        'objective': r'(?:^|\n)\s*(?:objective|career objective|professional objective)\s*[:\n]',
        'summary': r'(?:^|\n)\s*(?:summary|professional summary|profile|about me)\s*[:\n]',
        'skills': r'(?:^|\n)\s*(?:skills|technical skills|core competencies|expertise|technologies)\s*[:\n]',
        'education': r'(?:^|\n)\s*(?:education|academic background|qualifications)\s*[:\n]',
        'experience': r'(?:^|\n)\s*(?:experience|work experience|professional experience|employment history)\s*[:\n]',
        'internships': r'(?:^|\n)\s*(?:internships?|internship experience)\s*[:\n]',
        'projects': r'(?:^|\n)\s*(?:projects?|academic projects?|personal projects?)\s*[:\n]',
        'achievements': r'(?:^|\n)\s*(?:achievements?|accomplishments?|awards?|honors?)\s*[:\n]',
        'certifications': r'(?:^|\n)\s*(?:certifications?|certificates?|licenses?)\s*[:\n]',
        'contact': r'(?:^|\n)\s*(?:contact|contact information|personal details)\s*[:\n]'
    }
    
    # Find all section positions
    section_positions = []
    for section_name, pattern in section_patterns.items():
        matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
        for match in matches:
            section_positions.append((match.start(), section_name))
    
    # Sort by position
    section_positions.sort()
    
    # Extract content between sections
    for i, (start_pos, section_name) in enumerate(section_positions):
        if i < len(section_positions) - 1:
            end_pos = section_positions[i + 1][0]
            content = text[start_pos:end_pos].strip()
        else:
            content = text[start_pos:].strip()
        
        # Remove the section header from content
        content_lines = content.split('\n')
        if content_lines:
            content = '\n'.join(content_lines[1:]).strip()
        
        sections[section_name] = content
    
    return sections


def preprocess_text(text):
    """
    Preprocess text for analysis: lowercase, remove stopwords, tokenize.
    
    Args:
        text: Raw text
    
    Returns:
        Dictionary with processed text and tokens
    """
    # Convert to lowercase
    text_lower = text.lower()
    
    # Remove special characters but keep alphanumeric and spaces
    text_clean = re.sub(r'[^a-z0-9\s+#]', ' ', text_lower)
    
    # Tokenize
    try:
        tokens = word_tokenize(text_clean)
    except:
        # Fallback to simple split if NLTK tokenizer fails
        tokens = text_clean.split()
    
    # Remove stopwords
    try:
        stop_words = set(stopwords.words('english'))
        tokens_filtered = [word for word in tokens if word not in stop_words and len(word) > 2]
    except:
        # If stopwords not available, just filter short words
        tokens_filtered = [word for word in tokens if len(word) > 2]
    
    return {
        'text': text_clean,
        'tokens': tokens_filtered,
        'original': text
    }


def normalize_skills(text):
    """
    Normalize skill synonyms and variations.
    
    Args:
        text: Text containing skills
    
    Returns:
        Text with normalized skills
    """
    skill_synonyms = {
        'ml': 'machine learning',
        'ai': 'artificial intelligence',
        'dl': 'deep learning',
        'nlp': 'natural language processing',
        'js': 'javascript',
        'ts': 'typescript',
        'py': 'python',
        'react.js': 'react',
        'node.js': 'nodejs',
        'vue.js': 'vue',
        'angular.js': 'angular',
        'c++': 'cpp',
        'c#': 'csharp',
        'db': 'database',
        'rdbms': 'relational database',
        'nosql': 'non-relational database',
        'aws': 'amazon web services',
        'gcp': 'google cloud platform',
        'k8s': 'kubernetes',
        'ci/cd': 'continuous integration continuous deployment',
        'devops': 'development operations',
        'ui/ux': 'user interface user experience'
    }
    
    text_lower = text.lower()
    for abbrev, full_form in skill_synonyms.items():
        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(abbrev) + r'\b'
        text_lower = re.sub(pattern, full_form, text_lower)
    
    return text_lower

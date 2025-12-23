# ATS Resume Analyzer

A powerful, privacy-focused Applicant Tracking System (ATS) simulator that helps job seekers optimize their resumes. This tool performs deep NLP analysis to evaluate resume content against job descriptions, providing actionable feedback on skills, formatting, and keyword matching.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![React](https://img.shields.io/badge/react-18-61dafb.svg)

## 🚀 Features

- **Smart Resume Parsing**: Automatically extracts and segments resume sections (Skills, Experience, Education).
- **ATS Compatibility Score**: Calculates a 0-100 score based on industry-standard ATS algorithms.
- **Job Description Matching**: Upload a JD to see exactly how well your resume fits the role.
- **Skill Gap Analysis**: Identifies missing critical skills required for the job.
- **Privacy First**: Runs entirely locally. Your personal data never leaves your machine.
- **Detailed Insights**: Provides specific, actionable recommendations to improve your score.

## 🛠️ Tech Stack

- **Backend**: Python (Flask), NLTK, scikit-learn, pdfplumber
- **Frontend**: React.js, Vite, CSS Modules
- **Analysis**: TF-IDF Vectorization, Cosine Similarity, Rule-based NLP

## 📦 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher

### 1. Clone the Repository
```bash
git clone https://github.com/shashwat-dev1/ats-resume-analyzer.git
cd ats-resume-analyzer
```

### 2. Setup Backend
```bash
cd backend
python -m venv venv
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Setup Frontend
```bash
cd ../frontend
npm install
```

## 🏃‍♂️ Running the Application

You need to run both the backend and frontend servers.

**Option 1: Using Helper Scripts (Windows)**
- Double-click `start-backend.bat`
- Double-click `start-frontend.bat`

**Option 2: Manual Start**

*Terminal 1 (Backend)*
```bash
cd backend
python app.py
```

*Terminal 2 (Frontend)*
```bash
cd frontend
npm run dev
```

Open your browser to `http://localhost:5173` to use the application.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

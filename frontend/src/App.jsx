import React, { useState } from 'react';
import axios from 'axios';
import FileUpload from './components/FileUpload';
import AnalysisProgress from './components/AnalysisProgress';
import ResultsDashboard from './components/ResultsDashboard';
import './index.css';

function App() {
  const [resumeFile, setResumeFile] = useState(null);
  const [jdFile, setJdFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleAnalyze = async () => {
    if (!resumeFile) {
      setError('Please upload a resume file');
      return;
    }

    setLoading(true);
    setError(null);
    setResults(null);

    const formData = new FormData();
    formData.append('resume', resumeFile);
    if (jdFile) {
      formData.append('job_description', jdFile);
    }

    try {
      const response = await axios.post('/api/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setResults(response.data);
    } catch (err) {
      console.error('Analysis error:', err);
      setError(
        err.response?.data?.error ||
        'Failed to analyze resume. Please try again.'
      );
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResumeFile(null);
    setJdFile(null);
    setResults(null);
    setError(null);
  };

  return (
    <div>
      {/* Header */}
      <header className="header">
        <div className="header-content">
          <h1>🎯 ATS Resume Analyzer</h1>
          <p>
            Upload your resume to get instant ATS compatibility insights and actionable recommendations
          </p>
        </div>
      </header>

      {/* Main Content */}
      <div className="container">
        {!results ? (
          <div className="card">
            <h2 style={{ marginBottom: '1.5rem' }}>Upload Documents</h2>

            {error && (
              <div className="alert alert-error">
                {error}
              </div>
            )}

            <FileUpload
              onFileSelect={setResumeFile}
              fileType="resume"
              label="Resume"
              required={true}
            />

            <FileUpload
              onFileSelect={setJdFile}
              fileType="jd"
              label="Job Description (Optional)"
              required={false}
            />

            <div style={{
              display: 'flex',
              gap: '1rem',
              marginTop: '1.5rem'
            }}>
              <button
                className="btn btn-primary"
                onClick={handleAnalyze}
                disabled={!resumeFile || loading}
              >
                {loading ? 'Analyzing...' : 'Analyze Resume'}
              </button>

              {(resumeFile || jdFile) && (
                <button
                  className="btn btn-secondary"
                  onClick={handleReset}
                  disabled={loading}
                >
                  Reset
                </button>
              )}
            </div>

            {loading && (
              <div style={{ marginTop: '2rem' }}>
                <AnalysisProgress />
              </div>
            )}
          </div>
        ) : (
          <div>
            <div style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              marginBottom: '2rem'
            }}>
              <h2>Analysis Results</h2>
              <button className="btn btn-secondary" onClick={handleReset}>
                Analyze New Resume
              </button>
            </div>

            <ResultsDashboard results={results} />
          </div>
        )}
      </div>

      {/* Footer */}
      <footer style={{
        textAlign: 'center',
        padding: '2rem',
        color: 'var(--text-secondary)',
        fontSize: '0.875rem'
      }}>
        <p>
          ATS Resume Analyzer - Created by Shashwat Jain
        </p>
      </footer>
    </div>
  );
}

export default App;

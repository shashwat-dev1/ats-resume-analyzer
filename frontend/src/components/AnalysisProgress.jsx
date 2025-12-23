import React from 'react';

const AnalysisProgress = () => {
    return (
        <div className="loading-container">
            <div className="spinner"></div>
            <div className="loading-text">
                Analyzing your resume... This may take a few moments.
            </div>
        </div>
    );
};

export default AnalysisProgress;

import React from 'react';

const ScoreDisplay = ({ score, label, interpretation, level }) => {
    const getScoreClass = () => {
        if (level === 'excellent') return 'success';
        if (level === 'good') return 'warning';
        if (level === 'fair') return 'warning';
        return 'danger';
    };

    return (
        <div className={`score-card ${getScoreClass()}`}>
            <div className="score-label">{label}</div>
            <div className="score-value">{Math.round(score)}</div>
            <div className="score-interpretation">{interpretation}</div>
        </div>
    );
};

export default ScoreDisplay;

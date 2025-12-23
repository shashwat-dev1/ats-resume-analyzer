import React from 'react';

const RecommendationsList = ({ recommendations }) => {
    if (!recommendations || recommendations.length === 0) {
        return (
            <div className="card">
                <h2 style={{ marginBottom: '1rem' }}>Recommendations</h2>
                <p style={{ color: 'var(--text-secondary)' }}>
                    Great job! No critical recommendations at this time.
                </p>
            </div>
        );
    }

    return (
        <div className="card">
            <h2 style={{ marginBottom: '1rem' }}>Recommendations</h2>
            <ul className="recommendations-list">
                {recommendations.map((rec, index) => (
                    <li key={index} className={`recommendation-item ${rec.priority}`}>
                        <div className={`recommendation-priority ${rec.priority}`}>
                            {rec.priority}
                        </div>
                        <div className="recommendation-message">{rec.message}</div>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default RecommendationsList;

import React from 'react';
import ScoreDisplay from './ScoreDisplay';
import SectionScoreCard from './SectionScoreCard';
import RecommendationsList from './RecommendationsList';

const ResultsDashboard = ({ results }) => {
    const {
        ats_score,
        jd_match_score,
        sections,
        skills,
        recommendations,
        strengths,
        summary,
        interpretations,
        jd_analysis
    } = results;

    return (
        <div>
            {/* Summary */}
            {summary && (
                <div className="alert alert-success" style={{ marginBottom: '2rem' }}>
                    <strong>Analysis Summary:</strong> {summary}
                </div>
            )}

            {/* Scores */}
            <div className="score-container">
                <ScoreDisplay
                    score={ats_score}
                    label="ATS Score"
                    interpretation={interpretations?.ats_interpretation || ''}
                    level={interpretations?.ats_level || 'fair'}
                />
                {jd_match_score !== undefined && (
                    <ScoreDisplay
                        score={jd_match_score}
                        label="JD Match"
                        interpretation={interpretations?.jd_interpretation || ''}
                        level={interpretations?.jd_level || 'fair'}
                    />
                )}
            </div>

            {/* Strengths */}
            {strengths && strengths.length > 0 && (
                <div className="card" style={{ marginBottom: '2rem' }}>
                    <h2 style={{ marginBottom: '1rem', color: 'var(--success-color)' }}>
                        ✓ Strengths
                    </h2>
                    <ul style={{ paddingLeft: '1.5rem' }}>
                        {strengths.map((strength, index) => (
                            <li key={index} style={{ marginBottom: '0.5rem', color: 'var(--text-primary)' }}>
                                {strength}
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            {/* Section Scores */}
            <div className="card" style={{ marginBottom: '2rem' }}>
                <h2 style={{ marginBottom: '1rem' }}>Section Analysis</h2>
                <div className="section-scores">
                    {Object.entries(sections).map(([sectionName, sectionData]) => (
                        <SectionScoreCard
                            key={sectionName}
                            sectionName={sectionName}
                            sectionData={sectionData}
                        />
                    ))}
                </div>
            </div>

            {/* Skills */}
            {skills && skills.found_skills && skills.found_skills.length > 0 && (
                <div className="card skills-container">
                    <h2 style={{ marginBottom: '1rem' }}>
                        Identified Skills ({skills.skill_count})
                    </h2>
                    <div className="skills-grid">
                        {skills.found_skills.slice(0, 20).map((skill, index) => (
                            <span key={index} className="skill-tag">
                                {skill}
                            </span>
                        ))}
                        {skills.found_skills.length > 20 && (
                            <span className="skill-tag" style={{ fontStyle: 'italic' }}>
                                +{skills.found_skills.length - 20} more
                            </span>
                        )}
                    </div>
                </div>
            )}

            {/* Missing Skills (JD Analysis) */}
            {jd_analysis && jd_analysis.missing_skills && jd_analysis.missing_skills.length > 0 && (
                <div className="card skills-container">
                    <h2 style={{ marginBottom: '1rem', color: 'var(--danger-color)' }}>
                        Missing Skills from Job Description
                    </h2>
                    <div className="skills-grid">
                        {jd_analysis.missing_skills.slice(0, 15).map((skill, index) => (
                            <span key={index} className="skill-tag missing">
                                {skill}
                            </span>
                        ))}
                    </div>
                </div>
            )}

            {/* Recommendations */}
            <RecommendationsList recommendations={recommendations} />
        </div>
    );
};

export default ResultsDashboard;

import React from 'react';

const SectionScoreCard = ({ sectionName, sectionData }) => {
    return (
        <div className="section-card">
            <div className="section-header">
                <div className="section-name">{sectionName}</div>
                <span className={`section-badge ${sectionData.present ? 'present' : 'missing'}`}>
                    {sectionData.present ? '✓ Present' : '✗ Missing'}
                </span>
            </div>
            <div className="section-observation">{sectionData.observation}</div>
        </div>
    );
};

export default SectionScoreCard;

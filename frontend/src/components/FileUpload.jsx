import React, { useState } from 'react';

const FileUpload = ({ onFileSelect, fileType, label, required = false }) => {
    const [file, setFile] = useState(null);
    const [dragOver, setDragOver] = useState(false);

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        if (selectedFile) {
            setFile(selectedFile);
            onFileSelect(selectedFile);
        }
    };

    const handleDrop = (e) => {
        e.preventDefault();
        setDragOver(false);
        const droppedFile = e.dataTransfer.files[0];
        if (droppedFile) {
            setFile(droppedFile);
            onFileSelect(droppedFile);
        }
    };

    const handleDragOver = (e) => {
        e.preventDefault();
        setDragOver(true);
    };

    const handleDragLeave = () => {
        setDragOver(false);
    };

    const handleRemove = () => {
        setFile(null);
        onFileSelect(null);
    };

    const formatFileSize = (bytes) => {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
    };

    return (
        <div style={{ marginBottom: '1.5rem' }}>
            <label style={{
                display: 'block',
                fontWeight: '600',
                marginBottom: '0.5rem',
                color: 'var(--text-primary)'
            }}>
                {label} {required && <span style={{ color: 'var(--danger-color)' }}>*</span>}
            </label>

            {!file ? (
                <div
                    className={`upload-area ${dragOver ? 'drag-over' : ''}`}
                    onDrop={handleDrop}
                    onDragOver={handleDragOver}
                    onDragLeave={handleDragLeave}
                    onClick={() => document.getElementById(`file-input-${fileType}`).click()}
                >
                    <div className="upload-icon">📄</div>
                    <div className="upload-text">
                        Click to upload or drag and drop
                    </div>
                    <div className="upload-hint">
                        PDF, DOCX {fileType === 'jd' ? 'or TXT' : ''} (Max 10MB)
                    </div>
                    <input
                        id={`file-input-${fileType}`}
                        type="file"
                        accept={fileType === 'jd' ? '.pdf,.docx,.doc,.txt' : '.pdf,.docx,.doc'}
                        onChange={handleFileChange}
                        style={{ display: 'none' }}
                    />
                </div>
            ) : (
                <div className="file-info">
                    <div>
                        <div className="file-name">📄 {file.name}</div>
                        <div className="file-size">{formatFileSize(file.size)}</div>
                    </div>
                    <button className="remove-file" onClick={handleRemove} title="Remove file">
                        ✕
                    </button>
                </div>
            )}
        </div>
    );
};

export default FileUpload;

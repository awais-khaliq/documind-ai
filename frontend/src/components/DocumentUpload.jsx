import React, { useRef, useState } from 'react';
import { Upload, Loader } from 'lucide-react';

export default function DocumentUpload({ onUpload }) {
  const [isDragging, setIsDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadFile, setUploadFile] = useState(null);
  const inputRef = useRef(null);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => setIsDragging(false);

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    if (file) processFile(file);
  };

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) processFile(file);
    e.target.value = '';
  };

  const processFile = async (file) => {
    const ext = file.name.split('.').pop().toLowerCase();
    const allowed = ['pdf', 'docx', 'txt'];
    if (!allowed.includes(ext)) {
      alert(`Unsupported file type: .${ext}\nAllowed: PDF, DOCX, TXT`);
      return;
    }

    setUploading(true);
    setUploadFile(file.name);
    setUploadProgress(0);

    // Simulate progress
    const progressInterval = setInterval(() => {
      setUploadProgress((prev) => {
        if (prev >= 90) {
          clearInterval(progressInterval);
          return 90;
        }
        return prev + Math.random() * 15;
      });
    }, 200);

    try {
      await onUpload(file);
      setUploadProgress(100);
      setTimeout(() => {
        setUploading(false);
        setUploadFile(null);
        setUploadProgress(0);
      }, 800);
    } catch (err) {
      clearInterval(progressInterval);
      setUploading(false);
      setUploadFile(null);
      setUploadProgress(0);
    }
  };

  return (
    <div className="upload-zone">
      <div
        className={`upload-dropzone ${isDragging ? 'dragover' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => !uploading && inputRef.current?.click()}
      >
        <div className="upload-icon">
          {uploading ? (
            <Loader size={20} className="spin" />
          ) : (
            <Upload size={20} />
          )}
        </div>
        <div className="upload-text">
          <strong>Drop files here</strong> or click to browse
        </div>
        <div className="upload-formats">PDF, DOCX, TXT • Max 50MB</div>
        <input
          ref={inputRef}
          type="file"
          className="upload-input"
          accept=".pdf,.docx,.txt"
          onChange={handleFileSelect}
        />
      </div>

      {uploading && (
        <div className="upload-progress">
          <div className="upload-progress-bar-track">
            <div
              className="upload-progress-bar-fill"
              style={{ width: `${uploadProgress}%` }}
            />
          </div>
          <div className="upload-progress-text">
            <Loader size={12} className="spin" />
            Processing {uploadFile}...
          </div>
        </div>
      )}
    </div>
  );
}

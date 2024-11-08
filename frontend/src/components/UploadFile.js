import React, { useState } from 'react';
import axios from 'axios';
import { Box, Button, TextField, Typography } from '@mui/material';

function UploadFile({ setExperimentId, onUploadComplete }) {
  const [file, setFile] = useState(null);
  const [experimentIdInput, setExperimentIdInput] = useState('');
  const [isUploaded, setIsUploaded] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file || !experimentIdInput) {
      alert('Please enter an experiment ID and select a file to upload');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      await axios.post(
        `http://localhost:8000/files/upload/${experimentIdInput}`,
        formData,
        { headers: { 'Content-Type': 'multipart/form-data' } }
      );
      setExperimentId(experimentIdInput);
      setIsUploaded(true);
      onUploadComplete(); // Notify parent that upload is done
      alert('File uploaded successfully!');
    } catch (error) {
      console.error('Error uploading file:', error);
      alert('File upload failed');
    }
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mb: 4 }}>
      <Typography variant="h6">Upload PDF</Typography>
      <TextField
        label="Experiment ID"
        variant="outlined"
        value={experimentIdInput}
        onChange={(e) => setExperimentIdInput(e.target.value)}
      />
      <Button variant="contained" component="label">
        Select File
        <input type="file" hidden onChange={handleFileChange} />
      </Button>
      <Button
        variant="contained"
        color="primary"
        onClick={handleUpload}
        disabled={!file || !experimentIdInput}
      >
        Upload
      </Button>
    </Box>
  );
}

export default UploadFile;

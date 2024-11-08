import React, { useState } from 'react';
import UploadFile from './components/UploadFile';
import ChatBot from './components/ChatBot';
import { Container, Typography } from '@mui/material';

function App() {
  const [experimentId, setExperimentId] = useState(null);
  const [startChat, setStartChat] = useState(false);

  const handleUploadComplete = () => {
    setStartChat(true);
  };

  return (
    <Container maxWidth="md">
      <Typography variant="h4" align="center" gutterBottom>
        Document-Based Chatbot
      </Typography>
      <UploadFile setExperimentId={setExperimentId} onUploadComplete={handleUploadComplete} />
      {startChat && experimentId && <ChatBot experimentId={experimentId} />}
    </Container>
  );
}

export default App;

import React, { useState } from 'react';
import axios from 'axios';
import { Box, Button, TextField, Typography, Paper, List, ListItem, ListItemText } from '@mui/material';

function ChatBot({ experimentId }) {
  const [question, setQuestion] = useState('');
  const [chatHistory, setChatHistory] = useState([]);

  const handleAskQuestion = async () => {
    if (!question) return;

    try {
      const response = await axios.post(
        `http://localhost:8000/search/answer/${experimentId}/${encodeURIComponent(question)}`
      );
      const answer = response.data.answer;
      setChatHistory([...chatHistory, { question, answer }]);
      setQuestion('');
    } catch (error) {
      console.error('Error getting answer:', error);
      alert('Failed to get answer');
    }
  };

  return (
    <Box sx={{ maxWidth: 600, mx: 'auto', mt: 4 }}>
      <Typography variant="h6" gutterBottom>Chat with Document Chatbot</Typography>
      <Paper variant="outlined" sx={{ p: 2, mb: 2, maxHeight: 300, overflow: 'auto' }}>
        <List>
          {chatHistory.map((entry, index) => (
            <ListItem key={index}>
              <ListItemText
                primary={`Q: ${entry.question}`}
                secondary={`A: ${entry.answer}`}
              />
            </ListItem>
          ))}
        </List>
      </Paper>
      <TextField
        label="Type your question"
        variant="outlined"
        fullWidth
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        onKeyPress={(e) => e.key === 'Enter' && handleAskQuestion()}
      />
      <Button variant="contained" color="primary" onClick={handleAskQuestion} sx={{ mt: 2 }}>
        Ask
      </Button>
    </Box>
  );
}

export default ChatBot;

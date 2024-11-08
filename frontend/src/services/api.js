import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export const uploadFile = (experimentId, formData) => {
  return axios.post(`${API_BASE_URL}/files/upload/${experimentId}`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const askQuestion = (experimentId, question) => {
  return axios.post(`${API_BASE_URL}/search/answer/${experimentId}/${encodeURIComponent(question)}`);
};

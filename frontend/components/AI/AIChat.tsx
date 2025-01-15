import React, { useState } from 'react';
import { Paper, TextField, Box, Typography, CircularProgress } from '@mui/material';

interface MessageType {
  type: 'user' | 'ai';
  content: string;
  data?: any;
}

const Message = ({ message }: { message: MessageType }) => {
  return (
    <Box sx={{ my: 1, p: 2, bgcolor: message.type === 'user' ? '#e0f7fa' : '#f5f5f5', borderRadius: '5px' }}>
      <Typography variant="body1" fontWeight="bold" color={message.type === 'user' ? 'primary' : 'secondary'}>
        {message.type === 'user' ? 'Usuario' : 'AI'}
      </Typography>
      <Typography variant="body2">{message.content}</Typography>
      {message.data && <pre>{JSON.stringify(message.data, null, 2)}</pre>}
    </Box>
  );
};

export const AIChat = () => {
  const [messages, setMessages] = useState<MessageType[]>([]);
  const [input, setInput] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);

  const handleSend = async (message: string) => {
    setIsProcessing(true);
    try {
      // Aquí deberías llamar al servicio de IA
      // const response = await AIService.processQuery(message);
      setMessages(prev => [...prev,
        { type: 'user', content: message },
        { type: 'ai', content: 'Respuesta de la IA', data: {}} // Placeholder
      ]);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <Box sx={{ height: '600px', display: 'flex', flexDirection: 'column' }}>
      <Paper sx={{ flex: 1, p: 2, overflow: 'auto' }}>
        {messages.map((msg, index) => (
          <Message key={index} message={msg} />
        ))}
      </Paper>
      <TextField
        fullWidth
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Pregunta sobre tus datos..."
        onKeyPress={(e) => e.key === 'Enter' && handleSend(input)}
        disabled={isProcessing}
        InputProps={{
          endAdornment: isProcessing ? <CircularProgress size={20} /> : null,
        }}
      />
    </Box>
  );
};

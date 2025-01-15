import React, { useState, useEffect, useContext } from 'react';
import { Box, LinearProgress, Typography } from '@mui/material';
import { DocumentService } from '../../frontend/src/services/api';
import { SnackbarContext } from '../../frontend/context/SnackbarContext';

export const ProcessingStatus = ({ documentId }: { documentId: string }) => {
  const [status, setStatus] = useState('processing');
  const [progress, setProgress] = useState(0);
  const { showSnackbar } = useContext(SnackbarContext);

  useEffect(() => {
    const checkStatus = async () => {
      try {
        const result = await DocumentService.getStatus(documentId);
        setStatus(result.data.status);
        setProgress(result.data.progress);
        if (result.data.status === 'completed') {
          showSnackbar('Document processed successfully', 'success');
        } else if (result.data.status === 'error') {
          showSnackbar('Error processing document', 'error');
        }
      } catch (error) {
        console.error("Error checking processing status:", error);
        setStatus('error');
        showSnackbar('Error checking document status', 'error');
      }
    };

    const interval = setInterval(checkStatus, 2000);
    return () => clearInterval(interval);
  }, [documentId, showSnackbar]);

  return (
    <Box>
      <LinearProgress variant="determinate" value={progress} />
      <Typography>{status}</Typography>
    </Box>
  );
};

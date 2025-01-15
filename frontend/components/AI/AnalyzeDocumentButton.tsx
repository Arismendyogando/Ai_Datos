import React, { useState } from 'react';
import { Button, CircularProgress } from '@mui/material';
import { DocumentService } from '../../src/services/api';
import { useNotify } from '../../hooks/useNotify';

interface AnalyzeDocumentButtonProps {
  documentId: string;
}

export const AnalyzeDocumentButton: React.FC<AnalyzeDocumentButtonProps> = ({ documentId }) => {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const notify = useNotify();

  const handleAnalyze = async () => {
    setIsAnalyzing(true);
    try {
      await DocumentService.analyze(documentId);
      notify.success('Document analyzed successfully');
    } catch (error: any) {
      notify.error(`Error analyzing document: ${error.message}`);
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <Button 
      variant="contained" 
      color="primary" 
      onClick={handleAnalyze} 
      disabled={isAnalyzing}
      startIcon={isAnalyzing ? <CircularProgress size={20} /> : null}
    >
      {isAnalyzing ? 'Analyzing...' : 'Analyze Document'}
    </Button>
  );
};

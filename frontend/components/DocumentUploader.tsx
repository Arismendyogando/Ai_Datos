import React, { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { Button, IconButton, Typography, Box, CircularProgress, LinearProgress } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import DeleteIcon from '@mui/icons-material/Delete';
import { DocumentService } from '../src/services/api';
import { useNotify } from '../hooks/useNotify';
import { FilePreview } from './FilePreview';
import { useAIContext } from '../context/AIContext';

// Constantes configurables
const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
const ALLOWED_MIME_TYPES = ['image/jpeg', 'image/png', 'application/pdf'];

interface DocumentUploaderProps {
  onUploadSuccess?: (documentId: string) => void;
  selectedTemplate?: string;
}

export const DocumentUploader = ({ onUploadSuccess, selectedTemplate }: DocumentUploaderProps) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const notify = useNotify();
  const { requestAnalysis } = useAIContext();

  const { mutate: uploadFile, isPending: isUploading } = useMutation({
    mutationFn: async (file: File) => {
      const formData = new FormData();
      formData.append('file', file);
      if (selectedTemplate) {
        formData.append('templateId', selectedTemplate);
      }

      return await DocumentService.upload(formData, {
        onUploadProgress: (progressEvent) => {
          if (progressEvent.lengthComputable) {
            const percentCompleted = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            );
            setUploadProgress(percentCompleted);
          }
        },
      });
    },
    onSuccess: async (response, file) => {
      notify.success(`Archivo "${file.name}" subido con éxito`);
      
      try {
        await requestAnalysis(response.data.document_id);
      } catch (error) {
        notify.error('Error en el análisis del documento');
      }
      
      onUploadSuccess?.(response.data.document_id);
      setSelectedFile(null);
      setUploadProgress(0);
    },
    onError: (error: Error, file) => {
      notify.error(`Error al subir el archivo "${file.name}": ${error.message}`);
      setUploadProgress(0);
    },
  });  });  );  // ... rest of your code
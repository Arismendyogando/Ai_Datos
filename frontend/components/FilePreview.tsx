import React from 'react';
import { Box, Typography } from '@mui/material';
import PictureAsPdfIcon from '@mui/icons-material/PictureAsPdf';
import Image from 'next/image';

interface FilePreviewProps {
  file: File;
}

export const FilePreview = ({ file }: FilePreviewProps) => {
  const isImage = file.type.startsWith('image/');
  const previewUrl = URL.createObjectURL(file);

  return (
    <Box
      sx={{
        border: '1px solid',
        borderColor: 'divider',
        borderRadius: 1,
        p: 2,
        mt: 2,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        height: 200,
        overflow: 'hidden',
        position: 'relative'
      }}
      aria-label="Vista previa del archivo"
    >
      {isImage ? (
        <Image
          src={previewUrl}
          alt={`Vista previa de ${file.name}`}
          fill
          style={{ objectFit: 'contain' }}
          unoptimized
        />
      ) : (
        <Box textAlign="center">
          <PictureAsPdfIcon sx={{ fontSize: 64, color: 'text.secondary' }} />
          <Typography variant="caption" display="block">
            Vista previa no disponible para PDF
          </Typography>
        </Box>
      )}
    </Box>
  );
};
import React, { useState } from 'react';
import { Button, Typography } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import GoogleDriveIcon from '@mui/icons-material/Google';
import { useAIContext } from '../../context/AIContext';

const FileUploader = ({ onFileSelect }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const { setLoading } = useAIContext();

  const handleLocalUpload = (event) => {
    const file = event.target.files[0];
    if (validateFile(file)) {
      setSelectedFile(file);
      onFileSelect(file);
    }
  };

  const handleGoogleDriveUpload = async () => {
    try {
      setLoading(true);
      // Implementar integración con Google Drive API
      const file = await selectFromGoogleDrive();
      if (validateFile(file)) {
        setSelectedFile(file);
        onFileSelect(file);
      }
    } catch (error) {
      console.error('Error selecting from Google Drive:', error);
    } finally {
      setLoading(false);
    }
  };

  const validateFile = (file) => {
    const allowedTypes = ['application/pdf', 'image/jpeg', 'image/png'];
    if (!allowedTypes.includes(file.type)) {
      alert('Tipo de archivo no soportado');
      return false;
    }
    if (file.size > 10 * 1024 * 1024) { // 10MB
      alert('El archivo es demasiado grande');
      return false;
    }
    return true;
  };

  return (
    <div className="file-uploader-container">
      <Typography variant="h6" gutterBottom>
        Seleccione su factura
      </Typography>
      
      <input
        accept=".pdf,.jpg,.jpeg,.png"
        style={{ display: 'none' }}
        id="local-upload"
        type="file"
        onChange={handleLocalUpload}
      />
      <label htmlFor="local-upload">
        <Button
          variant="contained"
          component="span"
          startIcon={<CloudUploadIcon />}
          sx={{ mr: 2 }}
        >
          Desde mi computadora
        </Button>
      </label>

      <Button
        variant="contained"
        color="secondary"
        startIcon={<GoogleDriveIcon />}
        onClick={handleGoogleDriveUpload}
      >
        Desde Google Drive
      </Button>

      {selectedFile && (
        <Typography variant="body1" sx={{ mt: 2 }}>
          Archivo seleccionado: {selectedFile.name}
        </Typography>
      )}
    </div>
  );
};

export default FileUploader;

import { loadGoogleDriveAPI, selectFileFromGoogleDrive } from '../../lib/googleDriveConfig';

// Función para obtener archivo desde Google Drive
async function selectFromGoogleDrive() {
  try {
    // 1. Inicializar API
    await loadGoogleDriveAPI();
    
    // 2. Mostrar selector de archivos
    const fileId = await selectFileFromGoogleDrive();
    if (!fileId) {
      throw new Error('No se seleccionó ningún archivo');
    }
    
    // 3. Obtener metadatos del archivo
    const response = await window.gapi.client.drive.files.get({
      fileId,
      fields: 'name,mimeType,size,createdTime,modifiedTime'
    });
    
    // 4. Validar credenciales y permisos
    if (!response || !response.result) {
      throw new Error('No se pudo obtener la información del archivo');
    }
    
    // 5. Validar tipo y tamaño del archivo
    const allowedTypes = ['application/pdf', 'image/jpeg', 'image/png'];
    if (!allowedTypes.includes(response.result.mimeType)) {
      throw new Error('Tipo de archivo no soportado');
    }
    if (response.result.size > 10 * 1024 * 1024) { // 10MB
      throw new Error('El archivo es demasiado grande');
    }
    
    // 6. Retornar objeto de archivo
    return {
      id: fileId,
      name: response.result.name,
      type: response.result.mimeType,
      size: response.result.size,
      created: response.result.createdTime,
      modified: response.result.modifiedTime
    };
    
  } catch (error) {
    console.error('Error en Google Drive:', error);
    throw new Error(`Error al seleccionar archivo: ${error.message}`);
  }
}

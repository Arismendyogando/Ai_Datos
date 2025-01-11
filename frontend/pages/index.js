import { useState } from 'react';
import { Box, Paper, Typography, Container } from '@mui/material';
import { motion } from 'framer-motion';
import FileUploader from '../components/Upload/FileUploader';
import EditableDataGrid from '../components/DataGrid/EditableDataGrid';

export default function Home() {
  const [processedData, setProcessedData] = useState(null);

  const handleFileProcessed = (result) => {
    if (result && result.data) {
      setProcessedData(Array.isArray(result.data) ? result.data : [result.data]);
    }
  };

  const handleDataChange = (newData) => {
    setProcessedData(newData);
  };

  return (
    <Container maxWidth="xl">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <Box sx={{ mb: 4 }}>
          <Typography variant="h4" component="h1" gutterBottom align="center">
            Procesamiento Inteligente de Facturas
          </Typography>
          <Typography variant="subtitle1" color="text.secondary" align="center" gutterBottom>
            Sube tus facturas y obtén datos estructurados en segundos
          </Typography>
        </Box>

        <Paper 
          elevation={3} 
          sx={{ 
            p: 3, 
            mb: 4,
            backgroundColor: 'background.paper',
            borderRadius: 2
          }}
        >
          <FileUploader onFileProcessed={handleFileProcessed} />
        </Paper>

        {processedData && (
          <Paper 
            elevation={3} 
            sx={{ 
              p: 3,
              backgroundColor: 'background.paper',
              borderRadius: 2
            }}
          >
            <Typography variant="h6" gutterBottom>
              Datos Extraídos
            </Typography>
            <EditableDataGrid 
              data={processedData}
              onDataChange={handleDataChange}
            />
          </Paper>
        )}
      </motion.div>
    </Container>
  );
}

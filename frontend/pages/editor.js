import { useState, useEffect } from 'react';
import { Box, Typography, Container, Paper } from '@mui/material';
import { motion } from 'framer-motion';
import EditableDataGrid from '../components/DataGrid/EditableDataGrid';

export default function Editor() {
  const [savedData, setSavedData] = useState(null);

  useEffect(() => {
    // TODO: Cargar datos guardados del almacenamiento local o backend
    const loadSavedData = () => {
      const data = localStorage.getItem('processedInvoices');
      if (data) {
        setSavedData(JSON.parse(data));
      }
    };
    loadSavedData();
  }, []);

  const handleDataChange = (newData) => {
    setSavedData(newData);
    // TODO: Guardar cambios en almacenamiento local o backend
    localStorage.setItem('processedInvoices', JSON.stringify(newData));
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
            Editor de Datos
          </Typography>
          <Typography variant="subtitle1" color="text.secondary" align="center" gutterBottom>
            Revisa y edita los datos extraídos de tus facturas
          </Typography>
        </Box>

        <Paper 
          elevation={3} 
          sx={{ 
            p: 3,
            backgroundColor: 'background.paper',
            borderRadius: 2
          }}
        >
          {savedData ? (
            <EditableDataGrid 
              data={savedData}
              onDataChange={handleDataChange}
            />
          ) : (
            <Box sx={{ p: 3, textAlign: 'center' }}>
              <Typography color="text.secondary">
                No hay datos disponibles para editar. Procesa algunas facturas primero.
              </Typography>
            </Box>
          )}
        </Paper>
      </motion.div>
    </Container>
  );
}

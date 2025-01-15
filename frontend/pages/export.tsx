import React, { useState } from 'react';
import { Grid, Container } from '@mui/material';
import { ExportCard } from '../components/ExportCard';
import { ExportService } from '../src/services/api';
import { useNotify } from '../hooks/useNotify';
import ExcelIcon from '@mui/icons-material/Assessment';
import CloudIcon from '@mui/icons-material/Cloud';

interface ExportPageProps {}

const ExportPage: React.FC<ExportPageProps> = () => {
  const [exportingExcel, setExportingExcel] = useState(false);
  const [exportingSheets, setExportingSheets] = useState(false);
  const notify = useNotify();

  const handleExport = async (type: 'excel' | 'sheets') => {
    const setLoading = type === 'excel' ? setExportingExcel : setExportingSheets;
    setLoading(true);
    
    try {
      await ExportService[`to${type.charAt(0).toUpperCase() + type.slice(1)}`]({});
      notify.success(`Exportación a ${type} exitosa`);
    } catch (error: any) {
      notify.error(`Error en exportación a ${type}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="lg">
      <Grid container spacing={4}>
        <Grid item xs={12} md={6}>
          <ExportCard
            title="Exportar a Excel"
            description="Descarga tus datos en formato Excel"
            icon={ExcelIcon}
            onExport={() => handleExport('excel')}
            isLoading={exportingExcel}
          />
        </Grid>
        <Grid item xs={12} md={6}>
          <ExportCard
            title="Exportar a Google Sheets"
            description="Sincroniza con Google Sheets"
            icon={CloudIcon}
            onExport={() => handleExport('sheets')}
            isLoading={exportingSheets}
          />
        </Grid>
      </Grid>
    </Container>
  );
};

export default ExportPage;

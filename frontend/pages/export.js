import { useEffect, useState } from 'react';
import {
  Box,
  Typography,
  Container,
  Paper,
  Button,
  Grid,
  Card,
  CardContent,
  CardActions,
} from '@mui/material';
import {
  CloudDownload as DownloadIcon,
  Google as GoogleIcon,
  TableChart as ExcelIcon,
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import toast from 'react-hot-toast';
import * as XLSX from 'xlsx';
import { google } from 'googleapis';
import credentials from '@/config/gcp_credentials/ai-datos@ai-datos.iam.gserviceaccount.com-20250108202111.json';
import useInvoiceStore from '../lib/store';

export default function Export() {
  const { processedInvoices, setProcessedInvoices } = useInvoiceStore();
  const [exportingExcel, setExportingExcel] = useState(false);
  const [exportingSheets, setExportingSheets] = useState(false);

  useEffect(() => {
    const loadSavedData = () => {
      const data = localStorage.getItem('processedInvoices');
      if (data) {
        setProcessedInvoices(JSON.parse(data));
      }
    };
    loadSavedData();
  }, [setProcessedInvoices]);

  const handleExportExcel = async () => {
    if (!processedInvoices?.length) {
      toast.error('No hay datos para exportar');
      return;
    }

    setExportingExcel(true);
    try {
      const workbook = XLSX.utils.book_new();
      const worksheetData = [
        Object.keys(processedInvoices[0]), // Headers
        ...processedInvoices.map(item => Object.values(item)), // Data rows
      ];
      const worksheet = XLSX.utils.aoa_to_sheet(worksheetData);
      XLSX.utils.book_append_sheet(workbook, worksheet, 'Invoices');
      XLSX.writeFile(workbook, 'invoices.xlsx');
      toast.success('Datos exportados a Excel correctamente');
    } catch (error) {
      toast.error('Error al exportar a Excel');
      console.error('Error exporting to Excel:', error);
    } finally {
      setExportingExcel(false);
    }
  };

  const handleExportGoogleSheets = async () => {
    if (!processedInvoices?.length) {
      toast.error('No hay datos para exportar');
      return;
    }

    setExportingSheets(true);
    try {
      // Authenticate with Google Sheets API using service account credentials
      const authClient = new google.auth.GoogleAuth({
        credentials,
        scopes: ['https://www.googleapis.com/auth/spreadsheets'],
      });
      const auth = await authClient.getClient();
      const sheets = google.sheets({ version: 'v4', auth });

      const spreadsheet = await sheets.spreadsheets.create({
        properties: {
          title: 'Invoice Data Export',
        },
      });
      const spreadsheetId = spreadsheet.data.spreadsheetId;
      const values = [
        Object.keys(processedInvoices[0]),
        ...processedInvoices.map(item => Object.values(item)),
      ];
      await sheets.spreadsheets.values.update({
        spreadsheetId,
        range: 'Sheet1',
        valueInputOption: 'USER_ENTERED',
        resource: { values },
      });
      toast.success('Datos exportados a Google Sheets correctamente');
      console.log(`Spreadsheet URL: https://docs.google.com/spreadsheets/d/${spreadsheetId}`);
    } catch (error) {
      toast.error('Error al exportar a Google Sheets');
      console.error('Error exporting to Google Sheets:', error);
    } finally {
      setExportingSheets(false);
    }
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <Typography variant="h4" component="h1" gutterBottom>
          Exportar Datos
        </Typography>

        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <motion.div whileHover={{ scale: 1.02 }} transition={{ duration: 0.2 }}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Exportar a Excel
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Descarga los datos en formato Excel (.xlsx)
                  </Typography>
                </CardContent>
                <CardActions>
                  <Button
                    variant="contained"
                    startIcon={<ExcelIcon />}
                    onClick={handleExportExcel}
                    disabled={!processedInvoices?.length || exportingExcel}
                  >
                    {exportingExcel ? 'Exportando...' : 'Exportar a Excel'}
                  </Button>
                </CardActions>
              </Card>
            </motion.div>
          </Grid>

          <Grid item xs={12} md={6}>
            <motion.div whileHover={{ scale: 1.02 }} transition={{ duration: 0.2 }}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Exportar a Google Sheets
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Exporta los datos directamente a Google Sheets
                  </Typography>
                </CardContent>
                <CardActions>
                  <Button
                    variant="contained"
                    startIcon={<GoogleIcon />}
                    onClick={handleExportGoogleSheets}
                    disabled={!processedInvoices?.length || exportingSheets}
                  >
                    {exportingSheets ? 'Exportando...' : 'Exportar a Google Sheets'}
                  </Button>
                </CardActions>
              </Card>
            </motion.div>
          </Grid>
        </Grid>

        {!processedInvoices?.length && (
          <Paper sx={{ mt: 4, p: 3, textAlign: 'center' }}>
            <Typography color="text.secondary">
              No hay datos disponibles para exportar. Procesa algunas facturas primero.
            </Typography>
          </Paper>
        )}
      </motion.div>
    </Container>
  );
}

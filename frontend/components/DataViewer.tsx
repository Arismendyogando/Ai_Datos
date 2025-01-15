import React from 'react';
import { DataGrid, GridColDef, GridRowsProp } from '@mui/x-data-grid';
import { Box, Toolbar, Button } from '@mui/material';

interface DataViewerProps {
  data: GridRowsProp;
  onApprove?: (selectedRows: GridRowsProp) => void;
  onEdit?: (newCellValues: any) => void;
}

export const DataViewer: React.FC<DataViewerProps> = ({ data, onApprove, onEdit }) => {
  const columns: GridColDef[] = [
    { field: 'date', headerName: 'Fecha', width: 130 },
    { field: 'concept', headerName: 'Concepto', width: 200, editable: true },
    { field: 'amount', headerName: 'Monto', width: 130, editable: true },
    // ... más columnas según necesidad
  ];

  return (
    <Box sx={{ height: 400, width: '100%' }}>
      <DataGrid
        rows={data}
        columns={columns}
        initialState={{
          pagination: {
            paginationModel: {
              pageSize: 5,
            },
          },
        }}
        checkboxSelection
        disableRowSelectionOnClick
        processRowUpdate={onEdit}
      />
      {onApprove && (
        <Toolbar>
          <Button color="primary" onClick={() => {
            const selectedRows = data.filter(row => row.isSelected);
            onApprove(selectedRows);
          }}>
            Aprobar Seleccionados
          </Button>
        </Toolbar>
      )}
    </Box>
  );
};

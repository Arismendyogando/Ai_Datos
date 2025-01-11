import { useState, useMemo, useCallback } from 'react';
import {
  Box,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  IconButton,
  Tooltip,
  Button,
  TableSortLabel,
} from '@mui/material';
import {
  Check as CheckIcon,
  Close as CloseIcon,
  Edit as EditIcon,
  Download as DownloadIcon,
  Replay as ReplayIcon,
  MoreVert as MoreVertIcon,
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';
import toast from 'react-hot-toast';
import { Draggable, DragDropContext, Droppable } from 'react-beautiful-dnd';

const getItemStyle = (isRowDragging, draggableStyle) => ({
  // some basic default styles to make things a bit more visually appealing
  userSelect: 'none',
  padding: grid * 2,
  margin: `0 0 ${grid}px 0`,

  // change background colour if dragging
  background: isRowDragging ? 'lightgreen' : 'grey',

  // styles we need to apply on draggables
  ...draggableStyle
});

const getListStyle = (isColumnDraggingOver) => ({
  background: isColumnDraggingOver ? 'lightblue' : 'lightgrey',
  padding: 8,
  width: 250,
});

export default function EditableDataGrid({ data, onDataChange, onDiscardRow }) {
  const [editingCell, setEditingCell] = useState(null);
  const [editValue, setEditValue] = useState('');
  const [approvedRows, setApprovedRows] = useState(new Set());
  const [gridData, setGridData] = useState(data);
  const [columnVisibility, setColumnVisibility] = useState(() => {
    if (!data || data.length === 0) return {};
    return Object.keys(data[0]).reduce((acc, key) => ({ ...acc, [key]: true }), {});
  });
  const [columnOrder, setColumnOrder] = useState(() => {
    if (!data || data.length === 0) return [];
    return Object.keys(data[0]);
  });
  const [columnHeaders, setColumnHeaders] = useState(() => {
    if (!data || data.length === 0) return {};
    return Object.keys(data[0]).reduce((acc, key) => ({
      ...acc,
      [key]: key.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' '),
    }), {});
  });
  const [editingHeader, setEditingHeader] = useState(null);
  const [editHeaderValue, setEditHeaderValue] = useState('');

  const columns = useMemo(() => {
    return columnOrder.filter(key => columnVisibility[key]).map(key => ({
      id: key,
      header: columnHeaders[key],
      accessor: key,
    }));
  }, [columnOrder, columnVisibility, columnHeaders]);

  const handleEditClick = (rowIndex, columnId, value) => {
    setEditingCell({ rowIndex, columnId });
    setEditValue(value);
  };

  const handleEditCancel = () => {
    setEditingCell(null);
    setEditValue('');
  };

  const handleEditSave = (rowIndex, columnId) => {
    const newData = [...gridData];
    newData[rowIndex] = {
      ...newData[rowIndex],
      [columnId]: editValue,
    };
    setGridData(newData);
    onDataChange(newData);
    setEditingCell(null);
    setEditValue('');
    toast.success('Dato actualizado correctamente');
  };

  const handleRowApproval = (rowIndex) => {
    const newApprovedRows = new Set(approvedRows);
    if (newApprovedRows.has(rowIndex)) {
      newApprovedRows.delete(rowIndex);
    } else {
      newApprovedRows.add(rowIndex);
    }
    setApprovedRows(newApprovedRows);
    toast.success(newApprovedRows.has(rowIndex) ? 'Fila aprobada' : 'Aprobación removida');
  };

  const handleDiscardRow = (rowIndex) => {
    const rowToDiscard = gridData[rowIndex];
    onDiscardRow(rowToDiscard);
    const newData = gridData.filter((_, index) => index !== rowIndex);
    setGridData(newData);
    toast.success('Fila descartada');
  };

  const handleReconfigureRow = (rowIndex) => {
    const rowToReconfigure = gridData[rowIndex];
    onDiscardRow(rowToReconfigure, true); // Indicate it's for reconfig
    const newData = gridData.filter((_, index) => index !== rowIndex);
    setGridData(newData);
    toast.info('Fila marcada para reconfiguración');
  };

  const handleExportExcel = () => {
    const approvedData = gridData.filter((_, index) => approvedRows.has(index));
    if (approvedData.length === 0) {
      toast.error('No hay filas aprobadas para exportar');
      return;
    }
    
    // TODO: Implementar exportación a Excel
    toast.info('Exportación a Excel en desarrollo');
  };

  const handleExportGoogleSheets = () => {
    // TODO: Implementar exportación a Google Sheets
    toast.info('Exportación a Google Sheets en desarrollo');
  };

  const onDragEnd = (result) => {
    if (!result.destination) {
      return;
    }

    const items = Array.from(columnOrder);
    const [reorderedItem] = items.splice(result.source.index, 1);
    items.splice(result.destination.index, 0, reorderedItem);

    setColumnOrder(items);
  };

  const handleHeaderEditClick = (columnId, headerValue) => {
    setEditingHeader(columnId);
    setEditHeaderValue(headerValue);
  };

  const handleHeaderEditCancel = () => {
    setEditingHeader(null);
    setEditHeaderValue('');
  };

  const handleHeaderEditSave = (columnId) => {
    setColumnHeaders(prevHeaders => ({
      ...prevHeaders,
      [columnId]: editHeaderValue,
    }));
    setEditingHeader(null);
    setEditHeaderValue('');
    toast.success('Encabezado actualizado correctamente');
  };

  if (!gridData || gridData.length === 0) {
    return (
      <Box sx={{ p: 3, textAlign: 'center' }}>
        No hay datos para mostrar
      </Box>
    );
  }

  return (
    <Box sx={{ width: '100%', display: 'flex' }}>
      <Box sx={{ flexGrow: 1 }}>
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3 }}
        >
          <Box sx={{ mb: 2, display: 'flex', gap: 2 }}>
            <Button
              variant="contained"
              startIcon={<DownloadIcon />}
              onClick={handleExportExcel}
              disabled={approvedRows.size === 0}
            >
              Exportar a Excel
            </Button>
            <Button
              variant="contained"
              startIcon={<DownloadIcon />}
              onClick={handleExportGoogleSheets}
              disabled={approvedRows.size === 0}
            >
              Exportar a Google Sheets
            </Button>
          </Box>

          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Acciones</TableCell>
                  {columns.map(column => (
                    <TableCell key={column.id}>
                      {editingHeader === column.id ? (
                        <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
                          <TextField
                            value={editHeaderValue}
                            onChange={(e) => setEditHeaderValue(e.target.value)}
                            size="small"
                            autoFocus
                          />
                          <IconButton
                            size="small"
                            color="primary"
                            onClick={() => handleHeaderEditSave(column.id)}
                            aria-label="Guardar encabezado"
                          >
                            <CheckIcon />
                          </IconButton>
                          <IconButton
                            size="small"
                            color="error"
                            onClick={handleHeaderEditCancel}
                            aria-label="Cancelar edición de encabezado"
                          >
                            <CloseIcon />
                          </IconButton>
                        </Box>
                      ) : (
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <TableSortLabel>{column.header}</TableSortLabel>
                          <Tooltip title="Editar encabezado">
                            <IconButton
                              size="small"
                              onClick={() => handleHeaderEditClick(column.id, column.header)}
                              aria-label="Editar encabezado"
                            >
                              <EditIcon />
                            </IconButton>
                          </Tooltip>
                        </Box>
                      )}
                    </TableCell>
                  ))}
                </TableRow>
              </TableHead>
              <TableBody>
                {gridData.map((row, rowIndex) => (
                  <TableRow
                    key={rowIndex}
                    sx={{
                      backgroundColor: approvedRows.has(rowIndex) ? 'action.selected' : 'inherit',
                    }}
                  >
                    <TableCell>
                      <IconButton
                        color={approvedRows.has(rowIndex) ? 'success' : 'default'}
                        onClick={() => handleRowApproval(rowIndex)}
                        aria-label={approvedRows.has(rowIndex) ? 'Desaprobar' : 'Aprobar'}
                      >
                        <CheckIcon />
                      </IconButton>
                      <IconButton
                        color="warning"
                        onClick={() => handleReconfigureRow(rowIndex)}
                        aria-label="Reconfigurar"
                      >
                        <ReplayIcon />
                      </IconButton>
                      <IconButton
                        color="error"
                        onClick={() => handleDiscardRow(rowIndex)}
                        aria-label="Descartar"
                      >
                        <CloseIcon />
                      </IconButton>
                    </TableCell>
                    {columns.map(column => (
                      <TableCell key={column.id}>
                        {editingCell?.rowIndex === rowIndex && editingCell?.columnId === column.id ? (
                          <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
                            <TextField
                              value={editValue}
                              onChange={(e) => setEditValue(e.target.value)}
                              size="small"
                              autoFocus
                            />
                            <IconButton
                              size="small"
                              color="primary"
                              onClick={() => handleEditSave(rowIndex, column.id)}
                              aria-label="Guardar"
                            >
                              <CheckIcon />
                            </IconButton>
                            <IconButton
                              size="small"
                              color="error"
                              onClick={handleEditCancel}
                              aria-label="Cancelar"
                            >
                              <CloseIcon />
                            </IconButton>
                          </Box>
                        ) : (
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            {row[column.id]}
                            <Tooltip title="Editar">
                              <IconButton
                                size="small"
                                onClick={() => handleEditClick(rowIndex, column.id, row[column.id])}
                                aria-label="Editar"
                              >
                                <EditIcon />
                              </IconButton>
                            </Tooltip>
                          </Box>
                        )}
                      </TableCell>
                    ))}
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </motion.div>
      </Box>
      <DragDropContext onDragEnd={onDragEnd}>
        <Droppable droppableId="columnList">
          {(provided, snapshot) => (
            <Box
              ref={provided.innerRef}
              style={getListStyle(snapshot.isColumnDraggingOver)}
              {...provided.droppableProps}
            >
              {columnOrder.map((columnId, index) => (
                <Draggable key={columnId} draggableId={columnId} index={index}>
                  {(provided, snapshot) => (
                    <div
                      ref={provided.innerRef}
                      {...provided.draggableProps}
                      {...provided.dragHandleProps}
                      style={getItemStyle(snapshot.isRowDragging, provided.draggableProps.style)}
                    >
                      {columnHeaders[columnId]}
                    </div>
                  )}
                </Draggable>
              ))}
              {provided.placeholder}
            </Box>
          )}
        </Droppable>
      </DragDropContext>
    </Box>
  );
}

import React, { useState } from 'react';
import { TextField, Button, Select, MenuItem, FormControl, InputLabel, Box, Typography } from '@mui/material';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';

const initialFields = [
  { id: '1', name: 'Fecha', type: 'date' },
  { id: '2', name: 'Concepto', type: 'text' },
  { id: '3', name: 'Monto', type: 'number' },
];

const TemplateBuilder = () => {
  const [templateName, setTemplateName] = useState('');
  const [fields, setFields] = useState(initialFields);
  const [selectedFields, setSelectedFields] = useState([]);

  const handleDragEnd = (result) => {
    if (!result.destination) {
      return;
    }

    if (result.source.droppableId === "availableFields" && result.destination.droppableId === "selectedFields") {
      const fieldToAdd = fields.find(field => field.id === result.draggableId);
      setSelectedFields([...selectedFields, fieldToAdd]);
    } else if (result.source.droppableId === "selectedFields" && result.destination.droppableId === "availableFields") {
      const filteredFields = selectedFields.filter(field => field.id !== result.draggableId);
      setSelectedFields(filteredFields);
    }
  };

  const handleSaveTemplate = () => {
    console.log("Saving template:", { name: templateName, fields: selectedFields });
    // Aquí se implementaría la lógica para guardar la plantilla
  };

  return (
    <DragDropContext onDragEnd={handleDragEnd}>
      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, p: 3 }}>
        <Typography variant="h6">Nombre de la Plantilla</Typography>
        <TextField
          fullWidth
          value={templateName}
          onChange={(e) => setTemplateName(e.target.value)}
        />

        <Box sx={{ display: 'flex', gap: 3 }}>
          <Box flex={1}>
            <Typography variant="subtitle1">Campos Disponibles</Typography>
            <Droppable droppableId="availableFields">
              {(provided) => (
                <Box {...provided.droppableProps} ref={provided.innerRef} sx={{ border: '1px solid #ccc', minHeight: 100, p: 2 }}>
                  {fields.map((field, index) => (
                    <Draggable key={field.id} draggableId={field.id} index={index}>
                      {(provided) => (
                        <Box
                          {...provided.draggableProps}
                          {...provided.dragHandleProps}
                          ref={provided.innerRef}
                          sx={{ p: 1, m: 1, border: '1px solid #eee', bgcolor: '#f9f9f9' }}
                        >
                          {field.name}
                        </Box>
                      )}
                    </Draggable>
                  ))}
                  {provided.placeholder}
                </Box>
              )}
            </Droppable>
          </Box>

          <Box flex={1}>
            <Typography variant="subtitle1">Campos Seleccionados</Typography>
            <Droppable droppableId="selectedFields">
              {(provided) => (
                <Box {...provided.droppableProps} ref={provided.innerRef} sx={{ border: '1px solid #ccc', minHeight: 100, p: 2 }}>
                  {selectedFields.map((field, index) => (
                    <Draggable key={field.id} draggableId={field.id} index={index}>
                      {(provided) => (
                        <Box
                          {...provided.draggableProps}
                          {...provided.dragHandleProps}
                          ref={provided.innerRef}
                          sx={{ p: 1, m: 1, border: '1px solid #eee', bgcolor: '#e0e0e0' }}
                        >
                          {field.name}
                        </Box>
                      )}
                    </Draggable>
                  ))}
                  {provided.placeholder}
                </Box>
              )}
            </Droppable>
          </Box>
        </Box>

        <Button variant="contained" color="primary" onClick={handleSaveTemplate}>
          Guardar Plantilla
        </Button>
      </Box>
    </DragDropContext>
  );
};

export default TemplateBuilder;

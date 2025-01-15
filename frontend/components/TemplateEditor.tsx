import React, { useState } from 'react';
import {
  Box,
  TextField,
  Button,
  IconButton,
  List,
  ListItem,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Switch,
  FormControlLabel
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import DeleteIcon from '@mui/icons-material/Delete';

interface Field {
  name: string;
  type: string;
  required: boolean;
}

interface TemplateEditorProps {
  template: Template;
  onSave: (template: Template) => void;
  onCancel: () => void;
}

export const TemplateEditor = ({ template, onSave, onCancel }: TemplateEditorProps) => {
  const [editingTemplate, setEditingTemplate] = useState(template);
  const [newField, setNewField] = useState<Field>({ name: '', type: 'text', required: false });

  const handleAddField = () => {
    setEditingTemplate({
      ...editingTemplate,
      fields: [...editingTemplate.fields, newField]
    });
    setNewField({ name: '', type: 'text', required: false });
  };

  return (
    <Box p={2}>
      <TextField
        fullWidth
        label="Nombre de la Plantilla"
        value={editingTemplate.name}
        onChange={(e) => setEditingTemplate({...editingTemplate, name: e.target.value})}
        margin="normal"
      />

      <List>
        {editingTemplate.fields.map((field, index) => (
          <ListItem key={index}>
            {/* Campo existente */}
          </ListItem>
        ))}
      </List>

      <Box mt={2}>
        <Button 
          variant="contained" 
          color="primary" 
          onClick={() => onSave(editingTemplate)}
        >
          Guardar Plantilla
        </Button>
        <Button 
          variant="outlined" 
          onClick={onCancel}
          sx={{ ml: 1 }}
        >
          Cancelar
        </Button>
      </Box>
    </Box>
  );
};

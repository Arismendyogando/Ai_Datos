import React, { useState } from 'react';
import { 
  Box, 
  Button, 
  TextField,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  IconButton
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import { useAIContext } from '../context/AIContext';

// El resto del código permanece igual...
interface Template {
  id: string;
  name: string;
  fields: Array<{
    name: string;
    type: string;
    required: boolean;
  }>;
}

import { TemplateEditor } from './TemplateEditor';

import React, { useState, useEffect } from 'react';

export const TemplateManager = () => {
  const [templates, setTemplates] = useState<Template[]>([]);
  const [editingTemplate, setEditingTemplate] = useState<Template | null>(null);
  const { requestAnalysis } = useAIContext();

  useEffect(() => {
    const loadTemplates = async () => {
      try {
        const response = await TemplateService.getAll();
        setTemplates(response.data);
      } catch (error) {
        notify.error('Error al cargar las plantillas');
      }
    };

    loadTemplates();
  }, []);

  const handleSaveTemplate = async (template: Template) => {
    try {
      if (template.id) {
        await TemplateService.update(template.id, template);
      } else {
        await TemplateService.create(template);
      }
      const updatedTemplates = await TemplateService.getAll();
      setTemplates(updatedTemplates.data);
      setEditingTemplate(null);
    } catch (error) {
      notify.error('Error al guardar la plantilla');
    }
  };

  const handleAddTemplate = () => {
    const newTemplate: Template = {
      id: Date.now().toString(),
      name: '',
      fields: []
    };
    setEditingTemplate(newTemplate);
  };

  return (
    <Box>
      {editingTemplate ? (
        <TemplateEditor
          template={editingTemplate}
          onSave={handleSaveTemplate}
          onCancel={() => setEditingTemplate(null)}
        />
      ) : (
        <>
          <Button 
            variant="contained" 
            onClick={handleAddTemplate}
            sx={{ mb: 2 }}
          >
            Nueva Plantilla
          </Button>
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Nombre</TableCell>
                  <TableCell>Campos</TableCell>
                  <TableCell>Acciones</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {templates.map((template) => (
                  <TableRow key={template.id}>
                    <TableCell>{template.name}</TableCell>
                    <TableCell>{template.fields.length} campos</TableCell>
                    <TableCell>
                      <IconButton 
                        onClick={() => setEditingTemplate(template)}
                        aria-label="Editar plantilla"
                      >
                        <EditIcon />
                      </IconButton>
                      <IconButton 
                        onClick={() => handleDeleteTemplate(template.id)}
                        aria-label="Eliminar plantilla"
                      >
                        <DeleteIcon />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </>
      )}
    </Box>
  );
};

const handleDeleteTemplate = async (templateId: string) => {
  try {
    await TemplateService.delete(templateId);
    const updatedTemplates = await TemplateService.getAll();
    setTemplates(updatedTemplates.data);
    notify.success('Plantilla eliminada con éxito');
  } catch (error) {
    notify.error('Error al eliminar la plantilla');
  }
};

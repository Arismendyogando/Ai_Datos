import { useState } from 'react';
import { 
  Box,
  IconButton,
  List,
  ListItem,
  ListItemText,
  Divider,
  TextField,
  Button,
  CircularProgress,
  Typography,
  useTheme
} from '@mui/material';
import { 
  Close as CloseIcon,
  Menu as MenuIcon
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import { useAIContext } from '../../context/AIContext';
import styles from './SidePanel.module.css';

const SidePanel = () => {
  const theme = useTheme();
  const { concepts, isLoading, error, requestAnalysis } = useAIContext();
  const [isOpen, setIsOpen] = useState(false);
  const [inputValue, setInputValue] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    const conceptsArray = inputValue.split(',').map(c => c.trim()).filter(c => c);
    requestAnalysis(conceptsArray);
  };

  return (
    <Box 
      className={`${styles.sidePanel} ${isOpen ? styles.open : styles.closed}`}
      sx={{
        width: 320,
        height: '100vh',
        position: 'fixed',
        right: 0,
        top: 0,
        backgroundColor: theme.palette.background.paper,
        boxShadow: theme.shadows[4],
        zIndex: 1200,
        p: 2
      }}
    >
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
        <Typography variant="h6">Extracción de Datos</Typography>
        <IconButton onClick={() => setIsOpen(!isOpen)}>
          {isOpen ? <CloseIcon /> : <MenuIcon />}
        </IconButton>
      </Box>

      <Divider />

      <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
        <TextField
          fullWidth
          variant="outlined"
          label="Conceptos a extraer (separados por comas)"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          disabled={isLoading}
        />
        
        <Button
          type="submit"
          variant="contained"
          fullWidth
          sx={{ mt: 2 }}
          disabled={isLoading || !inputValue.trim()}
        >
          {isLoading ? <CircularProgress size={24} /> : 'Extraer Datos'}
        </Button>
      </Box>

      {error && (
        <Typography color="error" sx={{ mt: 2 }}>
          {error}
        </Typography>
      )}

      <List className={styles.conceptList}>
        {concepts.map((concept, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: index * 0.1 }}
          >
            <ListItem sx={{ px: 0 }}>
              <ListItemText
                primary={concept.name}
                secondary={concept.status}
                primaryTypographyProps={{ fontWeight: 500 }}
              />
            </ListItem>
            {index < concepts.length - 1 && <Divider />}
          </motion.div>
        ))}
      </List>

      {/* Nueva sección de interfaz de usuario */}
      <Box sx={{ mt: 4 }}>
        <Typography variant="h6" gutterBottom>
          Configuración de Extracción
        </Typography>
        
        <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
          <Button 
            variant="outlined" 
            fullWidth
            onClick={() => console.log('Configurar plantilla')}
          >
            Plantillas
          </Button>
          <Button 
            variant="outlined" 
            fullWidth
            onClick={() => console.log('Configurar validaciones')}
          >
            Validaciones
          </Button>
        </Box>

        <TextField
          fullWidth
          label="Nombre de la extracción"
          variant="outlined"
          sx={{ mb: 2 }}
        />

        <Button 
          variant="contained" 
          fullWidth
          onClick={() => console.log('Guardar configuración')}
        >
          Guardar Configuración
        </Button>
      </Box>
    </Box>
  );
};

export default SidePanel;

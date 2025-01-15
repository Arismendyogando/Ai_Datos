import React from 'react';
import { Card, CardContent, Button, Typography } from '@mui/material';
import { CircularProgress } from '@mui/material';
import { motion } from 'framer-motion';

interface ExportCardProps {
  title: string;
  icon: React.ElementType;
  description: string;
  onExport: () => void;
  isLoading: boolean;
}

export const ExportCard: React.FC<ExportCardProps> = ({ 
  title, 
  icon: Icon, 
  description, 
  onExport, 
  isLoading 
}) => {
  return (
    <Card component={motion.div} whileHover={{ scale: 1.02 }}>
      <CardContent>
        <Icon sx={{ fontSize: 40, mb: 2 }} />
        <Typography variant="h5" gutterBottom>
          {title}
        </Typography>
        <Typography color="textSecondary">
          {description}
        </Typography>
        <Button
          fullWidth
          variant="contained"
          onClick={onExport}
          disabled={isLoading}
          startIcon={isLoading ? <CircularProgress size={20} /> : <Icon />}
          sx={{ mt: 2 }}
        >
          {isLoading ? 'Exportando...' : 'Exportar'}
        </Button>
      </CardContent>
    </Card>
  );
};

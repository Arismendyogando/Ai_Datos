import { useContext } from 'react';
import { SnackbarContext } from '../context/SnackbarContext.js';

export const useNotify = () => {
  const context = useContext(SnackbarContext);
  if (!context) {
    throw new Error('useNotify must be used within a SnackbarProvider');
  }
  return context;
};

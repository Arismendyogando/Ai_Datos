import { createContext, useContext, useState } from 'react';

const AIContext = createContext();

export const AIProvider = ({ children }) => {
  const [concepts, setConcepts] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const requestAnalysis = async (conceptsArray) => {
    setIsLoading(true);
    setError(null);
    
    try {
      // Simular proceso de análisis
      const processingConcepts = conceptsArray.map(concept => ({
        name: concept,
        status: 'Procesando...'
      }));
      
      setConcepts(processingConcepts);

      // Simular tiempo de procesamiento
      await new Promise(resolve => setTimeout(resolve, 2000));

      const processedConcepts = processingConcepts.map(concept => ({
        ...concept,
        status: 'Completado'
      }));

      setConcepts(processedConcepts);
    } catch (err) {
      setError('Error al procesar los conceptos');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AIContext.Provider value={{
      concepts,
      isLoading,
      error,
      requestAnalysis
    }}>
      {children}
    </AIContext.Provider>
  );
};

export const useAIContext = () => useContext(AIContext);

import { createContext, useContext, useState } from 'react';
import { DocumentAnalysisService } from '../services/ai/documentService';

const AIContext = createContext();
const documentService = new DocumentAnalysisService();

export const AIProvider = ({ children }) => {
  const [concepts, setConcepts] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [analysisResults, setAnalysisResults] = useState([]);
  // Añadir manejo de plantillas
  const [templates, setTemplates] = useState([]);

  const analyzeWithTemplate = async (documentId, templateId) => {
    // Lógica de análisis con plantilla
  };

  const requestAnalysis = async (document, template) => {
    setIsLoading(true);
    setError(null);
    
    try {
      const result = await documentService.analyzeDocument(document, template);
      setAnalysisResults(prev => [...prev, result]);
      
      const processedConcepts = concepts.map(concept => ({
        ...concept,
        status: 'Completed',
        result: result
      }));

      setConcepts(processedConcepts);
    } catch (err) {
      setError('Error processing document: ' + err.message);
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
      analysisResults,
      requestAnalysis
    }}>
      {children}
    </AIContext.Provider>
  );
};

export const useAIContext = () => useContext(AIContext);
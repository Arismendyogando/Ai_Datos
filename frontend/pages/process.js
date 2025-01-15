import React, { useState } from 'react';
import { Container, Stepper, Step, StepLabel, Box } from '@mui/material';
import { DocumentUploader } from '../components/DocumentUploader';
import { DataViewer } from '../components/DataViewer';
import { AnalyzeDocumentButton } from '../components/AI/AnalyzeDocumentButton';
// import { TemplateSelector } from '../components/TemplateSelector'; // Assuming this component will be created later
// import { ExportOptions } from '../components/ExportOptions'; // Assuming this component will be created later

export default function ProcessPage() {
  const [activeStep, setActiveStep] = useState(0);
  const [processedData, setProcessedData] = useState(null);
  const [documentId, setDocumentId] = useState(null);

  const steps = [
    'Cargar Documento',
    'Seleccionar Plantilla',
    'Analizar Documento',
    'Verificar Datos',
    'Exportar'
  ];

  const handleDocumentUploaded = (id) => {
    setDocumentId(id);
    setActiveStep(1);
  };

  return (
    <Container maxWidth="md">
      <Stepper activeStep={activeStep} alternativeLabel>
        {steps.map((label, index) => (
          <Step key={label}>
            <StepLabel>{label}</StepLabel>
          </Step>
        ))}
      </Stepper>
      
      {/* Contenido según paso activo */}
      {activeStep === 0 && <DocumentUploader onDocumentUploaded={handleDocumentUploaded} />}
      {activeStep === 1 && <div> {/*<TemplateSelector />*/} </div>}
      {activeStep === 2 && documentId && <AnalyzeDocumentButton documentId={documentId} />}
      {activeStep === 3 && <DataViewer data={processedData || []} />}
      {activeStep === 4 && <div> {/*<ExportOptions data={processedData} />*/} </div>}
    </Container>
  );
}

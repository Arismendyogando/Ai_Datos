import React, { useState, useEffect } from 'react';
import { Grid, Typography } from '@mui/material';

interface DataSummaryProps {
  summary: any;
}

const DataSummary: React.FC<DataSummaryProps> = ({ summary }) => {
  return summary ? (
    <div>
      <Typography variant="h6">Resumen de Datos</Typography>
      <pre>{JSON.stringify(summary, null, 2)}</pre>
    </div>
  ) : (
    <Typography>No hay resumen disponible.</Typography>
  );
};

interface EntityRelationsProps {
  entities: any;
}

const EntityRelations: React.FC<EntityRelationsProps> = ({ entities }) => {
  return entities ? (
    <div>
      <Typography variant="h6">Relaciones de Entidades</Typography>
      <pre>{JSON.stringify(entities, null, 2)}</pre>
    </div>
  ) : (
    <Typography>No hay relaciones de entidades disponibles.</Typography>
  );
};

interface TransactionHistoryProps {
  transactions: any;
}

const TransactionHistory: React.FC<TransactionHistoryProps> = ({ transactions }) => {
  return transactions ? (
    <div>
      <Typography variant="h6">Historial de Transacciones</Typography>
      <pre>{JSON.stringify(transactions, null, 2)}</pre>
    </div>
  ) : (
    <Typography>No hay historial de transacciones disponible.</Typography>
  );
};

interface DataAnalyzerProps {
  documentId?: string;
}

export const DataAnalyzer: React.FC<DataAnalyzerProps> = ({ documentId }) => {
  const [analysisResults, setAnalysisResults] = useState<any>(null);

  useEffect(() => {
    const analyzeDocument = async () => {
      if (documentId) {
        // Aquí deberías llamar al servicio de IA
        // const results = await AIService.analyzeDocument(documentId);
        setAnalysisResults({
          summary: { totalAmount: 100 },
          entities: ['entity1', 'entity2'],
          transactions: [{ id: 1, amount: 50 }]
        }); // Placeholder
      }
    };

    analyzeDocument();
  }, [documentId]);

  return (
    <Grid container spacing={2}>
      <Grid item xs={12}>
        <DataSummary summary={analysisResults?.summary} />
      </Grid>
      <Grid item xs={12} md={6}>
        <EntityRelations entities={analysisResults?.entities} />
      </Grid>
      <Grid item xs={12} md={6}>
        <TransactionHistory transactions={analysisResults?.transactions} />
      </Grid>
    </Grid>
  );
};

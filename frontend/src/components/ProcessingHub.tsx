import { Grid, Paper, Box } from '@mui/material'
import { motion } from 'framer-motion'
import { FilePreviewList, ProcessingProgress, BatchActions, ErrorDisplay } from './components'
import { useProcessingHub } from '../hooks/useProcessingHub'

const ProcessingHub = () => {
  const {
    selectedFiles,
    processedCount,
    totalFiles,
    errors,
    handleFileSelect,
    handleBatchProcess,
    handleExport,
    handleRetry
  } = useProcessingHub()

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      <Grid container spacing={3}>
        <Grid item xs={12} md={7}>
          <Paper elevation={2} sx={{ p: 2 }}>
            <FilePreviewList 
              files={selectedFiles}
              onSelect={handleFileSelect}
            />
          </Paper>
        </Grid>
        
        <Grid item xs={12} md={5}>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <ProcessingProgress 
              current={processedCount}
              total={totalFiles}
            />
            
            <BatchActions 
              onBatchProcess={handleBatchProcess}
              onExport={handleExport}
              disabled={!selectedFiles.length}
            />
            
            {errors.length > 0 && (
              <ErrorDisplay 
                errors={errors}
                onRetry={handleRetry}
              />
            )}
          </Box>
        </Grid>
      </Grid>
    </motion.div>
  )
}

export default ProcessingHub
const HomePage = () => {
  const { 
    files,
    handleUpload,
    handleDriveSelect,
    handleFilterChange,
    startProcessing
  } = useFileProcessing()

  return (
    <Container maxWidth="lg">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <Box sx={{ mb: 4 }}>
          <Typography variant="h4" component="h1" gutterBottom>
            Procesamiento de Documentos
          </Typography>
        </Box>

        <FileUploadZone 
          onUpload={handleUpload}
          acceptedTypes={['.pdf', '.xlsx', '.jpg', '.png', '.txt']}
        />

        <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
          <GoogleDriveIntegration onSelect={handleDriveSelect} />
          <FileTypeFilters onChange={handleFilterChange} />
        </Box>

        <ProcessingQueue 
          files={files}
          onProcess={startProcessing}
        />
      </motion.div>
    </Container>
  )
}
import { ThemeProvider, CssBaseline } from '@mui/material'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { MainLayout } from './layouts'
import { HomePage, ProcessingHub, DataEditor, ExportView } from './pages'
import { theme } from './theme'
import { AnimatePresence } from 'framer-motion'

const App = () => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <BrowserRouter>
        <MainLayout>
          <AnimatePresence mode="wait">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/process" element={<ProcessingHub />} />
              <Route path="/edit" element={<DataEditor />} />
              <Route path="/export" element={<ExportView />} />
            </Routes>
          </AnimatePresence>
        </MainLayout>
      </BrowserRouter>
    </ThemeProvider>
  )
}

export default App
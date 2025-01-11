import { ThemeProvider, CssBaseline } from '@mui/material';
import dynamic from 'next/dynamic';
import { Suspense } from 'react';
import theme from '../src/theme';
import { AIProvider } from '../context/AIContext';

const DashboardLayout = dynamic(() => import('../components/Layout/DashboardLayout'), {
  loading: () => <div>Cargando...</div>,
  ssr: true
});

const Toaster = dynamic(() => import('react-hot-toast').then(mod => mod.Toaster), {
  ssr: false
});

function MyApp({ Component, pageProps }) {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AIProvider>
        <Suspense fallback={<div>Cargando...</div>}>
          <DashboardLayout>
            <Component {...pageProps} />
          </DashboardLayout>
          <Toaster
            position="top-right"
            toastOptions={{
              duration: 3000,
              style: {
                background: '#363636',
                color: '#fff',
              },
            }}
          />
        </Suspense>
      </AIProvider>
    </ThemeProvider>
  );
}

export default MyApp;

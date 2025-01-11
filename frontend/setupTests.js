import '@testing-library/jest-dom/extend-expect';
import { configure } from '@testing-library/react';

// Configuración adicional de Testing Library
configure({ testIdAttribute: 'data-test' });

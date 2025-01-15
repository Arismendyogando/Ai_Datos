import axios from 'axios';

const api = axios.create({
  baseURL: '/api'
});

export const ExportService = {
  toExcel: async (data: any) => {
    return api.post('/export/excel', data);
  },
  toSheets: async (data: any) => {
    return api.post('/export/sheets', data);
  }
};

export const DocumentService = {
  upload: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/documents/upload', formData);
  },
  process: async (documentId: string) => {
    return api.post(`/documents/${documentId}/process`);
  },
  analyze: async (documentId: string) => {
    return api.post(`/documents/${documentId}/analyze`);
  },
  getStatus: async (documentId: string) => {
    return api.get(`/documents/${documentId}/status`);
  }
};

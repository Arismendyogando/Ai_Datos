import fs from 'fs';
import path from 'path';

global.fetch = require('node-fetch');

describe('File Processing', () => {
  test('handles PDF files correctly', async () => {
    const filePath = path.join(__dirname, 'test-files', 'sample_invoice.pdf');
    const fileBuffer = fs.readFileSync(filePath);
    const fileName = 'sample_invoice.pdf';
    const fileType = 'application/pdf';
    const fileBlob = new Blob([fileBuffer], { type: fileType });

    const formData = new FormData();
    formData.append('file', fileBlob, fileName);

    const response = await fetch('/api/upload', {
      method: 'POST',
      body: formData,
    });

    expect(response.status).toBe(200);
    const data = await response.json();
    expect(data).toBeDefined();
    // Add more specific assertions based on the expected response structure
  });
  
  test('processes batch operations efficiently', async () => {
    // Simulate multiple file uploads
    const filePaths = [
      path.join(__dirname, 'test-files', 'sample_invoice.pdf'),
      path.join(__dirname, 'test-files', 'sample_invoice.pdf'),
    ];

    const formData = new FormData();
    filePaths.forEach((filePath, index) => {
      const fileBuffer = fs.readFileSync(filePath);
      const fileName = `sample_invoice_${index + 1}.pdf`;
      const fileType = 'application/pdf';
      const fileBlob = new Blob([fileBuffer], { type: fileType });
      formData.append('files', fileBlob, fileName);
    });

    const response = await fetch('/api/upload', {
      method: 'POST',
      body: formData,
    });

    expect(response.status).toBe(200);
    const data = await response.json();
    expect(data).toBeDefined();
    expect(Array.isArray(data)).toBe(true);
    expect(data.length).toBe(filePaths.length);
  });
});

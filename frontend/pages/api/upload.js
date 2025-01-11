import { formidable } from 'formidable';
import fs from 'fs';

export const config = {
  api: {
    bodyParser: false,
  },
};

export default async function handler(req, res) {
  if (req.method === 'POST') {
    const contentType = req.headers['content-type'];

    if (contentType && contentType.startsWith('application/json')) {
      // Handle Google Drive upload
      let body = '';
      req.on('data', (chunk) => {
        body += chunk.toString();
      });

      req.on('end', async () => {
        try {
          const data = JSON.parse(body);
          const { source, fileId } = data;

          if (source === 'google-drive' && fileId) {
            try {
              const backendResponse = await fetch('http://localhost:8000/api/upload/google-drive', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                },
                body: JSON.stringify({ fileId }),
              });

              if (!backendResponse.ok) {
                const errorData = await backendResponse.json();
                throw new Error(errorData.message || 'Error communicating with the backend');
              }

              const result = await backendResponse.json();
              return res.status(200).json(result);
            } catch (error) {
              console.error("Error sending Google Drive file ID to backend:", error);
              return res.status(500).json({ message: 'Error al comunicar con el backend.' });
            }
          } else {
            return res.status(400).json({ message: 'Invalid request for Google Drive upload.' });
          }
        } catch (error) {
          console.error("Error processing Google Drive upload:", error);
          return res.status(400).json({ message: 'Error al procesar la solicitud de Google Drive.' });
        }
      });
    } else {
      // Handle local file upload
      const form = formidable({ multiples: false });

      form.parse(req, async (err, fields, files) => {
        if (err) {
          console.error("Error parsing the incoming data:", err);
          return res.status(500).json({ message: 'Error al procesar la solicitud.' });
        }

        const file = files.file;
        if (!file) {
          return res.status(400).json({ message: 'No se subió ningún archivo' });
        }

        const extractionOption = fields.extractionOption;
        const fileContent = await fs.promises.readFile(file.filepath);

        try {
          const backendResponse = await fetch('http://localhost:8000/api/upload', {
            method: 'POST',
            body: fileContent,
            headers: {
              'Content-Type': file.mimetype,
              'X-File-Name': file.originalFilename,
              'X-Extraction-Option': extractionOption,
            },
          });

          if (!backendResponse.ok) {
            throw new Error(await backendResponse.text());
          }

          const data = await backendResponse.json();
          await fs.promises.unlink(file.filepath);
          return res.status(200).json(data);
        } catch (error) {
          console.error('Error al procesar el archivo:', error);
          return res.status(500).json({
            error: error.message || 'Error al procesar el archivo',
          });
        }
      });
    }
  } else {
    res.status(405).json({ message: 'Method not allowed' });
  }
}

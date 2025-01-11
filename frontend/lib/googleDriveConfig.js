// Configuración de Google Drive API
const GOOGLE_DRIVE_CONFIG = {
  apiKey: process.env.NEXT_PUBLIC_GOOGLE_API_KEY,
  clientId: process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID,
  discoveryDocs: [
    'https://www.googleapis.com/discovery/v1/apis/drive/v3/rest'
  ],
  scope: 'https://www.googleapis.com/auth/drive.readonly',
};

export const loadGoogleDriveAPI = () => {
  return new Promise((resolve, reject) => {
    try {
      // Verificar si la API ya está cargada
      if (window.gapi) {
        return resolve();
      }

      const script = document.createElement('script');
      script.src = 'https://apis.google.com/js/api.js';
      script.async = true;
      script.defer = true;
      
      script.onload = async () => {
        try {
          // Cargar cliente y autenticación
          await window.gapi.load('client:auth2');
          
          // Inicializar cliente con configuración
          await window.gapi.client.init(GOOGLE_DRIVE_CONFIG);
          
          // Verificar autenticación
          const authInstance = window.gapi.auth2.getAuthInstance();
          if (!authInstance.isSignedIn.get()) {
            await authInstance.signIn();
          }
          
          resolve();
        } catch (error) {
          reject(new Error(`Error al inicializar Google Drive API: ${error.message}`));
        }
      };
      
      script.onerror = (error) => {
        reject(new Error(`Error al cargar Google Drive API: ${error.message}`));
      };
      
      document.body.appendChild(script);
    } catch (error) {
      reject(new Error(`Error en la configuración de Google Drive: ${error.message}`));
    }
  });
};

export const selectFileFromGoogleDrive = () => {
  return new Promise((resolve, reject) => {
    try {
      // Verificar si la API está disponible
      if (!window.google || !window.google.picker) {
        throw new Error('Google Picker API no está disponible');
      }

      const pickerCallback = (data) => {
        try {
          if (data.action === window.google.picker.Action.PICKED) {
            if (!data.docs || data.docs.length === 0) {
              throw new Error('No se seleccionó ningún archivo');
            }
            
            const file = data.docs[0];
            if (!file.id) {
              throw new Error('El archivo seleccionado no tiene un ID válido');
            }
            
            resolve(file.id);
          } else if (data.action === window.google.picker.Action.CANCEL) {
            reject(new Error('Selección cancelada por el usuario'));
          }
        } catch (error) {
          reject(error);
        }
      };

      // Configurar vista del selector
      const view = new window.google.picker.View(window.google.picker.ViewId.DOCS);
      view.setMimeTypes('application/pdf,image/jpeg,image/png');
      
      // Obtener token de acceso
      const authInstance = window.gapi.auth2.getAuthInstance();
      const user = authInstance.currentUser.get();
      const accessToken = user.getAuthResponse().access_token;

      // Construir y mostrar selector
      const picker = new window.google.picker.PickerBuilder()
        .addView(view)
        .setOAuthToken(accessToken)
        .setDeveloperKey(GOOGLE_DRIVE_CONFIG.apiKey)
        .setCallback(pickerCallback)
        .setOrigin(window.location.origin)
        .build();
      
      picker.setVisible(true);
    } catch (error) {
      reject(new Error(`Error en el selector de archivos: ${error.message}`));
    }
  });
};

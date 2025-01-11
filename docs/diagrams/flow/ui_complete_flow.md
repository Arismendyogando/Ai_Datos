# Integrated UI and System Flow

## System Architecture Overview

```mermaid
graph TD
    A["Main Component"] --> B(backend)
    A --> F(frontend)
    B --> BA[api]
    B --> BAP[app]
    BAP --> BAPR[routes]
    BAPR --> BAPRF[file_processing.py]
    B --> BM[modules]
    BM --> BMI[invoice_processing]
    BMI --> BMIP[parsers]
    BMIP --> BMIPI[image_parser.py]
    BMI --> BMIU[utils]
    BMI --> BMIV[validators]
    B --> BS[services]
    BS --> BSI[invoice_parser.py]
    B --> BT[tests]
    BT --> BTI[integration]
    F --> FC[components]
    FC --> FCU[Upload]
    F --> FP[pages]
    FP --> FPA[api]
    F --> FRC[src]
    FRC --> FRCMP[components]
    FRC --> FRCP[pages]
    FRC --> FRCS[services]
    F --> FST[styles]
    SCR[scripts]  


User Interface Flow
```graph LR
    A[Inicio] --> B(Usuario abre la AppWeb)
    B --> C{Adjuntar Factura}
    C -- Desde el escritorio --> D[Seleccionar archivo desde el escritorio]
    C -- Desde Google Drive --> E[Seleccionar archivo desde Google Drive]
    D --> F(Archivo adjuntado)
    E --> F
    F --> G{Configurar extracción de datos}
    G -- Usar plantilla existente --> H[Seleccionar plantilla]
    G -- Crear nueva plantilla --> I[Definir campos a extraer y patrones]
    H --> J(Aplicar configuración)
    I --> J
    J --> K[Procesamiento de la factura]
    K --> L{Presentar datos extraídos en filas}
    L --> M{¿Corregir datos?}
    M -- Sí --> N[Modificar campos]
    N --> L
    M -- No --> O{¿Aprobar fila?}
    O -- Sí --> P[Agregar fila a tabla de datos]
    O -- No --> Q[Descartar fila / Volver a configurar]
    P --> R{¿Más filas por revisar?}
    R -- Sí --> L
    R -- No --> S[Mostrar tabla de datos]
    S --> T{Ajustar columnas de la tabla}
    T --> U{Editar encabezados de columnas}
    U --> V{Guardar/Compartir/Descargar}
    V -- Guardar --> W[Seleccionar formato de guardado (Excel, Google Sheets, PDF)]
    V -- Compartir --> X[Opciones de compartición (Correo, enlace, etc.)]
    V -- Descargar --> Y[Seleccionar formato de descarga (Excel, Google Sheets, PDF)]
    W --> Z[Archivo guardado]
    X --> AA[Compartido exitosamente]
    Y --> AB[Archivo descargado]
    Q --> G
    Z --> AC[Fin]
    AA --> AC
    AB --> AC

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style AC fill:#f9f,stroke:#333,stroke-width:2px
    style C fill:#ccf,stroke:#333,stroke-width:2px
    style G fill:#ccf,stroke:#333,stroke-width:2px
    style M fill:#ccf,stroke:#333,stroke-width:2px
    style O fill:#ccf,stroke:#333,stroke-width:2px
    style V fill:#ccf,stroke:#333,stroke-width:2px  


Current Implementation
```mermaid
flowchart TD
    UI["Modern and Intuitive UI"] --> FileUploader[FileUploader.jsx]
    UI --> EditableGrid[EditableDataGrid.jsx]
    UI --> ExportPage[export.js]
    
    FileUploader --> Upload[Desktop Upload]
    FileUploader --> GDrive[Google Drive]
    
    EditableGrid --> DataRows[Data Grid]
    EditableGrid --> Approval[Approval Process]
    EditableGrid --> EditColumns[Edit Columns]
    
    ExportPage --> Excel[Excel Export]
    ExportPage --> Sheets[Google Sheets]
    ExportPage --> Share[Share Options]
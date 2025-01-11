class DataManager {
  async processFile(file: File) {
    const data = await this.extractData(file)
    return this.formatData(data)
  }

  async saveToGoogleSheets(data: ProcessedData) {
    // Implementación de exportación
  }
}

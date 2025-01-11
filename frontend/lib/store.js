import { create } from 'zustand';

const useInvoiceStore = create((set) => ({
  processedInvoices: null,
  setProcessedInvoices: (data) => set({ processedInvoices: data }),
}));

export default useInvoiceStore;

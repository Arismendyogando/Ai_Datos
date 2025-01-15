export const TemplateService = {
  create: async (template) => api.post('/templates', template),
  update: async (id, template) => api.put(`/templates/${id}`, template),
  delete: async (id) => api.delete(`/templates/${id}`),
  getAll: async () => api.get('/templates'),
  getById: async (id) => api.get(`/templates/${id}`)
};

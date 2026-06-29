import api from './api';

const LIST_ENDPOINT = 'auth/admin/vendors/';
const CREATE_ENDPOINT = 'auth/admin/create-vendor/';

export const vendorService = {
  list: (params) => api.get(LIST_ENDPOINT, { params }),
  get: (id) => api.get(`${LIST_ENDPOINT}${id}/`),

  create: (data) => api.post(CREATE_ENDPOINT, data),

  update: (id, data) => api.put(`${LIST_ENDPOINT}${id}/`, data),
  partialUpdate: (id, data) => api.patch(`${LIST_ENDPOINT}${id}/`, data),
  remove: (id) => api.delete(`${LIST_ENDPOINT}${id}/`),
};

export default vendorService;
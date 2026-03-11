import { axiosV1 } from '../../../core/api/axiosInstance';

export const fuelRequestV1Api = {
  // Recebe os parâmetros (como { page: 1 }) e repassa para o Axios
  list: async (params) => {
    const response = await axiosV1.get('/requests/', { params });
    return response.data; 
  },
  
  create: async (data) => {
    const response = await axiosV1.post('/requests/', data);
    return response.data;
  },

  approve: async (id) => {
    const response = await axiosV1.post(`/requests/${id}/approve/`);
    return response.data;
  },

  reject: async (id) => {
    const response = await axiosV1.post(`/requests/${id}/reject/`);
    return response.data;
  },

  cancel: async (id) => {
    const response = await axiosV1.post(`/requests/${id}/cancel/`);
    return response.data;
  },

  complete: async (id) => {
    const response = await axiosV1.post(`/requests/${id}/complete/`);
    return response.data;
  }
};

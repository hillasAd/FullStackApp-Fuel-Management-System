import axiosV1 from '../../../core/api/axiosInstance';

export const vehicleApi = {
  // Lista todas as viaturas
  list: async () => {
    const response = await axiosV1.get('/vehicles/');
    return response.data.data; // Retorna o array de viaturas
  },

  // Cria uma nova viatura
  create: async (vehicleData) => {
    const response = await axiosV1.post('/vehicles/', vehicleData);
    return response.data.data;
  },

  update: async (id, vehicleData) => {
    const response = await axiosV1.put(`/vehicles/${id}/`, vehicleData);
    return response.data.data; // Retorna a nova versão vinda do backend
  },
  
  // GET ONE: Busca apenas uma viatura (útil para carregar o form)
  getById: async (id) => {
    const response = await axiosV1.get(`/vehicles/${id}/`);
    return response.data.data;
  }
};

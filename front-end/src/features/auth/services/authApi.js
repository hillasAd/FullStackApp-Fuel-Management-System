import {axiosV1} from '../../../core/api/axiosInstance';

/**
 * Comunicação direta com o módulo de Authentication do Django.
 */
export const authApi = {
  login: async (credentials) => {
    // credentials = { username, password }
    const response = await axiosV1.post('/auth/login/', credentials);
    // O teu backend responde: { success: true, data: { access, refresh, user: { ... } } }
    return response.data.data;
  },
};

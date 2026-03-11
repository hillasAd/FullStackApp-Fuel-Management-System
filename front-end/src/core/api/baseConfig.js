import { generateCorrelationId } from '../../shared/utils/correlationId';
import { useAuthStore } from '../auth/authStore';

export const applyInterceptors = (instance) => {
  // INTERCEPTOR DE REQUEST: Armadura de envio
  instance.interceptors.request.use(
    (config) => {
      config.headers['X-Correlation-ID'] = generateCorrelationId();
      
      const token = useAuthStore.getState().token;
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    },
    (error) => Promise.reject(error)
  );
  
  // INTERCEPTOR DE RESPONSE: Arsenal de tratamento de erros
  instance.interceptors.response.use(
    (response) => response,
    (error) => {
      // Se o erro for 409 (Conflict), nosso backend enviou um erro de concorrência
      if (error.response?.status === 409) {
        console.error("CONCURRENCY ERROR: Alguém alterou os dados primeiro.");
      }
      return Promise.reject(error);
    }
  );

  return instance;
};

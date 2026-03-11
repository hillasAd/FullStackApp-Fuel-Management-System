import axiosInstance from './axiosInstance';

/**
 * Wrapper Resiliente: Padroniza a resposta para o formato do teu Backend.
 * Se o Backend devolver { success: true, data: [...] }, este wrapper entrega o [...]
 */
export const requestWrapper = async (config) => {
  try {
    const response = await axiosInstance(config);
    // O teu backend devolve { success: true, data: ... }
    return response.data.data; 

  } catch (error) {

    const serverMessage = error.response?.data?.error?.message;
    // Aqui capturamos o erro padronizado do teu shared/exception_handler
    const apiError = error.response?.data?.error || {
      code: 'network_error',
       message: serverMessage || 'Erro na comunicação com o servidor.'
    };
    
    // Lançamos o erro para o React Query capturar
    throw apiError;
  }
};

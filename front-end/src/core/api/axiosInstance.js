import axios from 'axios';
import { applyInterceptors } from './baseConfig';

const API_V1_URL = import.meta.env.VITE_API_V1_URL;
const API_V2_URL = import.meta.env.VITE_API_V2_URL;

// Instância V1 (Ex: Viaturas, Combustível)
export const axiosV1 = applyInterceptors(axios.create({
  baseURL: API_V1_URL,
  headers: { 'Content-Type': 'application/json' },
}));

// Instância V2 (Ex: Novos módulos de Logística)
export const axiosV2 = applyInterceptors(axios.create({
  baseURL: API_V2_URL,
  headers: { 'Content-Type': 'application/json' },
}));

export default axiosV1;

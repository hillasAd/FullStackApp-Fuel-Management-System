import { axiosV2 } from '../../../core/api/axiosInstance';

export const getDashboardSummary = async () => {
  const response = await axiosV2.get('/dashboard/summary/');
  return response.data;
};

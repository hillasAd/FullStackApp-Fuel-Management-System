import { axiosV2 } from "../../../core/api/axiosInstance";
import { generateCorrelationId } from "../../../shared/utils/correlationId";

export const fuelRequestApi = {
  listBulk: async (params) => {
    const response = await axiosV2.get("/requests/bulk/", {params});
    return response.data.data || response.data;
  },

  getBulkDetail: async (id) => {
    const response = await axiosV2.get(`/requests/bulk/${id}/`);
    return response.data.data;
  },

  createBulk: async (bulkData) => {
    const idempotencyKey = generateCorrelationId();
    const response = await axiosV2.post(
      "/requests/bulk/create/",
      bulkData,
      { headers: { "X-Idempotency-Key": idempotencyKey } }
    );
    return response.data.data;
  },

  processItem: async (requestId, itemId, action, version, reason = "") => {
    const response = await axiosV2.post(
      `/requests/bulk/${requestId}/items/${itemId}/process/`, 
      { 
        action, 
        version: Number(version),
        reason 
      }
    );
    return response.data.data;
  },

  processBulkAction: async (requestId, action, version, reason = "") => {
     const response = await axiosV2.post(
      `/requests/bulk/${requestId}/process/`, 
      { 
        action, 
        version: Number(version), 
        reason 
      }
    );
    return response.data.data;
  }
};

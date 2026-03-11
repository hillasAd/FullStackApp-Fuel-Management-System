import { defineConfig } from "cypress";
import "dotenv/config";

export default defineConfig({
  e2e: {
    baseUrl: 'http://localhost:5173',
    
    setupNodeEvents(on, config) {
      config.env.apiUrlV1 = process.env.VITE_API_V1_URL;
      config.env.apiUrlV2 = process.env.VITE_API_V2_URL;
      
      return config;
    },
  },
});

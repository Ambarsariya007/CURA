import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    allowedHosts: [
      '6ead-115-245-68-163.ngrok-free.app',
      '703b-115-245-68-163.ngrok-free.app',
    ],
  },
});
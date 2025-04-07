import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    allowedHosts: [
      'f39c-115-245-68-163.ngrok-free.app',
      'cabf-115-245-68-163.ngrok-free.app',
    ],
  },
});
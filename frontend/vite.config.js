import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    staticPort: true,
    watch: {
      usePolling: true
    }

   },
   define: {
    'import.meta.env.VITE_API_URL': JSON.stringify('http://localhost:5001')
  }
})

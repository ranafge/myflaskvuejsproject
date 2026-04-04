
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',           // ✅ Docker/নেটওয়ার্ক অ্যাক্সেস
    port: 5173,                 // ✅ নির্দিষ্ট পোর্ট
    strictPort: true,           // ✅ পোর্ট ব্যস্ত থাকলে error (staticPort না!)
    watch: {
      usePolling: true          // ✅ Docker-এর জন্য প্রয়োজন
    },
    // 🔥 Ingress-এর জন্য এগুলো যোগ করো
    allowedHosts: [             // কোন হোস্ট থেকে request আসতে পারবে
      'app.myapp.local',        // Ingress ডোমেইন
      'localhost',              // লোকাল ডেভেলপমেন্ট
      '127.0.0.1',
      "192.168.0.100"              // লোকাল আইপি
    ],
    cors: true                  // CORS সক্রিয়
  },
  // define: {
  //   // Ingress-এর জন্য API URL পরিবর্তন করো
  //   'import.meta.env.VITE_API_URL': JSON.stringify('http://localhost:5000')
  // }
})


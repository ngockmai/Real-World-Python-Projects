import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react'

export default defineConfig({
    plugins: [
        react()
    ],
    build: {
        outDir: '../static/dist',
        emptyOutDir: true,
        rollupOptions: {
            output: {
                entryFileNames: 'assets/[name].js',
                chunkFileNames: 'assets/[name].js',
                assetFileNames: 'assets/[name].[ext]'
            }
        }
    },
    server: {
        port: 3000,
        strictPort: false,
        proxy: {
            '/api': {
                target: 'http://127.0.0.1:8000',
                changeOrigin: true,
            },
            '/device': {
                target: 'http://127.0.0.1:8000',
                changeOrigin: true,
            },
        },
    }
})
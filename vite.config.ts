import { defineConfig } from 'vite';
import path from 'path';

export default defineConfig({
  base: './',
  resolve: {
    alias: {
      '@core':    path.resolve(__dirname, 'src/core'),
      '@scenes':  path.resolve(__dirname, 'src/scenes'),
      '@entities':path.resolve(__dirname, 'src/entities'),
      '@systems': path.resolve(__dirname, 'src/systems'),
      '@ui':      path.resolve(__dirname, 'src/ui'),
      '@data':    path.resolve(__dirname, 'src/data'),
    }
  },
  server: {
    port: 3000,
    open: true,
  },
  build: {
    outDir:       'dist',
    assetsDir:    'assets',
    rollupOptions: {
      output: {
        manualChunks: {
          phaser: ['phaser'],
        }
      }
    }
  }
});

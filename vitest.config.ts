import { defineConfig } from 'vitest/config';
import path from 'path';

export default defineConfig({
  resolve: {
    alias: {
      '@core':    path.resolve(__dirname, 'src/core'),
      '@systems': path.resolve(__dirname, 'src/systems'),
      '@data':    path.resolve(__dirname, 'src/data'),
      '@scenes':  path.resolve(__dirname, 'src/scenes'),
      '@entities':path.resolve(__dirname, 'src/entities'),
      '@ui':      path.resolve(__dirname, 'src/ui'),
      '@i18n':    path.resolve(__dirname, 'src/i18n'),
    },
  },
  test: {
    environment: 'node',
    globals:     true,
    include:     ['tests/**/*.test.ts'],
  },
});

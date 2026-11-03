import { defineConfig } from 'vite';
export default defineConfig({server:{port:9011,proxy:{'/api':'http://localhost:8011'}}});
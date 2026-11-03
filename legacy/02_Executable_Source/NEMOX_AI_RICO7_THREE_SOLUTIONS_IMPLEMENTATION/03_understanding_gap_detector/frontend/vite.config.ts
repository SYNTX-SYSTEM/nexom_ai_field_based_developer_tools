import { defineConfig } from 'vite';
export default defineConfig({server:{port:9013,proxy:{'/api':'http://localhost:8013'}}});
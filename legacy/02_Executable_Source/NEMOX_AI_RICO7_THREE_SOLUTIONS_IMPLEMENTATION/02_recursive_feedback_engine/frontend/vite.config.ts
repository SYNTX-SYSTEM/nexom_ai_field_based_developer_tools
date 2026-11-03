import { defineConfig } from 'vite';
export default defineConfig({server:{port:9012,proxy:{'/api':'http://localhost:8012'}}});
import { defineConfig } from 'vite';
export default defineConfig({server:{port:3000,proxy:{'/api':process.env.DOCKER_ENV ? 'http://backend:8000' : 'http://127.0.0.1:8000'}}});

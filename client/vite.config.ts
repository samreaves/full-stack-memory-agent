import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import { env } from 'process';
import { fileURLToPath } from 'url';
import path from 'path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const clientPort = env.CLIENT_PORT || 5173;

export default defineConfig({
	plugins: [sveltekit()],
	resolve: {
		alias: {
			$components: path.resolve(__dirname, './src/components')
		}
	},
	server: {
		port: clientPort,
		host: true
	},
	preview: {
		port: clientPort,
		host: true
	}
});


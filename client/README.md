# Full Stack Memory Agent - Client

SvelteKit frontend application for the AI Chat with Memory agent.

## Development

### Prerequisites

- Node.js 20+ 
- npm or yarn

### Setup

```bash
npm install
```

### Run Development Server

```bash
npm run dev
```

The application will be available at `http://localhost:5173`.

### Environment Variables

Create a `.env` file (optional):

```
VITE_API_URL=http://localhost:8000
```

If not set, the API URL defaults to `http://localhost:8000`.

## Building for Production

```bash
npm run build
```

The built files will be in the `build/` directory.

## Docker

The client is containerized and can be run with docker-compose from the project root:

```bash
docker compose up client
```

Or build the image manually:

```bash
docker build -t ai-client .
docker run -p 5173:5173 ai-client
```

## Project Structure

```
client/
├── src/
│   ├── components/     # Svelte components
│   ├── lib/           # Utilities and stores
│   │   ├── api.ts     # API client
│   │   └── stores/    # Svelte stores for state management
│   └── routes/        # SvelteKit routes
├── static/            # Static assets
└── package.json       # Dependencies and scripts
```


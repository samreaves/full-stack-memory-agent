# Stage 1: Build the SvelteKit application
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Build arguments for environment variables
ARG API_PROTOCOL=${API_PROTOCOL:-http}
ARG API_HOST=${API_HOST:-0.0.0.0}
ARG API_PORT=${API_PORT:-8000}
ARG CLIENT_PORT=${CLIENT_PORT:-5173}

# Set environment variables
ENV API_PROTOCOL=${API_PROTOCOL}
ENV API_HOST=${API_HOST}
ENV API_PORT=${API_PORT}
ENV CLIENT_PORT=${CLIENT_PORT}

# Build the application
RUN npm run build

# Stage 2: Serve the application
FROM node:20-alpine AS runner

WORKDIR /app

# Install serve for static file serving
RUN npm install -g serve

# Copy built files from builder
COPY --from=builder /app/build ./build

# Expose port
EXPOSE 5173

# Serve the built application
CMD ["sh", "-c", "serve -s build -l 5173"]


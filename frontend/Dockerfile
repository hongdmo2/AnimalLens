# Base image
FROM node:20-slim

# Install pnpm globally
RUN npm install -g pnpm

# Set working directory
WORKDIR /app

# Copy dependency files
COPY package.json pnpm-lock.yaml ./

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy application source code
COPY . .

# Set environment variable
ENV NODE_ENV=production

# Build application for production
RUN pnpm build || exit 0

# Default command for production
CMD ["pnpm", "start"]

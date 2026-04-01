FROM node:18-alpine

WORKDIR /app

RUN corepack enable

# Copy package files
COPY package.json ./

# Install dependencies
RUN pnpm install

# Copy application
COPY . .

# Build Next.js
RUN pnpm build

# Expose port
EXPOSE 3000

# Start Next.js
CMD ["pnpm", "start"]

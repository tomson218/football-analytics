FROM node:22-alpine
WORKDIR /app

COPY package.json pnpm-lock.yaml ./
RUN corepack enable && corepack prepare pnpm@latest --activate && pnpm install --frozen-lockfile

COPY . .

EXPOSE 5173
CMD ["pnpm", "run", "dev", "--host", "0.0.0.0"]
# Nuxt Minimal Starter

Look at the [Nuxt documentation](https://nuxt.com/docs/getting-started/introduction) to learn more.

## Quick start (Docker + Makefile)
Build & run container:
```bash
make docker-up
```

Foreground mode:
```bash
make docker-dev
```

Stop container:
```bash
make docker-down
```

Rebuild container:
```bash
make docker-fresh
```

## API Base URL
Salin env:
```bash
copy .env.example .env
```

Atur `NUXT_PUBLIC_API_BASE` sesuai backend (default `http://localhost:8000`).
Jika FE berjalan di Docker dan BE di host:
```
NUXT_PUBLIC_API_BASE=http://host.docker.internal:8000
```

## Setup

Make sure to install dependencies:

```bash
# npm
npm install

# pnpm
pnpm install

# yarn
yarn install

# bun
bun install
```

## Development Server

Start the development server on `http://localhost:3000`:

```bash
# npm
npm run dev

# pnpm
pnpm dev

# yarn
yarn dev

# bun
bun run dev
```

## Production

Build the application for production:

```bash
# npm
npm run build

# pnpm
pnpm build

# yarn
yarn build

# bun
bun run build
```

Locally preview production build:

```bash
# npm
npm run preview

# pnpm
pnpm preview

# yarn
yarn preview

# bun
bun run preview
```

Check out the [deployment documentation](https://nuxt.com/docs/getting-started/deployment) for more information.

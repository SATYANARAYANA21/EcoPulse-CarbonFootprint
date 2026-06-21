# Architecture Documentation

EcoPulse follows a decoupled client-server architecture:

## Frontend (React + Vite + Zustand)
- **Vite** for fast HMR and optimized production builds.
- **TailwindCSS** for responsive and consistent design systems.
- **Zustand** for lightweight state management.
- **Zod** for strict runtime validation.

## Backend (FastAPI + Python)
- **FastAPI** for high-performance async endpoint resolution.
- **Pydantic** for rigorous data validation.
- **Slowapi** for robust, proxy-safe rate-limiting.

## Deployment
- Deployed on **Vercel** via Serverless Functions.

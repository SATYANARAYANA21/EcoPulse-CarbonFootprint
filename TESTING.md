# Testing Strategy

We maintain a rigorous testing strategy with a strict **90% coverage** threshold across statements, branches, lines, and functions.

## Automated Testing
- **Frontend**: Vitest and React Testing Library. Includes `vitest-axe` for accessibility testing.
- **Backend**: Pytest with Coverage plugins for API endpoints and logical services.

## Running Tests
- Frontend: `cd frontend && npm run test`
- Backend: `cd backend && pytest --cov=app`

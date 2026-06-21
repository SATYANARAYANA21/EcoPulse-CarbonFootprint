# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability within EcoPulse, please send an e-mail to security@ecopulse.local instead of creating a public issue.

## Security Features
- **Strict ESLint Rules**: `security/detect-object-injection` and `no-control-regex` enforce secure coding practices.
- **Rate Limiting**: `slowapi` protects against DDoS by capping API requests per IP.
- **Input Validation**: `Zod` and `Pydantic` enforce strict schemas on all inbound data to prevent injection attacks.

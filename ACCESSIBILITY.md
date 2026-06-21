# Accessibility Guidelines (WCAG 2.1 AA)

EcoPulse is built to be inclusive and accessible to everyone.

- **Semantic HTML**: We use `<article>`, `<section>`, and `<nav>` elements appropriately.
- **ARIA Attributes**: `aria-live="polite"` is used for dynamic updates. `aria-hidden="true"` hides decorative SVGs and Emojis from screen readers.
- **Keyboard Navigation**: All interactive elements are fully focusable and outline styles are enforced.
- **Testing**: We use `eslint-plugin-jsx-a11y` and `vitest-axe` for automated accessibility audits.

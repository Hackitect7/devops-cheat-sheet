# Contributing

## Dev setup

- Install [Quarto] and run `quarto render` to build the site.
- Open `_site/index.html` locally to preview.

## Branching & commits

- Use topic branches: `feat/...`, `fix/...`, `docs/...`, `ci/...`
- Conventional Commit messages, e.g.:
  - `feat(k8s): add service mesh summary`
  - `fix(es-mx): correct kubectl flags`
  - `docs: add release process`
  - `ci: enable link checker`

## Pull requests

- One logical change per PR; reference issues with `Closes #123`.
- Ensure local render passes: `quarto render`.
- For content changes, run a link check if possible.

## i18n

- Source language: **en-US** (recommendation).
- Keep structure aligned across locales; mark untranslated sections with `TODO:`.

[Quarto]: https://quarto.org/

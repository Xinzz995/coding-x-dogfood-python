# Engineering rules

- Keep `packages/api` and `packages/worker` independently installable.
- Add or update tests whenever behavior changes.
- Do not add Node, npm, or coding-x commands to GitHub CI.
- All changes to `main` must go through a protected pull request.

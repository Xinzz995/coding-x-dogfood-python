# coding-x Python dogfood

Public, synthetic Python monorepo fixture used to verify that coding-x can initialize and enforce a GitHub quality gate without adding Node or coding-x to project CI.

This repository contains no production code, credentials, customer data, or unpublished coding-x package contents. It exists only as reproducible quality-gate evidence.

The repository contains two independently packaged projects:

- `packages/api`
- `packages/worker`

Each package must pass its own tests, wheel build, and Ruff checks.

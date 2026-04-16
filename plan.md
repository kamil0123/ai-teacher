# Python Project Best Practices — Learning Plan

A step-by-step guide to building a Python project the professional way.

---

## 1. Project Setup & Structure

### 1.1 Repository Initialization
- Create a new GitHub repository (public or private)
- Clone it locally
- Add a `.gitignore` for Python (templates available at [github.com/github/gitignore](https://github.com/github/gitignore))
- Add a `README.md` and `LICENSE`

### 1.2 Standard Directory Layout
Use the `src/` layout — put your package inside `src/my_package/`. This separates source code from tests, config, and tooling. Key files to include at the root: `pyproject.toml`, `Dockerfile`, `docker-compose.yml`, `.env.example`, `.gitignore`, `README.md`.

---

## 2. Python Environment Management

### 2.1 Python Version Management
- Use `pyenv` (Linux/macOS) or `pyenv-win` (Windows) to switch between Python versions per project
- Pin the version in a `.python-version` file so everyone on the team uses the same version

### 2.2 Virtual Environments
- Create an isolated environment for every project using the built-in `venv`, or the faster modern alternative `uv`
- Never commit the virtual environment folder — add it to `.gitignore`

### 2.3 Dependency Management
| Tool | Notes |
|------|-------|
| `pip` + `requirements.txt` | Simplest option, good starting point |
| `pip-tools` | Keeps transitive dependencies pinned and reproducible |
| `uv` | Fast modern tool that replaces pip and venv together |
| `poetry` | Full lifecycle management — install, build, publish |

**Recommended for learning:** start with `pip` + `requirements.txt`, then graduate to `uv` or `poetry`.

### 2.4 Secrets & Configuration
- Store secrets (API keys, passwords) in `.env` files — **never commit them**
- Provide a `.env.example` with placeholder values for other developers
- Load config via `python-dotenv` or `pydantic-settings`
- Follow the [12-factor app](https://12factor.net/config) principle: all config comes from environment variables

---

## 3. Code Quality

### 3.1 Linting & Formatting
- Use **Ruff** — a single fast tool that replaces `flake8` (linting), `black` (formatting), and `isort` (import sorting)
- Configure it in `pyproject.toml`

### 3.2 Type Checking
- Add type hints to all functions — they serve as inline documentation and catch bugs early
- Run **mypy** or **pyright** to statically verify types without running the code

### 3.3 Pre-commit Hooks
- Use the `pre-commit` framework to run quality checks automatically before every commit
- Hooks can run Ruff, mypy, and secret scanning without any manual steps

---

## 4. Testing

### 4.1 Framework
- Use **pytest** as the test framework — it is the standard in the Python community
- Add `pytest-cov` for coverage measurement and `pytest-mock` for mocking

### 4.2 Test Types to Learn
| Type | Purpose |
|------|---------|
| Unit tests | Test individual functions in isolation |
| Integration tests | Test components working together |
| Mocking | Replace external dependencies (APIs, DBs) with fakes |
| Coverage | Measure what percentage of code is tested |

### 4.3 Test Structure
Follow the **AAA pattern**: Arrange (set up data) → Act (call the function) → Assert (check the result). Keep each test focused on one thing.

### 4.4 Coverage Target
- Aim for >= 80% code coverage
- Coverage does not guarantee good tests — focus on meaningful assertions, not just the number

---

## 5. Version Control with Git

### 5.1 Branching Strategy (GitHub Flow)
- `main` is always deployable and protected
- Create short-lived feature branches (`feature/`, `fix/`, `chore/`) and merge them via pull requests

### 5.2 Commit Message Convention
Follow **Conventional Commits** — prefix every commit with a type: `feat:`, `fix:`, `docs:`, `test:`, `chore:`. This makes the history readable and enables automated changelog generation.

### 5.3 Pull Request Workflow
1. Create a branch from `main`
2. Write code and tests
3. Open a PR with a description
4. CI checks must pass before merging
5. Get a code review
6. Merge to `main`

---

## 6. GitHub CI/CD with GitHub Actions

### 6.1 Continuous Integration (CI)
- Set up a workflow that runs automatically on every push and pull request
- Standard CI pipeline: install dependencies → lint → type check → run tests → upload coverage
- Use **Codecov** to track coverage trends over time

### 6.2 Continuous Delivery (CD)
- On merge to `main` (or on a version tag), automatically build and push a Docker image to Docker Hub or GitHub Container Registry
- The CD pipeline only runs after CI passes

### 6.3 Best Practices
- Pin action versions (e.g. `@v4`) — never use `@latest`
- Store all secrets in GitHub → Settings → Secrets, never in workflow files
- Use matrix builds to test against multiple Python versions
- Cache dependencies to speed up builds

---

## 7. Docker

### 7.1 Dockerfile
- Use **multi-stage builds** — a build stage installs dependencies, a final stage contains only what is needed to run. This keeps images small and secure.
- Use slim base images (`python:3.12-slim`) and pin versions
- Run the app as a non-root user inside the container

### 7.2 docker-compose for Local Development
- Use `docker-compose` to run the app together with its dependencies (database, cache, etc.) locally with a single command
- Mount source code as a volume for fast feedback during development

### 7.3 .dockerignore
- Always add a `.dockerignore` file — exclude `.venv`, `.env`, `.git`, `tests/`, and `__pycache__`

---

## 8. Documentation

Documentation is **written alongside code**, not after. Every PR that changes behavior must update the relevant docs.

### 8.1 README.md
Every README should cover: what the project does, how to set it up, how to configure it (env variables), architecture overview, and how to contribute.

### 8.2 Docstrings
- Write docstrings for all public functions and classes (Google style is the most popular in Python)
- Enforce with `pydocstyle` or the `D` rule set in Ruff

### 8.3 Documentation Site
- Use **MkDocs** with the **mkdocs-material** theme for a professional documentation site
- Use **mkdocstrings** to auto-generate API reference pages from your docstrings
- Preview locally with `mkdocs serve`

### 8.4 Auto-deploy Docs to GitHub Pages
- Add a GitHub Actions workflow that runs `mkdocs gh-deploy` on every push to `main`
- Docs are then live at `https://<username>.github.io/<repo>/` automatically

### 8.5 CHANGELOG.md
- Maintain a `CHANGELOG.md` following the [Keep a Changelog](https://keepachangelog.com) format
- Add an entry for every PR under `[Unreleased]` and move it to a versioned section on release

### 8.6 Architecture Decision Records (ADRs)
- Store significant technical decisions in `docs/adr/` as plain Markdown files
- Template: context → decision → consequences
- Invaluable for understanding *why* something was built the way it was

### 8.7 CONTRIBUTING.md
- Document how to set up the dev environment, run tests, follow code style, and open PRs
- This is the first file a new contributor reads

### 8.8 Documentation Update Checklist (per PR)
- [ ] Docstrings updated for changed functions/classes
- [ ] `README.md` updated if setup or usage changed
- [ ] `CHANGELOG.md` entry added under `[Unreleased]`
- [ ] ADR created if a significant architecture decision was made

---

## 9. Security

### 9.1 Static Security Analysis (SAST)
- Use **Bandit** to scan Python code for common security mistakes (hardcoded passwords, dangerous function calls, etc.)
- Add it to the CI pipeline and pre-commit hooks

### 9.2 Dependency Vulnerability Scanning
- Use **pip-audit** to check all installed packages against known CVE databases
- Run it in CI so vulnerabilities are caught before deployment

### 9.3 Automated Dependency Updates
- Enable **GitHub Dependabot** by adding a config file — it automatically opens PRs to update outdated or vulnerable dependencies weekly

### 9.4 Secret Scanning
- Enable GitHub's built-in secret scanning (Settings → Security)
- Add the **detect-secrets** pre-commit hook to catch secrets before they ever get committed
- Never hardcode API keys, tokens, or passwords — use environment variables

### 9.5 Security Checklist
- [ ] No secrets in source code or commit history
- [ ] All dependencies audited for CVEs
- [ ] Bandit reports no high-severity issues
- [ ] Docker container runs as a non-root user
- [ ] Input is validated at all system boundaries

---

## 10. Logging & Observability

### 10.1 Structured Logging
- Never use `print()` in production code — use Python's `logging` module or **structlog**
- **structlog** outputs clean, structured JSON logs that are easy to search in log aggregation tools
- Use log levels appropriately: `DEBUG` in dev, `INFO` and above in production
- Never log sensitive data (passwords, tokens, PII)
- Control log level via an environment variable

### 10.2 Health Check Endpoint
- Every service should expose a `/health` endpoint that returns its status
- Used by Docker, load balancers, and Kubernetes to know when the app is ready

### 10.3 Metrics
- Use **prometheus-client** to expose application metrics (request counts, error rates, latency)
- Visualise with **Grafana** — both have free tiers and are industry standard

### 10.4 Error Tracking
- Integrate **Sentry** to automatically capture and report exceptions with full context
- Has a free tier; catches errors you would otherwise never see in production

---

## 11. Release Management & Versioning

### 11.1 Semantic Versioning (SemVer)
Use `MAJOR.MINOR.PATCH` versioning:
- **MAJOR** — breaking change
- **MINOR** — new feature, backward-compatible
- **PATCH** — bug fix

### 11.2 Managing Versions
- Store the version in `pyproject.toml`
- Use **bump-my-version** to increment it consistently across all files with a single command

### 11.3 Git Tags & GitHub Releases
- Tag every release with `git tag v1.0.0` and push the tag to GitHub
- Create a GitHub Release from the tag and paste the CHANGELOG entry as release notes
- Consider automating this with the **release-please** GitHub Action

### 11.4 Automated Release Pipeline
- Trigger Docker image builds and pushes on version tags (e.g. `v*.*.*`) in GitHub Actions
- Tag the Docker image with both `latest` and the specific version number

---

## 12. Developer Experience (DX)

### 12.1 Makefile / Justfile
- Provide a `Makefile` (or `justfile`) with short commands for all common tasks: `make install`, `make test`, `make lint`, `make docs`
- New contributors should be able to get started with just two commands

### 12.2 pyproject.toml
- Use `pyproject.toml` as the single config file for the project: metadata, dependencies, Ruff, mypy, pytest, and coverage settings all in one place
- Use a build backend like **hatchling** or **flit**
- Define a `dev` optional dependency group so dev tools are installed with `pip install -e ".[dev]"`

### 12.3 GitHub Templates
- Add a **pull request template** (`.github/pull_request_template.md`) with a standard checklist
- Add **issue templates** for bug reports and feature requests — GitHub has a built-in wizard for this

### 12.4 Branch Protection Rules
Configure on GitHub → Settings → Branches to protect `main`:
- Require a pull request before merging
- Require at least one approval
- Require all CI status checks to pass
- Disallow force pushes

---

## 13. Recommended Learning Order

| Step | Topic | Time estimate |
|------|-------|---------------|
| 1 | Git basics + GitHub Flow + branch protection | 1–2 days |
| 2 | Python env (venv, pip, pyproject.toml) | 1 day |
| 3 | Write a small CLI app in `src/` layout + Makefile | 2–3 days |
| 4 | Add pytest unit tests + coverage | 1–2 days |
| 5 | Add Ruff + mypy + pre-commit + detect-secrets | 1 day |
| 6 | Add structured logging with `structlog` | 1 day |
| 7 | Write GitHub Actions CI workflow (lint + test + audit) | 1–2 days |
| 8 | Containerize with Docker + docker-compose | 2–3 days |
| 9 | Add CD — push Docker image on version tags | 1 day |
| 10 | Add bandit + pip-audit + Dependabot | 1 day |
| 11 | Set up MkDocs + docstrings + CHANGELOG | 1–2 days |
| 12 | Auto-deploy docs to GitHub Pages | 1 day |
| 13 | Release management — SemVer + git tags + GitHub Releases | 1 day |
| 14 | Add integration tests + Sentry error tracking | 1–2 days |

---

## 14. Key Tools Summary

| Category | Recommended Tool |
|----------|------------------|
| Package manager | `uv` or `poetry` |
| Project config | `pyproject.toml` (hatchling backend) |
| Linter/Formatter | `ruff` |
| Type checker | `mypy` (strict mode) |
| Testing | `pytest` + `pytest-cov` + `pytest-mock` |
| Pre-commit hooks | `pre-commit` + `detect-secrets` |
| SAST | `bandit` |
| Dependency audit | `pip-audit` + GitHub Dependabot |
| Logging | `structlog` |
| Error tracking | `sentry-sdk` |
| CI/CD | GitHub Actions |
| Containerization | Docker (multi-stage) + docker-compose |
| Secrets | `.env` + `pydantic-settings` |
| Documentation | `mkdocs-material` + `mkdocstrings` |
| Versioning | `bump-my-version` + SemVer |
| Dev commands | `Makefile` or `just` |

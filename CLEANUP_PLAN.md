# Tech‑Debt Cleanup Plan

## Overview
This plan outlines the steps needed to clean up the current prototype, add tests, improve code quality, and set up CI. The session‑storage change has been omitted as requested.

---

## 1. Add Unit Tests
- Create a `tests/` directory.
- Write tests for:
  - FastAPI endpoints (`/chat`, `/health`, etc.) using `TestClient`.
  - Streaming logic (mock the LLM client to return a known stream).
- Use `pytest` fixtures for common setup.

## 2. Add Integration Tests
- Choose a headless browser tool (e.g., Playwright).
- Write tests that:
  - Open the app in a new browser context.
  - Verify session handling (if still relevant).
  - Send a chat message and assert streamed tokens appear in the UI.

## 3. Refactor Streaming Logic
- Extract streaming generator into a separate module (e.g., `app/streaming.py`).
- Use dependency injection (`Depends`) to inject the LLM client.
- Define a clear interface (`StreamingClient`) for easier mocking.

## 4. Add Type Hints & Linting
- Add type hints to all public functions and classes.
- Configure `mypy` in `pyproject.toml`.
- Run `ruff check . --fix` to auto‑format and lint.
- Optionally add a pre‑commit hook.

## 5. Document the API
- Ensure FastAPI’s automatic OpenAPI docs (`/docs`) are accessible.
- Add a README section explaining:
  - What the session ID is for (if still used).
  - How to start the server (`uvicorn main:app --reload`).
  - How to run tests.

## 6. CI Workflow
- Create `.github/workflows/ci.yml` that:
  - Checks out code.
  - Sets up Python (e.g., 3.11).
  - Installs dependencies (`pip install -r requirements.txt`).
  - Runs `pytest`, `ruff check`, and `mypy`.
- Add a status badge to the README.

## 7. Clean Up Unused Code
- Run `isort .` and `autoflake --in-place --remove-all-unused-imports -r .`.
- Review any remaining `print` statements or debug logs.

## 8. Environment Variable Handling
- Create a `.env.example` with placeholders for secrets (e.g., LLM API key).
- Use `python-dotenv` or FastAPI’s `BaseSettings` to load them.
- Add a note in the README about creating `.env`.

## 9. Final Documentation
- Update `README.md` to reflect all new features, tests, and usage instructions.
- Add a “Contributing” section with guidelines for running tests locally.

---

### Deliverables
1. **Unit & integration tests** covering core functionality.
2. **Refactored streaming module** with dependency injection.
3. **Type hints, linting, and formatting** in place.
4. **CI workflow** that runs tests, linting, and type checks.
5. **Updated README** with setup, run, test, and contribution instructions.

Feel free to adapt the plan as needed. Happy coding!

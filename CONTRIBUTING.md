# Contributing to Global API Project

Welcome! Global API Project is developed by an international university team. These guidelines help us write consistent Python code, review changes fairly, and keep the project reproducible.

For Git commands and instructions for committing and pushing from a terminal or the GitHub interface, see [GITHUB.md](GITHUB.md). Read the [README](README.md) for project setup and usage.

## 1. Working language and collaboration

- Use English for code, comments, documentation, commit messages, issues, and pull requests so every team member can participate.
- Write clearly and respectfully. Explain technical terms when useful, and ask questions when requirements are unclear.
- Discuss substantial architectural changes in an issue before implementing them. Record decisions in the repository so absent teammates can catch up.
- Agree on an owner and acceptance criteria for each task. Keep issues updated and report blockers early.
- Allow for different time zones and class schedules. Include a time zone when arranging meetings or deadlines, and avoid expecting immediate replies.
- Review the code, not the person. Give specific, constructive feedback and acknowledge contributions.
- Follow university rules for academic integrity, attribution, third-party code, and AI assistance. Contributors remain responsible for understanding, verifying, and explaining submitted work.

## 2. Contribution workflow

1. Read the README, this guide, and any applicable security or assignment instructions.
2. Find or open an issue describing the problem and expected outcome. Small typo fixes may go directly to a pull request.
3. Update your local `main` branch and create a task branch.
4. Make a focused change, add appropriate tests, and update documentation.
5. Run the repository's formatting, linting, and test checks.
6. Commit using Conventional Commits and push your branch.
7. Open a pull request, request a review, and address feedback.
8. Merge after approval and required checks pass; delete the merged task branch.

The commands below assume a checkout with an `origin` remote and a shared `main` branch. Use the repository's documented workflow if its configuration differs. Contributors without write access should use a fork and open a pull request against the original repository.

```bash
git switch main
git pull --ff-only origin main
git switch -c feat/42-user-search

# Make changes and run checks, then stage only the intended files.
git add src/global_api/services/user_service.py tests/unit/test_user_service.py
git diff --staged
git commit -m "feat(users): add search by display name"
git push -u origin feat/42-user-search
```

For changes made through GitHub's web interface, create a task branch and submit a pull request. Use the same naming and review rules as terminal contributions.

## 3. Branch conventions

- Keep `main` stable and ready for the team's documented build and test process.
- Submit changes through pull requests; do not push directly to `main`.
- Use short-lived branches with the pattern `<type>/<issue-number>-<short-description>`.
- Use lowercase letters, digits, and hyphens in the description. Omit the issue number when no issue exists.
- Recommended types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, and `ci`.

Examples:

```text
feat/42-user-search
fix/57-invalid-token
docs/contribution-guide
test/61-user-validation
```

Keep branches synchronized with `main` using the team's agreed merge or rebase workflow. Coordinate before rewriting shared history. Never force-push to `main`; if a rebase requires updating your own branch, use `git push --force-with-lease` after checking that nobody else depends on it.

## 4. Commit conventions: Conventional Commits

Use this structure:

```text
<type>[optional scope][!]: <description>

[optional body]

[optional footer(s)]
```

| Type | Use for |
| --- | --- |
| `feat` | A new feature |
| `fix` | A bug fix |
| `docs` | Documentation changes |
| `style` | Formatting changes without behavior changes |
| `refactor` | Code restructuring without a feature or bug fix |
| `test` | Adding or improving tests |
| `perf` | Performance improvements |
| `build` | Dependencies or build configuration |
| `ci` | Continuous integration changes |
| `chore` | Other maintenance |
| `revert` | Reverting an earlier change |

- Write the description in English, in the imperative: “add,” “fix,” or “remove.”
- Prefer a lowercase opening word, no final period, and a subject of 72 characters or fewer.
- Use a short, consistent scope when helpful, such as `auth`, `users`, `api`, or `docs`.
- Keep each commit focused on one logical change. Avoid messages such as `update`, `stuff`, or `final version`.
- Explain the reason for a change in the body when it is not obvious.
- Mark breaking changes with `!` after the type or scope, or a `BREAKING CHANGE:` footer. Explain migration steps.
- Reference related issues in the body or footer. Use closing keywords only when the change fully resolves the issue.

```text
feat(users): add search by display name
fix(auth): reject expired access tokens
docs(setup): explain local environment variables
test(users): cover duplicate email addresses
```

Example breaking change:

```text
feat(api)!: rename the user identifier field

Use user_id consistently across user responses.

BREAKING CHANGE: clients must read user_id instead of id.
Closes #42
```

Use the same convention for pull request titles, especially when squash merging.

## 5. Python naming conventions

| Item | Convention | Example |
| --- | --- | --- |
| Python files/modules | `snake_case.py` | `user_service.py` |
| Package folders | Short lowercase names; underscores if needed | `services`, `api_clients` |
| Other project folders | Lowercase; follow the existing structure | `docs`, `tests` |
| Functions and methods | `snake_case` | `get_user_by_id()` |
| Variables and parameters | `snake_case` | `user_id`, `retry_count` |
| Classes and exceptions | `PascalCase` | `UserService`, `UserNotFoundError` |
| Module-level constants | `UPPER_SNAKE_CASE` | `DEFAULT_TIMEOUT_SECONDS` |
| Internal implementation details | Leading underscore | `_normalize_email()` |
| Test files and functions | `test_` prefix | `test_user_service.py`, `test_missing_user()` |

Choose descriptive English names. Avoid spaces, accents, ambiguous abbreviations, and names that shadow built-ins, such as `list` or `id`. Do not name modules after standard libraries or dependencies, such as `json.py` or `pytest.py`. Reserve double-underscore names for Python-defined behavior.

## 6. Project structure

Follow the existing repository layout. For new components, the following is the recommended structure; it is an example, not a claim that every file already exists:

```text
global-api-project/
├── src/
│   └── global_api/
│       ├── __init__.py
│       ├── main.py
│       ├── api/              # Routes and request/response handling
│       ├── services/         # Business rules and use cases
│       ├── models/           # Domain or persistence models
│       ├── schemas/          # Input/output validation schemas
│       ├── repositories/     # Data access
│       └── core/             # Configuration and shared infrastructure
├── tests/
│   ├── unit/
│   └── integration/
├── docs/
├── .github/
│   └── workflows/
├── .env.example
├── .gitignore
├── pyproject.toml
├── README.md
├── GITHUB.md
└── CONTRIBUTING.md
```

Keep API handlers thin, business logic in services, and storage access in repositories. Add abstractions when they serve a clear purpose. Avoid circular imports, duplicate helpers, and unrelated code in generic utility modules. Use `__init__.py` where required by the project's package strategy. Do not reorganize the entire repository as part of an unrelated feature.

## 7. Code style, formatting, and documentation

- Follow PEP 8 and use four spaces for indentation; do not use tabs.
- Add type hints to new or changed public functions and methods. Use the Python version declared by the project.
- Prefer small functions with one clear responsibility and explicit error handling. Avoid bare `except:` clauses and silently swallowing failures.
- Use the repository's formatter and linter configuration as the source of truth. Recommended defaults for a new setup are Ruff for linting and formatting, with an 88-character line length.
- Keep imports organized with the configured tools. Avoid wildcard imports.
- Write comments to explain intent, constraints, or non-obvious decisions. Keep them accurate when code changes.
- Update the README or `docs/` whenever setup, configuration, API behavior, or usage changes. Include migration instructions for incompatible changes.

### Docstrings

Use Google-style docstrings for public modules, classes, and functions. Start with a short summary. Add `Args`, `Returns`, and `Raises` sections when they help explain the interface; omit sections that do not apply. Document behavior and constraints rather than repeating type annotations.

```python
DEFAULT_PAGE_SIZE = 20


def validate_page_size(page_size: int) -> int:
    """Validate the number of records requested per page.

    Args:
        page_size: Requested number of records, from 1 to 100 inclusive.

    Returns:
        The validated page size.

    Raises:
        ValueError: If page_size is outside the supported range.
    """
    if not 1 <= page_size <= 100:
        raise ValueError("page_size must be between 1 and 100")
    return page_size
```

## 8. Tests and local checks

- Use the test framework configured by the project; pytest is the recommended default.
- Add tests for new behavior and regression tests for bug fixes.
- Cover expected behavior, boundary conditions, invalid inputs, and relevant error paths. For API changes, cover status codes, response schemas, and authorization where applicable.
- Keep unit tests fast, deterministic, and isolated. Replace external services with controlled test doubles where appropriate.
- Run integration tests against isolated test resources. Never use production credentials or real personal data.
- Name tests after the behavior being verified, and use fixtures for reusable setup.
- Follow any coverage threshold configured in CI. Prioritize meaningful assertions over a coverage percentage.

Example test for the function above (assuming it lives in `global_api/services/pagination.py`):

```python
import pytest

from global_api.services.pagination import validate_page_size


@pytest.mark.parametrize("page_size", [1, 20, 100])
def test_validate_page_size_accepts_supported_values(page_size: int) -> None:
    assert validate_page_size(page_size) == page_size


@pytest.mark.parametrize("page_size", [0, -1, 101])
def test_validate_page_size_rejects_unsupported_values(page_size: int) -> None:
    with pytest.raises(ValueError, match="between 1 and 100"):
        validate_page_size(page_size)
```

If Ruff and pytest are configured and installed in the project environment, run:

```bash
python -m ruff check .
python -m ruff format --check .
python -m pytest
```

To apply formatting locally, use `python -m ruff format .`, then inspect the changes. Use the exact installation commands, test options, and additional checks documented in the README and CI configuration. Do not introduce a second formatter or change shared rules without team agreement.

## 9. Pull requests and reviews

- Keep each pull request focused and reasonably small. Separate unrelated cleanup from functional changes.
- Open a draft pull request early when feedback would help.
- Include the problem, the approach, related issues, and how the change was verified.
- Describe API, configuration, dependency, or database changes and any migration steps. Include request/response examples when useful.
- Request at least one review from another team member. Do not approve your own work.
- Resolve review discussions and obtain approval before merging. Re-request review after substantial changes.
- All required CI checks must pass. Do not bypass failing checks without a documented team decision.
- Prefer squash merging with a Conventional Commit title unless the team has agreed on another strategy.
- Repository maintainers should configure branch protection and required reviews/checks to enforce these expectations.

Suggested pull request description:

```markdown
## Purpose
Explain the problem and expected behavior.

## Changes
- Describe the main changes.

## Verification
- List checks run and their results, or explain what could not be tested.

## Compatibility and migration
Describe breaking changes or write "None."

## Related issue
Closes #<issue-number>
```

Before requesting review:

- [ ] My change matches the issue and contains no unrelated edits.
- [ ] Naming, docstrings, and commit messages follow this guide.
- [ ] Relevant tests are added or updated and local checks pass.
- [ ] Documentation and configuration examples are updated.
- [ ] No secrets, personal data, or generated clutter are included.
- [ ] Breaking changes and limitations are clearly described.

## 10. Security and repository hygiene

- Never commit passwords, API keys, tokens, private keys, `.env` files, or real personal data. Keep safe placeholders in `.env.example` and exclude local secrets through `.gitignore`.
- If a secret is exposed, notify the responsible maintainer privately and revoke or rotate it immediately. Deleting it in a later commit does not remove it from Git history; coordinate any necessary history cleanup.
- Report suspected vulnerabilities through the private channel documented in `SECURITY.md`, if present. Otherwise contact a maintainer privately through the team's established channel. Avoid publishing exploit details in a public issue.
- Validate external input, enforce authorization, use parameterized database queries, and avoid exposing sensitive information in logs or error responses.
- Keep dependencies necessary and reproducible using the project's dependency and lock-file policy. Review new dependencies and their licenses.
- Do not commit virtual environments, caches, build outputs, editor-specific clutter, or large datasets unless explicitly required. Track shared editor settings only when the team agrees.
- Respect third-party licenses, attribute reused work, and use synthetic or anonymized test data.

## 11. Maintaining these guidelines

Propose changes to this guide through a pull request. Explain the benefit and allow the team to discuss workflow changes before adopting them. Keep this document, [GITHUB.md](GITHUB.md), the README, and automated checks consistent.

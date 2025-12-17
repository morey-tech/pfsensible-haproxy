# Development Guidelines for AI Agents

This document provides guidelines for AI agents (like Claude Code) working on the pfsensible.haproxy Ansible collection to ensure consistency and quality.

## Documentation Maintenance

### Keeping Module Documentation Up to Date

When making changes to modules, always update the corresponding documentation:

1. **Module Changes** - If you modify a module's DOCUMENTATION, EXAMPLES, or RETURN blocks in `plugins/modules/*.py`, you must update the corresponding markdown file in `docs/modules/*.md`

2. **New Modules** - When adding a new module:
   - Create the module file in `plugins/modules/`
   - Create the module utils file in `plugins/module_utils/` if needed
   - Create the documentation file in `docs/modules/` using the template below
   - Update the README.md modules section to include the new module
   - Create unit tests in `tests/units/modules/`

3. **Documentation Template** - All module documentation files follow this structure:

```markdown
# [module_name]

[short_description]

## Synopsis

- [description points]

## Parameters

| Parameter | Type | Required | Default | Choices | Description |
|-----------|------|----------|---------|---------|-------------|
| param1 | str | yes | - | - | Description |

## Examples

```yaml
[EXAMPLES block verbatim from module]
```

## Return Values

| Key | Type | Returned | Description | Sample |
|-----|------|----------|-------------|--------|
| commands | list | always | Description | `["sample"]` |

## Author

- [Author Name] (@github-handle)

## Version

Added in version X.Y.Z
```

4. **Documentation Extraction** - Extract documentation directly from the module's DOCUMENTATION, EXAMPLES, and RETURN blocks. Do not invent or assume parameters.

## Commit Message Guidelines

Use [Conventional Commits](https://www.conventionalcommits.org/) format for all commits:

### Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that don't affect code meaning (formatting, whitespace, etc.)
- **refactor**: Code change that neither fixes a bug nor adds a feature
- **perf**: Performance improvement
- **test**: Adding missing tests or correcting existing tests
- **chore**: Changes to build process or auxiliary tools

### Scopes

Common scopes for this project:
- **backend**: Backend module changes
- **backend_server**: Backend server module changes
- **frontend**: Frontend module changes
- **frontend_server**: Frontend server module changes
- **ci**: CI/CD workflow changes
- **deps**: Dependency updates
- **dev**: Developer tooling (devcontainer, pre-commit, etc.)

### Examples

```bash
# Adding a new feature
feat(frontend): add support for custom error pages

# Fixing a bug
fix(backend_server): correct SSL verification parameter handling

# Updating documentation
docs(modules): update frontend module examples

# CI/CD changes
ci: add Python 3.11 to test matrix

# Refactoring code
refactor(backend): simplify health check configuration logic
```

### Breaking Changes

If a commit introduces breaking changes, add `BREAKING CHANGE:` in the footer:

```
feat(backend): change default balance algorithm

BREAKING CHANGE: The default balance algorithm is now 'roundrobin' instead of 'none'
```

### AI Agent Attribution

**IMPORTANT**: Do not include AI attribution in commit messages.

- **Do NOT add** "Generated with Claude Code" or similar attribution
- **Do NOT add** "Co-Authored-By: Claude" trailers
- Commits should appear as standard human contributions
- Keep commit messages clean and focused on the actual changes

**Bad Example:**
```bash
feat(frontend): add SSL certificate support

🤖 Generated with Claude Code

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Good Example:**
```bash
feat(frontend): add SSL certificate support
```

## Feature Branch Workflow

Always use feature branches for development work:

### Branch Naming Convention

```
<type>/<short-description>
```

**Types:**
- `feature/` - New features or enhancements
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions or updates

**Examples:**
```
feature/add_haproxy_frontend
fix/backend-ssl-verification
docs/update-installation-guide
refactor/simplify-health-checks
test/add-frontend-unit-tests
```

### Workflow Steps

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/my-new-feature
   ```

2. **Make Changes**
   - Write code
   - Update documentation
   - Add/update tests
   - Run pre-commit hooks locally: `pre-commit run --all-files`

3. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat(scope): add new feature"
   ```

   Pre-commit hooks will automatically run. If they fail, fix the issues and commit again.

4. **Push to Remote**
   ```bash
   git push origin feature/my-new-feature
   ```

5. **Create Pull Request**
   - Create PR against `main` branch
   - GitHub Actions will automatically run PR checks
   - Ensure all checks pass before requesting review

6. **After Merge**
   - Delete the feature branch
   - Pull latest changes from main

### Branch Protection

The `main` branch should be protected with:
- Required status checks (PR Checks job must pass)
- No direct pushes (all changes via PR)
- Up-to-date branches required

## Testing Requirements

Before committing, ensure:

1. **Code Style** - Run pycodestyle: `pycodestyle plugins/ tests/`
2. **Sanity Tests** - Run ansible-test sanity: `ansible-test sanity --requirements --python 3.10`
3. **Unit Tests** - Run ansible-test units: `ansible-test units --requirements --python 3.10`

These are automatically enforced by pre-commit hooks and GitHub Actions.

## Module Development Checklist

When creating or modifying modules:

- [ ] Module file in `plugins/modules/`
- [ ] Module utils file in `plugins/module_utils/` (if needed)
- [ ] Unit tests in `tests/units/modules/`
- [ ] Documentation file in `docs/modules/`
- [ ] README.md modules section updated
- [ ] DOCUMENTATION block complete and accurate
- [ ] EXAMPLES block with common use cases
- [ ] RETURN block documenting return values
- [ ] All tests passing (pycodestyle, sanity, units)
- [ ] Conventional commit message
- [ ] Feature branch used

## Additional Resources

- [Ansible Module Development](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html)
- [ansible-test Documentation](https://docs.ansible.com/ansible/latest/dev_guide/testing.html)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Pre-commit Framework](https://pre-commit.com/)

## Questions?

If you have questions or need clarification on these guidelines, please open an issue in the GitHub repository.

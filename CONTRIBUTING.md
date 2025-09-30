# Contributing to Django E-commerce Portal

First off, thank you for considering contributing to our e-commerce platform! It's people like you that make this project such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

- Use a clear and descriptive title
- Describe the exact steps to reproduce the problem
- Provide specific examples to demonstrate the steps
- Describe the behavior you observed after following the steps
- Explain which behavior you expected to see instead and why
- Include screenshots if possible
- Include error messages and stack traces if applicable

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please provide:

- Use a clear and descriptive title
- Provide a step-by-step description of the suggested enhancement
- Provide specific examples to demonstrate the steps
- Describe the current behavior and explain which behavior you expected to see instead
- Explain why this enhancement would be useful
- List some other e-commerce sites or applications where this enhancement exists

### Pull Requests

- Fill in the required template
- Do not include issue numbers in the PR title
- Follow the Python style guide
- Include screenshots in your pull request whenever possible
- Update the documentation accordingly
- End all files with a newline
- Follow the commit message conventions

## Development Process

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code lints
6. Issue that pull request!

### Local Development Setup

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
npm install
```

3. Set up pre-commit hooks:

```bash
pre-commit install
```

### Running Tests

```bash
python manage.py test
```

### Code Style

This project uses:

- Black for Python code formatting
- isort for import sorting
- flake8 for linting
- prettier for JavaScript/CSS formatting

Run the formatters:

```bash
black .
isort .
flake8
prettier --write .
```

## Documentation

### Python Docstrings

Use Google-style docstrings:

```python
def function_name(param1: type, param2: type) -> return_type:
    """Short description.

    Longer description if needed.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: Description of when this error occurs
    """
    pass
```

### JavaScript Documentation

Use JSDoc for JavaScript documentation:

```javascript
/**
 * Function description
 * @param {string} param1 - Parameter description
 * @param {number} param2 - Parameter description
 * @returns {boolean} Description of return value
 */
function functionName(param1, param2) {
  return true;
}
```

## Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line
- Consider starting the commit message with an applicable emoji:
  - 🎨 `:art:` when improving the format/structure of the code
  - 🐎 `:racehorse:` when improving performance
  - 🚱 `:non-potable_water:` when plugging memory leaks
  - 📝 `:memo:` when writing docs
  - 🐛 `:bug:` when fixing a bug
  - 🔥 `:fire:` when removing code or files
  - 💚 `:green_heart:` when fixing the CI build
  - ✅ `:white_check_mark:` when adding tests
  - 🔒 `:lock:` when dealing with security
  - ⬆️ `:arrow_up:` when upgrading dependencies
  - ⬇️ `:arrow_down:` when downgrading dependencies

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](link-to-tags).

## Review Process

The core team reviews Pull Requests on a regular basis. After feedback has been given we expect responses within two weeks. After two weeks we may close the pull request if it isn't showing any activity.

## Community

- Join our [Discord server](link-to-discord)
- Follow us on [Twitter](link-to-twitter)
- Read our [Blog](link-to-blog)

## Questions?

Don't hesitate to contact the project maintainers if you have any questions or need help!

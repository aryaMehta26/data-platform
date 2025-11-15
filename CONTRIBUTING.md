## Contributing

### Development setup
- Python 3.10+
- Docker Desktop

### Workflow
1. Create a feature branch
2. Make changes with tests
3. Run tests locally: `cd api && pytest -q`
4. Push and open a PR; CI runs tests and builds images

### Coding standards
- Python: meaningful names, guard clauses, handle errors explicitly
- Keep functions small and focused; add docstrings for non-trivial logic
- Ensure FastAPI endpoints return JSON and are covered by tests

### Commit messages
- Use concise, imperative style: "Add DQ validators for ranges"



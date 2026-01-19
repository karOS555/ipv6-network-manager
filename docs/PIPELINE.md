# CI/CD Pipeline Documentation

## Workflow
The project utilizes GitHub Actions for Continuous Integration.

## Triggers
* **Push:** Every push to the `main` branch triggers the build.
* **Pull Request:** Every PR targeting `main` triggers the build.

## Stages
1. **Setup:** Installs Python 3.10 and upgrades `pip`.
2. **Dependency Check:** Installs `flake8`, `pytest`, `streamlit`, `docker`, `paramiko`.
3. **Linting:** Runs `flake8` to ensure code quality and PEP8 compliance.
4. **Testing:** Runs `pytest` to verify database integrity and basic logic functions.
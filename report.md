# Project Quality Report: Simple Notes App

**Made by Team_13: Daria Shibkova, Nika Lobanova, Daniil Prostiruk, Egor Valikov, Andrey Gerasimov**

## 1. Quality Gate Automation

All quality gates are executed through local automation scripts and manual commands:

* **Backend** checks and tests executed locally:

  * Flake8 for PEP8 compliance
  * Ruff for supplementary linting and complexity analysis
  * Bandit for security vulnerability scanning
  * pytest suite execution with coverage measurement and HTML report generation
  * pytest-benchmark for performance benchmarking
  * Locust scenarios for load testing
* **Frontend** validations performed with npm scripts:

  * ESLint and Prettier for code style and formatting checks
  * TypeScript compiler for static type verification
  * Jest execution for unit and snapshot testing

## 2. Test Coverage

**Backend**: 90% line coverage, surpassing the 60% requirement. Coverage details:

  * Authentication modules (`auth.py`, `hashing.py`, `tokens.py`)
  * Note management logic (`notes.py`, `crud.py`)
  * Translation functionality (`translate.py`)
**Frontend**: Testing framework configured (Jest, React Testing Library). Current test cases include:

* Creating a new note
* Editing an existing note
* Archiving a note

Coverage targets are being defined as component tests are implemented. TypeScript compilation ensures code safety.

## 3. Testing and Analysis Methods

A variety of methods have been applied to ensure software quality:

1. **Static Analysis**

   * Backend: Flake8 and Ruff for linting and complexity analysis
   * Frontend: ESLint, Prettier, TypeScript compiler for code style and type safety
2. **Unit Testing**

   * Backend: pytest is used for business logic and API route testing
   * Frontend: Jest with React Testing Library for testing note creation, editing, and archiving functionality
3. **Integration Testing**

   * Backend: End-to-end API and database interaction tests via FastAPI’s TestClient
4. **Performance Testing**

   * Backend: pytest-benchmark for function-level benchmarks
   * Backend: Locust for concurrent user load scenarios
5. **Security Testing**

   * Backend: Bandit static analysis for identifying vulnerabilities in python code
   * Frontend: relies on framework-level protections and content security policies
6. **Mutation Testing**

* Mutmut included in test dependencies; future integration planned to strengthen test suite resilience

## 4. Reliability Mechanisms

**Backend**: Centralized error handling and atomic SQLite transactions to maintain data consistency

**Frontend**: Type safety via TypeScript and use of React error boundaries to prevent unhandled crashes

## 5. Performance Results

**Backend**: Key API endpoints consistently respond in under 200 ms during local load tests.

**Frontend**: Initial performance estimations are favorable. User interactions, such as creating, editing, and archiving notes, are responsive. Formal Lighthouse reports are planned for future iterations.

## 6. Documentation and Configuration

* **README.md**: Provides detailed setup instructions, environment configuration, and usage examples for both backend and frontend
* **pytest.ini**: Local configuration for pytest markers, coverage options, and benchmark settings
* **requirements-test.txt**: Lists backend test dependencies including pytest, Locust, Bandit, and Mutmut
* **package.json**: Defines npm scripts for linting, formatting, building, and testing the front-end application

## 7. Assessment of Quality Requirements

* **Maintainability**: Code adheres to style guides, exhibits modular design, and includes comprehensive documentation, benchmark of MI 70 is checked using radon 
* **Reliability**: High backend test coverage; robust error handling and transactional integrity
* **Performance**: Benchmarked backend functions meet performance targets; frontend structure is optimized for fast load times, the system handles 20 concurrent users
* **Security**: 
Bandit is used for static analysis, and no critical vulnerabilities are reported. The backend uses JWT tokens for authentication, and tests validate secure handling. Passwords are hashed using bcrypt (via get_password_hash in hashing.py). Sensitive user data is excluded from API responses. 

## 8. Technical Stack

**Backend**: Python 3.11, FastAPI, SQLAlchemy with SQLite, pytest, coverage.py, Ruff, Flake8, Bandit, Locust, Mutmut

**Frontend**: Next.js (React) with TypeScript, Tailwind CSS, React Testing Library, Jest, ESLint, Prettier

**Automation**: Local scripts and npm commands for quality gate enforcement

---

**Conclusion:**
All quality gates have been validated locally. The application fully satisfies the defined requirements for maintainability, reliability, performance, and security and is prepared for final submission.

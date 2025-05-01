## FastAPI Backend Architecture Plan

This architecture emphasizes modularity, testability, and scalability, leveraging FastAPI's features like dependency injection, Pydantic models, and asynchronous support.

**1. Directory Structure:**

```
/teacherly-backend
├── app/
│   ├── __init__.py
│   ├── api/                     # API Routers (Endpoints)
│   │   ├── __init__.py
│   │   ├── deps.py              # Dependency injection functions (get_db, get_current_user)
│   │   └── v1/                  # API Version 1
│   │       ├── __init__.py
│   │       ├── endpoints/       # Individual feature routers
│   │       │   ├── __init__.py
│   │       │   ├── auth.py
│   │       │   ├── users.py     # (Admin/Teacher/Self-management endpoints)
│   │       │   ├── content_generation.py
│   │       │   ├── grading.py
│   │       │   ├── students.py
│   │       │   ├── attendance.py
│   │       │   ├── reports.py
│   │       │   └── settings.py
│   │       └── api.py           # Aggregates all v1 routers
│   │
│   ├── core/                    # Core logic, settings, security
│   │   ├── __init__.py
│   │   ├── config.py            # Application settings (from .env)
│   │   └── security.py          # Password hashing, JWT handling, RBAC checks
│   │
│   ├── crud/                    # Data Access Layer (CRUD operations)
│   │   ├── __init__.py
│   │   ├── base.py              # Base CRUD class (optional)
│   │   ├── crud_user.py
│   │   ├── crud_student.py
│   │   ├── crud_content.py
│   │   ├── crud_grade.py
│   │   ├── crud_attendance.py
│   │   └── crud_report.py       # (Maybe not direct CRUD, but data retrieval for reports)
│   │
│   ├── db/                      # Database setup and session management
│   │   ├── __init__.py
│   │   ├── base_class.py        # Base for ORM models
│   │   ├── database.py          # Engine, SessionLocal setup (PostgreSQL)
│   │   └── vector_db.py         # Connection/client setup for Vector DB
│   │
│   ├── models/                  # ORM Database Models (e.g., SQLAlchemy)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── teacher.py           # (Could be part of user or separate if complex)
│   │   ├── student.py
│   │   ├── content.py           # Base content, QuizExam, TeachingMaterial inherit
│   │   ├── grade.py
│   │   ├── attendance.py
│   │   └── report.py            # (Maybe track report generation jobs/metadata)
│   │
│   ├── schemas/                 # Pydantic Schemas (API data validation)
│   │   ├── __init__.py
│   │   ├── token.py
│   │   ├── user.py
│   │   ├── student.py
│   │   ├── content.py
│   │   ├── grade.py
│   │   ├── attendance.py
│   │   ├── report.py
│   │   └── msg.py               # Generic message responses
│   │
│   ├── services/                # Business Logic Layer
│   │   ├── __init__.py
│   │   ├── auth_service.py      # Handles login logic
│   │   ├── generation_service.py # Orchestrates RAG, LLM for content
│   │   ├── grading_service.py   # Orchestrates OCR, LLM for grading
│   │   ├── report_service.py    # Handles report generation, formatting, emailing
│   │   └── attendance_service.py # Logic for attendance processing
│   │
│   ├── ai/                      # AI Integration Modules
│   │   ├── __init__.py
│   │   ├── llm_interface.py     # Interface with Google Gemini (fine-tuned)
│   │   ├── rag_interface.py     # Interface with Vector DB for context retrieval
│   │   └── ocr_interface.py     # Interface with external OCR API
│   │
│   ├── exceptions/              # Custom Exception classes
│   │   ├── __init__.py
│   │   └── custom_exceptions.py # Define domain-specific exceptions
│   │
│   └── utils/                   # Utility functions
│       ├── __init__.py
│       ├── email_sender.py      # Email sending logic
│       └── file_handler.py      # Handling uploads/temp files for OCR
│
├── tests/                     # Unit and Integration Tests
│   ├── __init__.py
│   ├── conftest.py            # Pytest fixtures
│   ├── api/
│   │   └── v1/
│   ├── crud/
│   ├── services/
│   └── utils/
│
├── .env                       # Environment variables (DB URLs, API Keys, Secret Key)
├── .gitignore
├── main.py                    # FastAPI app entry point
├── requirements.txt
└── README.md
```

**2. Core Concepts & Flow:**

*   **Entry Point (`main.py`):** Initializes the FastAPI app, includes the main API router (`app.api.v1.api.router`), sets up CORS middleware, **registers custom exception handlers**.
*   **API Routers (`app/api/v1/endpoints/`):** Define path operations (`@router.post`, `@router.get`, etc.). Use Pydantic schemas (`app/schemas/`) for request body validation and response models. Use `Depends` to inject dependencies like DB sessions and the current authenticated user (`app/api/deps.py`). Routers primarily call `Service` layer functions. **RBAC checks** can be implemented via dependencies or within endpoints.
*   **Dependencies (`app/api/deps.py`):** Functions to provide dependencies like `get_db()` (yields a DB session) and `get_current_active_user()` (validates JWT token from `app/core/security.py` and retrieves user from DB via `app/crud/crud_user.py`). Dependencies can also handle role checks.
*   **Services (`app/services/`):** Contain the core business logic. They orchestrate calls to CRUD functions (`app/crud/`), AI interfaces (`app/ai/`), and utilities (`app/utils/`). Example: `grading_service.py` would receive data from the router, call `ocr_interface.py`, `llm_interface.py`, `crud_grade.py` to save results, and **ensure robust cleanup of transient data**. Use `BackgroundTasks` here for long-running AI operations.
*   **CRUD (`app/crud/`):** Functions that interact directly with the database via the ORM models (`app/models/`). They perform basic Create, Read, Update, Delete operations. Keep business logic minimal here.
*   **Models (`app/models/`):** Define the database tables using an ORM like SQLAlchemy, reflecting the ERD. Include relationships. **Implement encryption for sensitive fields (e.g., using SQLAlchemy types or extensions)**.
*   **Schemas (`app/schemas/`):** Pydantic models defining the expected structure of API request and response data. Ensures data validation.
*   **AI Interfaces (`app/ai/`):** Abstract away the direct calls to external AI APIs (Gemini, OCR) and the Vector DB. Handle prompt formatting, API key management (via `config.py`), and response parsing.
*   **Core (`app/core/`):** Handles configuration loading (`config.py` reads `.env`) and security functions (`security.py` handles password hashing, JWT creation/validation).
*   **Database (`app/db/`):** Manages database connections (PostgreSQL engine/sessions, Vector DB client).
*   **Exceptions (`app/exceptions/`):** Define custom, domain-specific exception classes (`custom_exceptions.py`) for clearer error handling.
*   **Async:** Leverage `async def` for path operations, services, and CRUD functions, especially when dealing with I/O (DB calls, external API calls).

**3. Key Technologies:**

*   **Framework:** FastAPI
*   **Data Validation:** Pydantic
*   **Database ORM (PostgreSQL):** SQLAlchemy (recommended)
*   **Field Encryption (PostgreSQL):** Libraries like `sqlalchemy-utils` or custom SQLAlchemy Types with encryption logic.
*   **Vector Database Client:** Specific client library (e.g., `pinecone-client`, `qdrant-client`, `pgvector` if using Postgres extension)
*   **Password Hashing:** `passlib` with bcrypt
*   **JWT:** `python-jose`
*   **Background Tasks:** FastAPI's built-in `BackgroundTasks`
*   **Migrations:** Alembic (for SQLAlchemy)
*   **Testing:** `pytest`, `httpx` (for async API testing)
*   **Environment Variables:** `python-dotenv`, `pydantic-settings`

---

## Detailed Step-by-Step Backend TODO List

This list assumes a sequential build, starting with foundations and adding features iteratively.

**Phase 1: Project Setup & Core Foundations**

1.  **Initialize Project:**
    *   Create project directory (`teacherly-backend`).
    *   Set up a virtual environment (`python -m venv venv`).
    *   Activate virtual environment.
    *   Create `requirements.txt`.
    *   Install FastAPI and Uvicorn: `pip install fastapi uvicorn[standard]`
2.  **Basic FastAPI App:**
    *   Create `main.py` with a basic FastAPI app instance.
    *   Add a root health check endpoint (`/`).
    *   Run the app using `uvicorn main:app --reload`.
3.  **Directory Structure:** Create the folders outlined in the architecture plan, including `app/exceptions/`. Add `__init__.py` files where needed.
4.  **Configuration:**
    *   Install `python-dotenv` and `pydantic-settings`.
    *   Create `.env` file (add to `.gitignore`). Define initial variables (e.g., `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`, `ENCRYPTION_KEY`).
    *   Implement `app/core/config.py` using Pydantic's `BaseSettings` to load environment variables.
5.  **Database Setup (PostgreSQL):**
    *   Install SQLAlchemy, psycopg2-binary (or asyncpg for async), Alembic, and potentially `sqlalchemy-utils` for encryption: `pip install sqlalchemy "psycopg2-binary" alembic asyncpg sqlalchemy-utils`
    *   Add `DATABASE_URL` to `.env`.
    *   Implement `app/db/database.py` (engine, `SessionLocal`).
    *   Implement `app/db/base_class.py` (declarative base).
    *   Setup Alembic for migrations (`alembic init alembic`). Configure `alembic.ini` and `env.py`.
6.  **Database Setup (Vector DB):**
    *   Choose a Vector DB (e.g., Pinecone, Qdrant, Weaviate, Milvus, pgvector).
    *   Install the corresponding Python client library.
    *   Add Vector DB connection details/API keys to `.env`.
    *   Implement `app/db/vector_db.py` for client initialization and connection.

**Phase 2: Authentication & User Management**

7.  **Security Implementation:**
    *   Install `passlib[bcrypt]` and `python-jose[cryptography]`.
    *   Implement password hashing functions in `app/core/security.py`.
    *   Implement JWT token creation (`create_access_token`) and decoding/validation logic in `app/core/security.py`.
8.  **User Model & Schema:**
    *   Define `User` model in `app/models/user.py` (using SQLAlchemy). Include fields like `id`, `email`, `hashed_password`, `role` (e.g., using `Enum`), `is_active`.
    *   Define `UserCreate`, `UserRead`, `UserUpdate` schemas in `app/schemas/user.py`.
    *   Define `Token` and `TokenData` schemas in `app/schemas/token.py`.
9.  **User CRUD:** Implement `app/crud/crud_user.py` (functions: `get_user`, `get_user_by_email`, `create_user`, `update_user`, `authenticate_user`).
10. **Dependency Injection:**
    *   Implement `get_db` dependency in `app/api/deps.py`.
    *   Implement `get_current_user` dependency (using OAuth2PasswordBearer and token validation) in `app/api/deps.py`. Add `get_current_active_user` variant. **Add optional role checking parameters/dependencies here if needed for RBAC.**
11. **Authentication Endpoints:**
    *   Implement `app/api/v1/endpoints/auth.py`.
    *   Add `/login/access-token` endpoint (using `OAuth2PasswordRequestForm`, calls `crud_user.authenticate_user`, creates JWT).
    *   Add `/users/signup` endpoint (or similar, calls `crud_user.create_user`).
    *   Add `/users/me` endpoint (protected, uses `get_current_active_user` to return user info).
12. **API Router Setup:**
    *   Aggregate auth/user routers in `app/api/v1/api.py`.
    *   Include the v1 router in `main.py`.
13. **Initial Migrations:** Create initial Alembic migration for the User model (`alembic revision --autogenerate -m "Add user table"`) and apply it (`alembic upgrade head`).
14. **Testing (Auth):** Write basic unit tests for security functions and CRUD operations. Write integration tests for login and signup endpoints.

**Phase 3: Feature Implementation (Iterative)**

*(Repeat steps 15-21 for each major feature: Content Generation, Student Management, Grading, Attendance, Reporting)*

15. **Models & Schemas:**
    *   Define necessary ORM models (`app/models/`) based on the ERD (e.g., `Student`, `Content`, `Grade`, `Attendance`). Establish relationships (ForeignKeys, relationships).
    *   **Implement encryption for sensitive fields** (e.g., `student.parent_email`, `grade.score` if required) using appropriate types (e.g., `sqlalchemy_utils.types.EncryptedType`) configured with `ENCRYPTION_KEY` from `config.py`.
    *   Define corresponding Pydantic schemas (`app/schemas/`) for API requests and responses (e.g., `StudentCreate`, `GradeRead`, `ContentGenerateRequest`).
16. **CRUD Implementation:** Create/update CRUD modules (`app/crud/`) with functions to interact with the new models (e.g., `create_student`, `get_grades_by_student`, `save_generated_content`). Handle encrypted fields appropriately during read/write.
17. **AI Interface Implementation (If applicable):**
    *   Implement functions in `app/ai/` to interact with relevant external services (LLM, RAG, OCR). Load API keys from `config.py`. Handle potential errors from external APIs gracefully.
18. **Service Layer Logic:**
    *   Implement business logic in the corresponding service module (`app/services/`).
    *   Orchestrate calls to CRUD, AI interfaces, and utilities.
    *   Use `BackgroundTasks` for long operations (e.g., `grading_service.grade_submission`, `generation_service.generate_exam`).
19. **API Endpoints:**
    *   Implement the feature's router in `app/api/v1/endpoints/`.
    *   Define path operations, use schemas, inject dependencies (`db`, `current_user`, `BackgroundTasks`).
    *   Protect endpoints requiring authentication using `Depends(get_current_active_user)`.
    *   Implement Role-Based Access Control (RBAC) checks within endpoints or dependencies (e.g., using `Depends(get_current_active_user_with_role('teacher'))`). Check ownership where necessary (e.g., teacher accessing their own students/content).
20. **Custom Exceptions:** Define feature-specific exceptions in `app/exceptions/custom_exceptions.py` (e.g., `StudentNotFoundError`, `GradeProcessingError`). Raise these in Service/CRUD layers.
21. **Migrations & Testing:**
    *   Generate Alembic migrations for new/updated models (including encrypted fields). Apply migrations.
    *   Write unit tests for CRUD and Service logic, including tests for encryption/decryption and RBAC logic.
    *   Write integration tests for the new API endpoints, testing different roles and ownership scenarios.

**Specific Feature Considerations:**

*   **Content Generation:** Needs RAG integration (query Vector DB in `rag_interface.py`, pass context to `llm_interface.py`).
*   **Grading:** Needs file handling (`app/utils/file_handler.py` for temp storage), OCR call (`ocr_interface.py`), LLM call (`llm_interface.py`), background task processing. Store transient OCR text temporarily if needed. **Ensure the background task robustly deletes transient OCR data (e.g., using `try...finally`) after processing, even if LLM grading fails.**
*   **Reporting:** Needs data aggregation logic (likely in `report_service.py`), Excel file generation (e.g., using `openpyxl` or `pandas`), email integration (`app/utils/email_sender.py`).
*   **Attendance:** Straightforward CRUD, potentially some aggregation logic for reporting.
*   **Student Management:** Standard CRUD operations. Ensure teachers can only manage *their* students (add authorization logic). **Ensure parent\_email encryption is handled correctly.**

**Phase 4: Supporting Features & Refinements**

22. **Settings Endpoints:** Implement endpoints in `app/api/v1/endpoints/settings.py` for profile updates, password changes, 2FA management (requires additional libraries like `pyotp`).
23. **Email Utility:** Implement `app/utils/email_sender.py` using an email service provider (e.g., SendGrid, Mailgun) or SMTP. Configure credentials in `.env`.
24. **Error Handling:**
    *   Implement custom exception handlers in `main.py` (using `@app.exception_handler()`) for custom exceptions defined in `app/exceptions/` and potentially for generic FastAPI/Starlette exceptions (like `RequestValidationError`, `HTTPException`).
    *   Ensure handlers return consistent JSON error responses.
25. **Middleware:** Add CORS middleware in `main.py`. Consider adding logging middleware.
26. **Refine RBAC & Admin Functionality:**
    *   Review and ensure appropriate authorization checks (role-based and ownership-based) are consistently applied across all relevant endpoints.
    *   **If required:** Implement specific admin-only endpoints in `app/api/v1/endpoints/users.py` (or a dedicated `admin.py`) for tasks like listing all users, managing roles, etc., protected by admin role checks in dependencies.

**Phase 5: Testing & Documentation**

27. **Comprehensive Testing:** Increase test coverage for unit and integration tests. Test edge cases, error conditions, encrypted field handling, and RBAC scenarios thoroughly.
28. **API Documentation:** Review and enhance the auto-generated Swagger UI/ReDoc documentation by adding detailed descriptions, examples, security scheme definitions (`OAuth2PasswordBearer`), and tags to endpoints and schemas.
29. **README Update:** Update `README.md` with setup instructions, environment variable explanations (including `ENCRYPTION_KEY`), how to run the app, how to run tests, and **a note explaining that RAG data ingestion (embedding curriculum/resources into the Vector DB) is a separate process not handled by this runtime API.**

**Phase 6: Deployment Preparation**

30. **Dockerization:** Create `Dockerfile` and potentially `docker-compose.yml` for easier development setup and deployment.
31. **Production Settings:** Configure settings for production (e.g., logging levels, database URLs, disable debug mode, securely manage `ENCRYPTION_KEY`).
32. **Dependency Management:** Freeze final dependencies (`pip freeze > requirements.txt`).
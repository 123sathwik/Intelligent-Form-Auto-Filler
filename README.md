# Intelligent Form Auto-Filler

An enterprise-grade, scalable AI-powered application designed to automate form population from documents (PDF, DOCX, JPG, JPEG, PNG) through OCR, NLP, and Intelligent Key-Value Mapping.

## Technical Architecture

This repository uses a multi-module clean architecture containing decoupled folders for Frontend, Backend, Machine Learning, and configuration modules.


User
   │
   ▼
Select Form Type
   │
   ▼
Upload PDF / DOCX / Image
   │
   ▼
OCR
   │
   ▼
Text Cleaning
   │
   ▼
Entity Extraction
   │
   ▼
JSON Standardization
   │
   ▼
Semantic Field Mapping
   │
   ▼
Dynamic Form Generation
   │
   ▼
Auto Fill
   │
   ▼
Review & Edit
   │
   ▼
Submit / Export

```
.
├── .github/                   # GitHub CI/CD configurations
├── dataset/                   # Local raw dataset files (Git ignored)
├── models/                    # Shared serialized model registry (Git ignored)
├── firebase/                  # Firebase auth, rules, and configuration files
├── docs/                      # Documentation, ADRs, and API schemas
├── tests/                     # Integration and system tests
├── scripts/                   # Deployment and helper scripts
├── docker/                    # Dockerfiles for frontend, backend, and ml
├── frontend/                  # React + TypeScript + Tailwind UI
├── backend/                   # FastAPI backend
└── ml/                        # ML Pipeline (data prep, training, evaluation)
```

---

## Folder Guide & Explanations

### 1. Root Directories

*   **`dataset/`**: Local repository for storing raw, processed, and split dataset files (PDFs, DOCX, Images) used for training ML models. This folder is ignored in Git to prevent checking in large/sensitive binary data.
*   **`models/`**: Dedicated local storage for model checkpoints, weights, and serialized configurations (e.g., PyTorch, ONNX, HuggingFace transformers). Git ignored.
*   **`firebase/`**: Contains configurations, security rules (`firestore.rules`, `storage.rules`), and settings for Firebase Authentication and Database integration.
*   **`docs/`**: Holds technical documentation, Architectural Decision Records (ADRs), user manuals, system diagrams, and specifications.
*   **`tests/`**: Contains cross-module integration tests, end-to-end tests, and system verification tests.
*   **`scripts/`**: Automation scripts for setting up dev environments, building containers, cleaning caches, and handling database migrations.
*   **`docker/`**: Contains dockerfiles (`frontend.Dockerfile`, `backend.Dockerfile`, `ml.Dockerfile`) for consistent containerization.
*   **`.github/`**: House workflows for CI/CD pipeline automation (e.g., linting, tests, automated deployment).

---

### 2. Frontend Directory (`frontend/`)
Built with **React**, **TypeScript**, **Vite**, and **Tailwind CSS**.

*   **`src/components/`**: Reusable visual components (e.g., Buttons, Inputs, Dialogs, Dropdowns, PDF Viewers).
*   **`src/pages/`**: View/page routes representing logical app views (e.g., Dashboard, Upload, FormReview).
*   **`src/layouts/`**: Layout containers defining global layout frames (e.g., MainLayout, DashboardLayout).
*   **`src/hooks/`**: Custom React hooks encapsulation (e.g., `useAuth`, `useFormFiller`).
*   **`src/services/`**: API wrapper classes communicating with backend service endpoints.
*   **`src/contexts/`**: React Context providers for managing global state (e.g., ThemeContext, FormContext).
*   **`src/utils/`**: Shared helper utilities (e.g., validators, converters, date formatters).
*   **`src/types/`**: TypeScript interfaces and custom types for API models and client-side structures.
*   **`src/assets/`**: Static visual assets like logos, default icons, and illustrations.
*   **`src/styles/`**: Custom design styles and tailwind styling configurations (e.g., `index.css`).
*   **`src/config/`**: Configuration constants, environmental variables, and Firebase client initialization.

---

### 3. Backend Directory (`backend/`)
Built with **FastAPI** (Python), implementing Clean Architecture / Domain-Driven Design principles.

*   **`app/api/`**: FastAPI routing definitions exposing HTTP/WebSocket endpoints grouped by module.
*   **`app/controllers/`**: Coordinates requests, validates models, and routes control flow to application service layers.
*   **`app/services/`**: Core application logic layer. Orchestrates business procedures.
*   **`app/repositories/`**: Data Access Objects (DAOs) interfacing with relational or Document databases.
*   **`app/models/`**: Database schema declarations (e.g., SQLAlchemy ORM models).
*   **`app/schemas/`**: Pydantic schemas defining request/response structures and validations.
*   **`app/middlewares/`**: CORS, Security, Logging, and request timing interceptors.
*   **`app/database/`**: Engine instantiation, session managers, and migrations setup.
*   **`app/config/`**: Pydantic BaseSettings loading configs from environment variables.
*   **`app/utils/`**: Utilities for encryption, logging, and general utility functions.
*   **`app/ocr/`**: Optical Character Recognition modules encapsulating document parsing libraries.
*   **`app/nlp/`**: Natural Language Processing and Named Entity Recognition pipeline wrappers.
*   **`app/ml/`**: Inference execution wrappers hosting models for mapping predictions.
*   **`app/core/`**: Critical system logic, exception handlers, security dependencies, and authorization filters.

---

### 4. ML Pipeline Directory (`ml/`)
Designed for development, training, and deployment of custom OCR and document parsing models.

*   **`ml/training/`**: Training pipelines, scripts, hyperparameter tuning logs, and loss plotting functions.
*   **`ml/evaluation/`**: Performance metrics validators (F1, Precision, Recall, Confusion Matrices).
*   **`ml/preprocessing/`**: File conversion, image resizing, cleaning, skew corrections, and splitting.
*   **`ml/saved_models/`**: Stashes for model checkpoints and binary exports ready for deployment.
*   **`ml/datasets/`**: Script utilities to fetch, cache, and structure datasets (e.g., receipt data, forms data).

---

## Local Development Setup

To set up the development environment, configure the global environment as described:

1. Clone repository
2. Set up environments: `cp .env.example .env`
3. Spin up local containers: `docker-compose up --build`

### Python Dependency Management

Python dependencies are modularized into three separate logical files inside the `backend/` directory:

1. **[requirements-base.txt](file:///c:/Users/Admin/OneDrive/auto%20filler/backend/requirements-base.txt)**: Contains only packages required to run the core FastAPI backend.
2. **[requirements-ocr.txt](file:///c:/Users/Admin/OneDrive/auto%20filler/backend/requirements-ocr.txt)**: Contains OCR-related libraries (e.g., easyocr, PyMuPDF, pdfplumber, Pillow).
3. **[requirements-ml.txt](file:///c:/Users/Admin/OneDrive/auto%20filler/backend/requirements-ml.txt)**: Contains AI/ML packages (e.g., PyTorch, Transformers, Sentence-Transformers, pandas, numpy, torchvision).

#### Installation Instructions

Depending on what part of the system you are developing, you can install the specific dependencies inside your Python environment:

* **FastAPI Backend only**:
  ```bash
  pip install -r backend/requirements-base.txt
  ```
* **FastAPI Backend with OCR capabilities**:
  ```bash
  pip install -r backend/requirements-base.txt -r backend/requirements-ocr.txt
  ```
* **FastAPI Backend with ML capabilities**:
  ```bash
  pip install -r backend/requirements-base.txt -r backend/requirements-ml.txt
  ```
* **Full Stack / ML Pipeline development (All Dependencies)**:
  ```bash
  pip install -r requirements.txt
  ```

#### Running the Backend Locally (Without Docker)

To run the backend server locally inside a Python virtual environment:

1. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```
2. **Create and activate a virtual environment**:
   * On Windows:
     ```powershell
     python -m venv .venv
     .venv\Scripts\activate
     ```
   * On macOS/Linux:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
3. **Install the base dependencies**:
   ```bash
   pip install -r requirements-base.txt
   ```
4. **Configure environment variables**:
   Create a `.env` file from the template (if not already done):
   ```bash
   cp .env.example .env
   ```
5. **Start the FastAPI backend with Uvicorn**:
   ```bash
   python -m uvicorn app.main:app --reload --port 8000
   ```
   The backend API will be available at `http://localhost:8000` and the interactive API documentation at `http://localhost:8000/docs`.



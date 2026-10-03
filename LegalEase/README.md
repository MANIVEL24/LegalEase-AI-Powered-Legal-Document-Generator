# LegalEase

LegalEase is an AI-powered legal-document drafting application based on the supplied project specification. It uses:

- Streamlit frontend
- FastAPI backend
- Google Gemini through the `google-genai` SDK
- python-docx for DOCX
- fpdf2 for PDF
- plain TXT export

The supplied specification calls for Gemini 1.5 Pro and the older `google-generativeai` SDK. This implementation keeps the requested architecture but uses Google's current `google-genai` client package. The model is configurable through `.env`.

## 1. Requirements

- Python 3.11 recommended
- VS Code
- Internet connection for Gemini API calls
- A Gemini API key for live AI mode

The application can also run in DEMO_MODE without an API key.

## 2. Create the environment

### Windows PowerShell

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### Windows CMD

```cmd
py -3.11 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
```

## 3. Configure Gemini

Open `.env`.

For live Gemini mode:

```env
GEMINI_API_KEY=YOUR_KEY_HERE
GEMINI_MODEL=gemini-2.5-flash
DEMO_MODE=false
```

If no key is available yet:

```env
GEMINI_API_KEY=
GEMINI_MODEL=gemini-2.5-flash
DEMO_MODE=true
```

Never commit `.env` to source control.

## 4. Run the application

Open two VS Code terminals.

### Terminal 1 - FastAPI

```powershell
.\.venv\Scripts\Activate.ps1
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Check:

- http://127.0.0.1:8000/
- http://127.0.0.1:8000/health
- http://127.0.0.1:8000/docs

### Terminal 2 - Streamlit

```powershell
.\.venv\Scripts\Activate.ps1
streamlit run frontend/app.py
```

Open the URL printed by Streamlit, normally:

http://localhost:8501

## 5. Test

From the project root:

```powershell
pytest -q
```

The tests cover:

- FastAPI root and health endpoints
- Document generation
- Text sanitization
- HTML preview
- DOCX generation
- PDF generation

## 6. Workflow

1. Enter document type.
2. Enter the parties.
3. Enter terms separated by semicolons.
4. Select the effective date.
5. Generate.
6. Review/edit the generated draft.
7. Download TXT, DOCX, or PDF.

## 7. Project structure

```text
LegalEase/
├── backend/
│   ├── main.py
│   ├── routes.py
│   ├── schemas.py
│   ├── config.py
│   ├── ai_core/
│   │   └── gemini_generator.py
│   └── formatters/
│       ├── common.py
│       ├── docx_formatter.py
│       └── pdf_formatter.py
├── frontend/
│   └── app.py
├── tests/
│   ├── test_api.py
│   └── test_formatters.py
├── assets/
│   └── logo.png
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## 8. Legal safety

This application produces AI-generated drafts. It does not establish that a document is legally valid for a particular jurisdiction, and it does not replace legal advice. Users should review generated documents and obtain professional legal advice where appropriate.

## 9. Troubleshooting

### `ModuleNotFoundError`

Activate `.venv` and run:

```powershell
pip install -r requirements.txt
```

### Streamlit cannot reach backend

Make sure the FastAPI terminal is running on port 8000. In the Streamlit sidebar, verify the Backend URL is:

```text
http://127.0.0.1:8000
```

### Gemini errors

Verify:

- `GEMINI_API_KEY` is present
- the API key is valid
- `GEMINI_MODEL` names a model available to your API account
- your network permits the Gemini API connection

Set `DEMO_MODE=true` to verify the application and exporters independently of Gemini.

### PDF export problems

This project uses `fpdf2`. If an older `fpdf` package is installed in the same environment, uninstall it and reinstall from requirements:

```powershell
pip uninstall -y fpdf
pip install -r requirements.txt
```

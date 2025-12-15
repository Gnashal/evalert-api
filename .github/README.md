# EV Alert Backend - Template Matching

This is a **real-time EV (Emergency Vehicle) alert backend** using **template matching** on audio signals.  
The backend receives audio buffers from an Android app (or any client) over WebSockets, performs **Spectral Flux + FFT Matching** and returns detection alerts.

---

## **Setup Instructions**

### 1. Clone / download this repository

```
git clone <your_repo_url>
cd ev-detect-backend
```

### 2. Create a Python virtual environment

```
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

#### Running the Backend Server

```
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Server will automatically load templates on startup.

#### WebSocket endpoint: ws://<host>:8000/ws/detect

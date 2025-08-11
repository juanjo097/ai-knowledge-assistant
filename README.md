# AI Knowledge Assistant (MVP)

Monorepo for an AI-powered knowledge assistant. Users can **upload** a file (TXT/CSV), **chat** grounded on that file, and **save answers as notes**. Includes **JWT authentication**, a **Flask** backend with **FAISS** indexing, and a **React + TypeScript + Vite + MUI** frontend.

---

## Features

- **Auth (JWT)**: Minimal login, protected routes.
- **Upload**: TXT/CSV → normalize → chunk → embed → index (**FAISS**).
- **Chat**: Ask questions grounded on the indexed content.
- **Notes**: Save and list notes from chat answers.
- **Clean architecture**: Separated routes/services/middlewares on backend; feature-first on frontend.
- **Persistence**: Frontend stores chat history per `docId` in `localStorage`.

---

## Architecture Overview

```
          +-------------------+
          |     Frontend      |
          | React + TS + Vite |
          | Material UI v7    |
          +---------+---------+
                    |
             HTTPS / fetch
                    |
     +--------------v---------------+
     |            Backend           |
     |        Flask (Python)        |
     |  Routes / Services / MWs     |
     |  - /auth (JWT)               |
     |  - /notes (CRUD subset)      |
     |  - /chat (RAG ask)           |
     +--------------+---------------+
                    |
            Embeddings / Index
                    |
            +-------v-------+
            |   FAISS CPU   |
            | Vector store  |
            +---------------+
```

---

## Repository Layout

```
/
├─ backend/
│  ├─ app/
│  │  ├─ routes/            # auth_routes.py, notes_routes.py, (chat routes)
│  │  ├─ services/          # auth_service.py, notes_repo.py, embedding_service.py, ...
│  │  ├─ middlewares/       # auth_middleware.py
│  │  └─ __init__.py        # create_app(), CORS, blueprint registration
│  ├─ data/                 # local storage (e.g., notes.json)
│  ├─ run.py                # app entrypoint
│  ├─ requirements.txt
│  └─ .env.example
│
├─ frontend/
│  ├─ src/
│  │  ├─ app/               # App.tsx, AppHeader.tsx, DocContext.tsx
│  │  ├─ features/
│  │  │  ├─ auth/           # LoginPage.tsx, auth.ts
│  │  │  ├─ upload/         # uploadCard.tsx
│  │  │  ├─ chat/           # ChatPanel.tsx, ChatInput.tsx, useChat.ts, MessageBubble.tsx
│  │  │  └─ notes/          # NotesList.tsx, NotesPreview.tsx
│  │  ├─ pages/             # Home.tsx
│  │  └─ shared/            # api/http.ts, hooks, ui, theme
│  ├─ index.html
│  ├─ package.json
│  └─ .env.example
│
└─ README.md (this file)
```

---

## Prerequisites

- **Python** 3.10+
- **Node.js** 18+ and **npm** 9+

Recommended: a virtual environment for Python (`venv`).

---

## Local Development

### 1) Backend

```bash
cd backend

# (once) create & activate venv
python -m venv venv
source venv/bin/activate           # Windows: venv\Scripts\activate

# install deps
pip install -r requirements.txt

# copy env and edit values
cp .env.example .env

# run
python run.py
# app on http://localhost:5000
```

**Backend .env example**
```bash
# Authentication
ADMIN_USER=admin
ADMIN_PASS=supersecreto123
JWT_SECRET=change-me
JWT_EXPIRES_MIN=120
OPENAI_API_KEY=""

# (Optional) LLM provider keys, if your chat service calls an external LLM
# OPENAI_API_KEY=...
```

### 2) Frontend

```bash
cd frontend

# install deps
npm install

# copy env and edit values
cp .env.example .env

# dev server
npm run dev
# app on http://localhost:5173
```

**Frontend .env example**
```bash
VITE_API_BASE=http://localhost:5000
# optional override if backend uses a different chat path (e.g., /ask)
VITE_CHAT_PATH=/chat
```

---

## API Reference (MVP)

### Auth
**POST** `/auth/login`  
Request:
```json
{ "username": "admin", "password": "supersecreto123" }
```
Response:
```json
{ "token": "<JWT>" }
```
> Attach the token to subsequent requests as `Authorization: Bearer <JWT>`.

### Notes
**GET** `/notes?limit=10&offset=0` → list notes  
**POST** `/notes` → create a note  
Request:
```json
{ "content": "Note content" }
```
Response:
```json
{ "id": "uuid", "content": "Note content", "createdAt": "2025-08-10T15:30:00Z" }
```

### Chat (RAG)
**POST** `/chat` *(or `/ask` if configured)*  
Request:
```json
{ "doc_id": 1, "message": "What are the key points?" }
```
Response (one of these fields will contain the text):
```json
{ "answer": "..." } 
```
or
```json
{ "message": "..."} 
```

### Health
**GET** `/health` → `{ "ok": true }`

---

## Frontend Notes

- Protected routes: `/`, `/chat`, `/notes`. Public: `/login`.
- Token is stored in `localStorage` and injected by `src/shared/api/http.ts`.
- Chat history is persisted per `docId` (key: `chat:<docId>`).  
  Switching `docId` switches the conversation context/history automatically.

---

## CORS & Security

- Backend must allow CORS for the frontend origin.
- Allow headers: `Authorization, Content-Type`.
- Respond `200` to `OPTIONS` preflight.
- Auth middleware should **skip** `OPTIONS` and allow `/auth/login` and `/health`.

---

## Deployment

- **Frontend**: `npm run build` → deploy `dist/` to static hosting (Vercel, Netlify, Nginx).
- **Backend**: deploy Flask app behind HTTPS (Gunicorn/Uvicorn + reverse proxy, or a managed platform).
- Update envs:
  - Frontend `VITE_API_BASE` to your backend URL.
  - Backend CORS `origins` to your frontend domain(s).

---

## Troubleshooting

- **401 on /notes**: Check CORS preflight and that `Authorization` header is allowed. Ensure auth middleware ignores `OPTIONS`.
- **Empty chat answers**: Verify payload `{ doc_id, message }` and that the index/embeddings exist for the uploaded file.
- **Double slashes in URLs**: Ensure `VITE_API_BASE` has no trailing slash.
- **Messages disappear**: Ensure you’re using `useChat.ts` with `usePersistentState` keyed by `docId`.

---

## Roadmap

- Notes: search, filters, pagination
- Chat: streaming responses, regenerate, copy, citations
- Upload: size limits, progress per chunk, supported formats
- Tests: unit (pytest / Vitest), E2E (Playwright), CI
- Observability: request logs, timings, error boundary

---

## License

Internal / project use.

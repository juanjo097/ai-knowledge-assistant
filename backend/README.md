# AI Knowledge Assistant — Backend (RAG + Tool)

Small backend that powers a mini AI knowledge assistant using **RAG** (Retrieval‑Augmented Generation) and exposes a simple **tool** to persist notes.

## Features (MVP)

- Upload TXT/CSV → normalize + dedupe by checksum.
- Chunking with overlap.
- Embeddings (OpenAI) and per‑document **FAISS** index.
- Chat endpoint that answers **grounded** on retrieved chunks (RAG) and cites chunk ids.
- Tool endpoint to **create/list notes**.
- "Fast path" **pipeline** endpoint to do upload→chunk→index in a single request.

---

## Project structure

```
backend/
├─ start.sh                 # one‑command local run (make it executable)
├─ run.py                   # dev entrypoint (Flask app factory)
├─ requirements.txt
├─ .env.example             # copy to .env and fill values
├─ .gitignore
├─ README.md
├─ data/                    # runtime data (git‑ignored): SQLite, docs, FAISS
└─ app/
   ├─ __init__.py           # create_app(), health, register routes/errors
   ├─ config.py             # Settings.from_env() + DATA_DIR bootstrap
   ├─ db.py                 # SQLAlchemy engine/session init
   ├─ models.py             # Document, Chunk, Note
   ├─ errors.py             # ApiError + JSON error handlers
   ├─ openai_client.py      # OpenAI client factory
   ├─ utils/
   │  └─ text.py            # normalize_text(), sha256_hex()
   ├─ repos/
   │  ├─ document_repo.py
   │  └─ chunk_repo.py
   ├─ services/
   │  ├─ ingestion_service.py   # upload → normalize → save
   │  ├─ chunk_service.py       # chunk building
   │  ├─ embedding_service.py   # embeddings + FAISS index
   │  ├─ rag_service.py         # retrieve + prompt + LLM answer
   │  └─ notes_service.py       # tool: create/list notes
   ├─ vectorstore/
   │  └─ faiss_store.py         # save/load/search FAISS per doc
   └─ routes/
      ├─ upload_routes.py       # POST /upload
      ├─ chunk_routes.py        # POST /chunks/build
      ├─ index_routes.py        # POST /index/build
      ├─ chat_routes.py         # POST /chat
      ├─ tools_routes.py        # POST /tools/create_note, GET /tools/notes
      └─ pipeline_routes.py     # POST /pipeline/ingest, POST /pipeline/process/:id
```

> Note: `data/` location is controlled by `DATA_DIR` (default `./data`). Ensure the folder exists or let the app create it.

---

## Environment variables

Copy `.env.example` → `.env` and fill as needed.

- `OPENAI_API_KEY` (required)
- `DB_URL` (default `sqlite:///./data/app.db`)
- `DATA_DIR` (default `./data`)
- `CORS_ORIGINS` (default `*` for dev)
- `EMBEDDING_MODEL` (default `text-embedding-3-small`)
- `LLM_MODEL` (default `gpt-4o-mini`)
- `TOP_K` (default `5`)
- `CHUNK_SIZE` (default `800`) and `CHUNK_OVERLAP` (default `120`)
- `MAX_UPLOAD_MB` (default `5`)
- `LOG_LEVEL` (default `INFO`)
- `ALLOWED_EXT` (default `txt,csv`)

---

## How to run (with `start.sh`)
1. Make sure you have Python 3.10+.
2. Copy env: `cp .env.example .env` and set `OPENAI_API_KEY`.
3. Make the script executable: `chmod +x start.sh`.
4. Run: `./start.sh`.
5. Health check: open `http://localhost:5000/health`.

> **Note:** The `./start.sh` script will automatically install dependencies from `requirements.txt`; no extra steps needed.

> **Tip:** If `start.sh` creates a venv, keep using it for subsequent runs; if not, install deps once with `pip install -r requirements.txt`.

---

## Quickstart (manual, without script)

```bash
# 1) Create venv and install deps
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2) Env vars
cp .env.example .env
# edit .env and set OPENAI_API_KEY

# 3) Run
python run.py
```

Then hit `http://localhost:5000/health`.

---

## API overview

**Granular endpoints** (great for debugging):

- `POST /upload` — form‑data `file`: save normalized text and create `Document`.
- `POST /chunks/build` — JSON `{ doc_id }`: build chunks for that document.
- `POST /index/build` — JSON `{ doc_id }`: build embeddings + FAISS index for that document.
- `POST /chat` — JSON `{ doc_id, message }`: RAG answer with `[chunk ids]` in sources.
- `POST /tools/create_note` — JSON `{ title, content }`: persist a note.
- `GET /tools/notes` — list recent notes.

**Pipeline endpoints** (fast path for the frontend):

- `POST /pipeline/ingest` — form‑data `file`: upload → chunk → index in one shot.
- `POST /pipeline/process/<doc_id>` — rebuild chunks + index for an existing doc.

---

## Smoke tests (curl)

```bash
# One‑shot ingest (returns doc_id)
curl -F "file=@/absolute/path/to/test.txt" http://localhost:5000/pipeline/ingest

# Ask a question
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"doc_id": 1, "message": "How do I clean the filter?"}'

# Create a note
curl -X POST http://localhost:5000/tools/create_note \
  -H "Content-Type: application/json" \
  -d '{"title":"Demo","content":"Saved from chat"}'

# List notes
curl http://localhost:5000/tools/notes
```

---

## Why both granular endpoints *and* a pipeline?

- **Maintainability & testability:** pinpoint failures by stage and retry only the broken part.
- **Selective reprocessing:** tweak chunk params or embedding model without re‑uploading files.
- **Cost control:** avoid recomputing embeddings when content is unchanged (checksum).
- **Scalability path:** each stage can become an async job later.
- **UX:** pipeline is perfect for the frontend; granular endpoints are perfect for debugging and CI.

---

## Troubleshooting

- **400 Missing fields / wrong body type** → ensure JSON vs multipart as required.
- **413 Payload too large** → raise `MAX_UPLOAD_MB` in `.env`.
- **No FAISS index yet** → run `/index/build` or `/pipeline/ingest` first.
- **OPENAI\_API\_KEY missing** → set it in `.env` and restart.
- **Ports** → `run.py` starts on `:5000` by default; adjust Insomnia/cURL accordingly.

---

## Deploy notes (MVP)

- Set env vars in your host (Render/Railway/AWS/etc.).
- Persist `DATA_DIR` as a volume so FAISS/SQLite survive restarts.
- Restrict `CORS_ORIGINS` in production.
- Use a process manager (e.g., gunicorn + gevent or uvicorn with ASGI bridge) when moving beyond dev.
 
---

## Security Notes

⚠️ **Important**: Never commit your `.env` file to version control!
- Copy `env.template` to `.env` and fill in your actual API keys
- The `.env` file is already in `.gitignore` for security
- Use `env.example` for non-sensitive configuration values

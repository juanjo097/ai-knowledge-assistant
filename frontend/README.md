# AI Knowledge Assistant — Frontend

## Overview
This repository contains the **frontend** for the AI Knowledge Assistant MVP. It enables users to:
- **Sign in** with JWT
- **Upload** a knowledge file (TXT/CSV)
- **Chat** grounded on the uploaded file
- **Save** the assistant’s last answer as a **note**
- **Browse** notes

Built with **React + TypeScript + Vite + Material UI v7**, using **React Router v6** and a small **fetch wrapper** (`http.ts`).  
Chat history is persisted in **localStorage per `docId`** to survive navigation.

---

## Tech Stack
- **React 18** + **TypeScript**
- **Vite**
- **Material UI v7**
- **React Router v6**
- **LocalStorage** (lightweight persistence for chat messages)

---

## Requirements
- **Node.js** ≥ 18
- **npm** ≥ 9

---

## Quick Start
```bash
# 1) Install dependencies
npm install

# 2) Configure environment (see .env variables below)
cp .env.example .env

# 3) Run the dev server
npm run dev

# 4) Build & preview
npm run build
npm run preview
```

### Environment Variables
Create `.env` in the frontend root (no trailing slash in `VITE_API_BASE`).

```
VITE_API_BASE=http://localhost:5000
# Optional: override chat path if your backend uses a different route (e.g., /ask)
VITE_CHAT_PATH=/chat
```

- `VITE_API_BASE`: Backend base URL.
- `VITE_CHAT_PATH` (optional): Chat endpoint path (default `/chat`).

---

## Project Structure (key files)
```
src/
  app/
    App.tsx                 # Router, protected routes, Shell layout
    AppHeader.tsx           # Tabs navigation + Logout
    DocContext.tsx          # Provides active docId
  features/
    auth/
      LoginPage.tsx
      auth.ts               # token helpers (localStorage)
    chat/
      ChatPanel.tsx
      ChatInput.tsx
      MessageBubble.tsx
      useChat.ts            # chat logic + per-docId persistence
    notes/
      NotesList.tsx         # full list
      NotesPreview.tsx      # sidebar/preview (optional on Home)
    upload/
      uploadCard.tsx
  pages/
    Home.tsx                # Upload (left) + Chat (right)
  shared/
    api/http.ts             # fetch wrapper + Authorization header, 401 handling
    hooks/usePersistentState.ts
    ui/PageContainer.tsx    # (optional) page shell
    ui/Section.tsx          # (optional) card section wrapper
  shared/theme/             # AppTheme (MUI theme)
```

---

## Routing & Navigation
- **Public** route: `/login`
- **Protected** routes: `/`, `/chat`, `/notes` (require JWT)

`App.tsx` uses a `ProtectedRoute` to check `isAuthenticated()` (token presence in localStorage).  
`AppHeader` provides tabs (Home / Chat / Notes) and a **Logout** button (clears token + redirects to `/login`).

---

## Authentication (Frontend)
- Login posts to `POST /auth/login` with `{ "username": "...", "password": "..." }`.
- On success, the backend returns `{ "token": "..." }` which is stored in **localStorage**.
- The token is attached to every request in `src/shared/api/http.ts` via `Authorization: Bearer <token>`.
- On **401**, the client clears the token; protected routes will redirect to `/login`.

> **CORS note:** The backend must allow `OPTIONS` preflight and the `Authorization` header.

---

## Data Flow
### Doc ID
`DocContext` provides the active `docId` (set after a successful upload).

### Chat
`useChat.ts` persists chat messages per document using `localStorage` and the key `chat:<docId>`.  
When the user navigates away and returns, the conversation is rehydrated automatically.

**Send message:**
```ts
await http.post('/chat', { doc_id: Number(docId), message: 'Your question' });
```

### Notes
- `POST /notes` with `{ content }` saves the latest answer as a note.
- `GET /notes?limit=3` is used by `NotesPreview` for a quick sidebar list.
- `GET /notes` is used by `NotesList` to display all notes.

---

## API Client (`http.ts`)
A tiny wrapper around `fetch` that:
- Prefixes all requests with `VITE_API_BASE`
- Adds `Authorization` when a token exists
- Clears the token on **401** and surfaces a readable error

Example:
```ts
http.get<T>('/notes')
http.post<T>('/auth/login', { username, password })
http.post<T>('/chat', { doc_id, message })
```

---

## Key Components
### Home (`pages/Home.tsx`)
Two-column layout with Material UI `Grid`:
- **Left**: `UploadCard`
- **Right**: `ChatPanel`

On wider screens, the chat column gets more space (see `xs/sm/md/lg/xl` settings in `Home.tsx`).

### UploadCard
- Click **Choose file** or **drag & drop** (TXT/CSV)
- Shows processing state and last uploaded filename
- Uses the `useUpload` hook for the actual upload flow

### ChatPanel
- Sticky header with **Save last answer** button
- Scrollable message list
- Input docked at the bottom
- Height is responsive; width controlled by the parent grid

### ChatInput
- Multiline auto-grow (1–6 rows)
- **Enter** to send, **Shift+Enter** for newline
- Spinner while awaiting response (`busy` state)

### Notes
- **NotesPreview**: latest notes (e.g., 3) with a “View all” button
- **NotesList**: full list with timestamps

---

## Styling & UX
- Material UI v7 components with subtle borders and rounded corners
- Keep titles inside cards (avoid duplicated headings)
- Consistent paddings (`p: 2` or `1.5`) and spacing (`Stack`/`gap`)
- To make chat wider:
  - Increase container width in `App.tsx` (`maxWidth="xl"`), and/or
  - Adjust grid fractions in `Home.tsx` (e.g., `xl={10}` for Chat, `xl={2}` for Upload)

---

## Deployment
- Build: `npm run build` (outputs to `dist/`)
- Serve `dist/` with your preferred static host (Vercel, Netlify, Nginx, etc.)
- Ensure backend **CORS** allows the deployed frontend origin:
  - Methods: `GET, POST, OPTIONS, ...`
  - Headers: `Authorization, Content-Type`
  - Preflight (`OPTIONS`) must return 200

---

## Troubleshooting

**Login works but `/notes` returns 401**  
- Backend must allow **OPTIONS** preflight and the `Authorization` header.
- The auth middleware should skip `OPTIONS` and allow `/auth/login` and `/health`.

**Chat doesn’t respond / wrong payload**  
- Confirm request body matches backend: `{ doc_id, message }`.
- If the chat route is different (e.g. `/ask`), set `VITE_CHAT_PATH=/ask`.

**Double slashes in URLs**  
- Ensure `VITE_API_BASE` has **no trailing slash**.

**Messages disappear when navigating**  
- Ensure `useChat.ts` persists per `docId` using `usePersistentState`.

---

## Roadmap
- Notes: search, filters, pagination
- Chat: copy-to-clipboard, regenerate answer, message actions
- Upload: size limits, per-chunk progress
- Error boundary and toasts for network failures
- Tests: component (Vitest/RTL) and E2E (Playwright)

---

## License
Internal / Project use.

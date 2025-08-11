import { getToken, clearToken } from "../../features/auth/auth";

const BASE = import.meta.env.VITE_API_BASE;

async function handle<T>(res: Response): Promise<T> {
  if (!res.ok) {
    // if token is missing, clear the token
    if (res.status === 401) {
      clearToken();
    }
    let msg = `${res.status} ${res.statusText}`;
    try {
      const data: unknown = await res.json();
      if (typeof data === "object" && data !== null) {
        const errorMsg =
          (data as { error?: string })?.error ||
          (data as { message?: string })?.message;
        if (typeof errorMsg === "string") {
          msg = errorMsg;
        }
      }
    } catch {
      msg = `${res.status} ${res.statusText}`;
    }
    throw new Error(msg);
  }
  return res.json() as Promise<T>;
}

function authHeaders(extra?: HeadersInit): HeadersInit {
  const h = new Headers(extra);
  const token = getToken();
  console.log("TOKEN", token);
  if (token) h.set("Authorization", `Bearer ${token}`);
  return h;
}

export const http = {
  get<T>(path: string) {
    return fetch(`${BASE}${path}`, {
      headers: authHeaders(),
    }).then((res) => handle<T>(res));
  },

  post<T>(path: string, body: unknown) {
    return fetch(`${BASE}${path}`, {
      method: "POST",
      headers: authHeaders({ "Content-Type": "application/json" }),
      body: JSON.stringify(body),
    }).then((res) => handle<T>(res));
  },

  postForm<T>(path: string, form: FormData) {
    // NO pongas Content-Type manual, el browser arma el boundary
    return fetch(`${BASE}${path}`, {
      method: "POST",
      headers: authHeaders(),
      body: form,
    }).then((res) => handle<T>(res));
  },
};

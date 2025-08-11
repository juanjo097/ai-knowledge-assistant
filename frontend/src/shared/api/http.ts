const BASE = import.meta.env.VITE_API_BASE;

async function handle<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let msg = `${res.status} ${res.statusText}`;
    try {
      const data = await res.json();
      msg = data?.error || data?.message || msg;
    } catch {
        // If parsing JSON fails, we keep the original message
        // This can happen if the response is not JSON formatted
        msg = `${res.status} ${res.statusText}`;
    }
    throw new Error(msg);
  }
  return res.json() as Promise<T>;
}

export const http = {
  get<T>(path: string) {
    return fetch(`${BASE}${path}`).then(res => handle<T>(res));
  },
  post<T>(path: string, body: unknown) {
    return fetch(`${BASE}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }).then(res => handle<T>(res));
  },
  postForm<T>(path: string, form: FormData) {
    return fetch(`${BASE}${path}`, { method: "POST", body: form }).then(
      res => handle<T>(res)
    );
  },
};

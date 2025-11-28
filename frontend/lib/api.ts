export const API_URL = "http://localhost:8000";

// ---------- Types ----------
export interface LoginResponse {
  access_token: string;
  token_type: string;
}


export async function apiLogin(username: string, password: string): Promise<LoginResponse> {
  const res = await fetch(`${API_URL}/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username:username, password:password }),
  });

  if (!res.ok) {
    throw new Error("Invalid credentials");
  }

  return res.json() as Promise<LoginResponse>;
}


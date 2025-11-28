export function saveToken(token: string): void {
  if (typeof window !== "undefined") {
     try {
      localStorage.setItem('token', token);
    } catch (error) {
      console.error("Failed to save token:", error);
    }
  }
}

export function getToken(): string | null {
  if (typeof window === "undefined") return null;
  try {
    return localStorage.getItem('token');
  } catch (error) {
    console.error("Failed to retrieve token:", error);
    return null;
  }
}

export function logout(): void {
  if (typeof window !== "undefined") {
    try {
      localStorage.removeItem('token');
      window.location.href = "/login";
    } catch (error) {
      console.error("Failed to logout:", error);
    }
  }
}

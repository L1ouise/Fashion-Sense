const headers = {
  "Content-Type": "application/json; charset=utf-8",
};

export async function generateLook(userInput) {
  const res = await fetch("/api/generate-look/", {
    method: "POST",
    headers,
    body: JSON.stringify({ user_input: userInput }),
  });
  if (!res.ok) {
    const detail = await res.text();
    throw new Error(detail || "Erreur API");
  }
  return res.json();
}

export async function fetchHistory(limit = 5) {
  const res = await fetch(`/api/generate-look/?limit=${limit}`);
  if (!res.ok) return [];
  return res.json();
}

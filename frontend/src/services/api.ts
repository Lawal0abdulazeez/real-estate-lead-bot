const API_BASE = import.meta.env.VITE_API_BASE || "/api/v1";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...(options?.headers || {}) },
    ...options,
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body?.detail || body?.error?.message || `Request failed (${res.status})`);
  }
  return res.json();
}

export type Conversation = {
  id: string;
  lead_id: string;
  channel: string;
  status: string;
  started_at: string;
  created_at: string;
};

export type Message = {
  id: string;
  conversation_id: string;
  sender_type: string;
  content: string;
  processing_status?: string;
  created_at: string;
};

export type Lead = {
  id: string;
  name?: string;
  email?: string;
  phone?: string;
  property_type?: string;
  transaction_type?: string;
  bedrooms?: number;
  location?: string;
  budget_max?: number;
  currency?: string;
  timeline?: string;
  status: string;
  classification?: string;
  score?: number;
  created_at: string;
};

export async function createConversation(payload?: {
  name?: string;
  email?: string;
  phone?: string;
}): Promise<Conversation> {
  return request("/conversations", {
    method: "POST",
    body: JSON.stringify({ channel: "WEB", ...payload }),
  });
}

export async function sendMessage(
  conversationId: string,
  content: string
): Promise<Message> {
  return request(`/conversations/${conversationId}/messages`, {
    method: "POST",
    body: JSON.stringify({ content }),
  });
}

export async function getMessages(conversationId: string): Promise<{
  items: Message[];
  total: number;
}> {
  return request(`/conversations/${conversationId}/messages`);
}

export async function listLeads(): Promise<{ items: Lead[]; total: number }> {
  return request("/leads?limit=50");
}

export async function getLead(id: string): Promise<Lead> {
  return request(`/leads/${id}`);
}

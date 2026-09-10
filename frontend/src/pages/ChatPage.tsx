import { FormEvent, useEffect, useRef, useState } from "react";
import {
  createConversation,
  getMessages,
  Message,
  sendMessage,
} from "../services/api";

const WELCOME =
  "Hi! I'm the PrimeHomes assistant. Tell me what you're looking for — buy, rent, or land — and I'll help capture your requirements.";

type UiMessage = {
  id: string;
  sender_type: string;
  content: string;
};

const SUGGESTIONS = [
  "Looking for a 3-bedroom apartment in Lekki around ₦85m to buy within 2 months",
  "I want to rent a 2-bedroom flat in Ikeja GRA with a budget of ₦5m per year",
  "Interested in 2 plots of commercial land in Epe for investment",
];

export default function ChatPage() {
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [messages, setMessages] = useState<UiMessage[]>([
    { id: "welcome", sender_type: "BOT", content: WELCOME },
  ]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const bottomRef = useRef<HTMLDivElement>(null);
  const messagesRef = useRef<UiMessage[]>(messages);

  useEffect(() => {
    messagesRef.current = messages;
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, sending]);

  async function ensureConversation() {
    if (conversationId) return conversationId;
    const conv = await createConversation();
    setConversationId(conv.id);
    return conv.id;
  }

  function handleReset() {
    setConversationId(null);
    setMessages([{ id: `welcome-${Date.now()}`, sender_type: "BOT", content: WELCOME }]);
    setInput("");
    setError(null);
  }

  async function onSubmit(e?: FormEvent, customText?: string) {
    if (e) e.preventDefault();
    const text = (customText ?? input).trim();
    if (!text || sending) return;

    setError(null);
    setInput("");
    setSending(true);

    const tempId = `local-${Date.now()}`;
    setMessages((prev) => [
      ...prev,
      { id: tempId, sender_type: "CUSTOMER", content: text },
    ]);

    try {
      const convId = await ensureConversation();
      const msg = await sendMessage(convId, text);
      setMessages((prev) =>
        prev.map((m) =>
          m.id === tempId
            ? { id: msg.id, sender_type: msg.sender_type, content: msg.content }
            : m
        )
      );

      // Poll for bot reply from n8n
      await pollForBotReply(convId, msg.id);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to send message");
    } finally {
      setSending(false);
    }
  }

  async function pollForBotReply(convId: string, afterId: string) {
    for (let i = 0; i < 12; i++) {
      await new Promise((r) => setTimeout(r, 1500));
      try {
        const res = await getMessages(convId);
        const currentIds = new Set(messagesRef.current.map((m) => m.id));
        const bots = res.items.filter(
          (m: Message) =>
            m.sender_type === "BOT" &&
            m.id !== afterId &&
            !currentIds.has(m.id)
        );
        if (bots.length) {
          setMessages((prev) => {
            const known = new Set(prev.map((p) => p.id));
            const extra = bots
              .filter((b) => !known.has(b.id))
              .map((b) => ({
                id: b.id,
                sender_type: b.sender_type,
                content: b.content,
              }));
            return extra.length ? [...prev, ...extra] : prev;
          });
          return;
        }
      } catch {
        /* ignore poll errors */
      }
    }

    // Fallback acknowledgement if bot hasn't replied yet
    setMessages((prev) => {
      // only add if no bot reply arrived
      const hasRecentBot = prev.some(
        (m, idx) => idx > 0 && m.sender_type === "BOT"
      );
      if (hasRecentBot) return prev;
      return [
        ...prev,
        {
          id: `ack-${Date.now()}`,
          sender_type: "BOT",
          content:
            "Thank you! Your requirements have been captured and forwarded to our PrimeHomes property advisory team. We will reach out with matching options shortly.",
        },
      ];
    });
  }

  return (
    <>
      {error && <div className="error-banner">{error}</div>}
      <div className="card chat-layout">
        <div className="chat-header">
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <div>
              <h1>PrimeHomes Property Assistant</h1>
              <p>Tell us your property requirements, budget, and preferred location.</p>
            </div>
            <button
              onClick={handleReset}
              className="btn"
              style={{
                fontSize: "0.8rem",
                padding: "0.4rem 0.8rem",
                background: "white",
                border: "1px solid var(--neutral-300)",
              }}
              title="Start a new chat session"
            >
              New Chat
            </button>
          </div>
        </div>

        <div className="messages">
          {messages.map((m) => (
            <div
              key={m.id}
              className={`bubble ${
                m.sender_type === "CUSTOMER"
                  ? "customer"
                  : m.sender_type === "SYSTEM"
                  ? "system"
                  : "bot"
              }`}
            >
              {m.content}
            </div>
          ))}
          {sending && (
            <div className="typing" aria-label="Processing">
              <span />
              <span />
              <span />
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        {messages.length <= 1 && (
          <div style={{ padding: "0 1rem 0.75rem", display: "flex", flexWrap: "wrap", gap: "0.5rem" }}>
            {SUGGESTIONS.map((s, i) => (
              <button
                key={i}
                type="button"
                className="btn"
                style={{
                  fontSize: "0.78rem",
                  padding: "0.35rem 0.75rem",
                  background: "var(--orange-50)",
                  border: "1px solid var(--orange-200)",
                  color: "var(--orange-700)",
                  textAlign: "left",
                }}
                onClick={() => onSubmit(undefined, s)}
                disabled={sending}
              >
                💡 {s}
              </button>
            ))}
          </div>
        )}

        <form className="composer" onSubmit={onSubmit}>
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="e.g. Looking for a 3-bedroom apartment around Lekki, budget ₦80m..."
            disabled={sending}
            autoFocus
          />
          <button className="btn btn-primary" type="submit" disabled={sending || !input.trim()}>
            {sending ? "Processing…" : "Send"}
          </button>
        </form>
      </div>
    </>
  );
}

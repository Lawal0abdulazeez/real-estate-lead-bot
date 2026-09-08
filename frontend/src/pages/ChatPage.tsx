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

export default function ChatPage() {
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [messages, setMessages] = useState<UiMessage[]>([
    { id: "welcome", sender_type: "BOT", content: WELCOME },
  ]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, sending]);

  async function ensureConversation() {
    if (conversationId) return conversationId;
    const conv = await createConversation();
    setConversationId(conv.id);
    return conv.id;
  }

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    const text = input.trim();
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

      // Poll briefly for bot reply (n8n may write it back)
      await pollForBotReply(convId, msg.id);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to send message");
    } finally {
      setSending(false);
    }
  }

  async function pollForBotReply(convId: string, afterId: string) {
    for (let i = 0; i < 8; i++) {
      await new Promise((r) => setTimeout(r, 1200));
      try {
        const res = await getMessages(convId);
        const bots = res.items.filter(
          (m: Message) =>
            m.sender_type === "BOT" &&
            m.id !== afterId &&
            !messages.some((x) => x.id === m.id)
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
    // Fallback acknowledgement if n8n hasn't responded yet
    setMessages((prev) => [
      ...prev,
      {
        id: `ack-${Date.now()}`,
        sender_type: "BOT",
        content:
          "Thanks! I've received your message and our system is processing it. A sales specialist will follow up if needed.",
      },
    ]);
  }

  return (
    <>
      {error && <div className="error-banner">{error}</div>}
      <div className="card chat-layout">
        <div className="chat-header">
          <h1>Real Estate Assistant</h1>
          <p>Describe what you're looking for in natural language</p>
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

        <form className="composer" onSubmit={onSubmit}>
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="e.g. I want a 3-bedroom apartment in Lekki under ₦80m"
            disabled={sending}
            autoFocus
          />
          <button className="btn btn-primary" type="submit" disabled={sending || !input.trim()}>
            Send
          </button>
        </form>
      </div>
    </>
  );
}

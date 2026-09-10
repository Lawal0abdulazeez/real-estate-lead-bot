import { useEffect, useState } from "react";
import { Lead, listLeads } from "../services/api";

function badgeClass(c?: string) {
  if (!c) return "unqualified";
  return c.toLowerCase();
}

function formatNaira(amount?: number) {
  if (!amount) return null;
  if (amount >= 1_000_000_000) {
    return `₦${(amount / 1_000_000_000).toFixed(1)}B`;
  }
  if (amount >= 1_000_000) {
    return `₦${(amount / 1_000_000).toFixed(amount % 1_000_000 === 0 ? 0 : 1)}M`;
  }
  return `₦${amount.toLocaleString()}`;
}

export default function LeadsPage() {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [filter, setFilter] = useState<string>("ALL");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  function fetchLeads() {
    setLoading(true);
    setError(null);
    listLeads()
      .then((res) => setLeads(res.items))
      .catch((e) => setError(e instanceof Error ? e.message : "Failed to load leads"))
      .finally(() => setLoading(false));
  }

  useEffect(() => {
    fetchLeads();
  }, []);

  const filteredLeads = leads.filter((l) => {
    if (filter === "ALL") return true;
    return (l.classification || "UNQUALIFIED").toUpperCase() === filter;
  });

  return (
    <div>
      <div className="leads-header">
        <div>
          <h2>PrimeHomes Leads Pipeline</h2>
          <p style={{ margin: "0.25rem 0 0", fontSize: "0.85rem", color: "var(--neutral-500)" }}>
            Automatically qualified leads captured from incoming customer enquiries
          </p>
        </div>
        <button
          onClick={fetchLeads}
          className="btn btn-primary"
          style={{ fontSize: "0.85rem", padding: "0.45rem 1rem" }}
          disabled={loading}
        >
          {loading ? "Refreshing…" : "🔄 Refresh Leads"}
        </button>
      </div>

      <div style={{ display: "flex", gap: "0.5rem", marginBottom: "1rem", flexWrap: "wrap" }}>
        {["ALL", "HOT", "WARM", "COLD", "UNQUALIFIED"].map((cat) => (
          <button
            key={cat}
            onClick={() => setFilter(cat)}
            className={`btn ${filter === cat ? "btn-primary" : ""}`}
            style={{
              fontSize: "0.8rem",
              padding: "0.35rem 0.8rem",
              background: filter === cat ? undefined : "white",
              border: "1px solid var(--neutral-300)",
              color: filter === cat ? "white" : "var(--neutral-700)",
            }}
          >
            {cat} {cat === "ALL" ? `(${leads.length})` : `(${leads.filter(l => (l.classification || "UNQUALIFIED").toUpperCase() === cat).length})`}
          </button>
        ))}
      </div>

      {error && <div className="error-banner">{error}</div>}

      <div className="card table-wrap">
        {loading && leads.length === 0 ? (
          <div className="empty">Loading leads pipeline…</div>
        ) : filteredLeads.length === 0 ? (
          <div className="empty">
            {leads.length === 0
              ? "No leads captured yet. Go to the Chat tab to start a conversation!"
              : `No leads in '${filter}' category.`}
          </div>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Customer</th>
                <th>Requirement</th>
                <th>Location</th>
                <th>Budget & Timeline</th>
                <th>Score / Class</th>
                <th>Status</th>
                <th>Captured</th>
              </tr>
            </thead>
            <tbody>
              {filteredLeads.map((l) => (
                <tr key={l.id}>
                  <td>
                    <strong>{l.name || "Anonymous Lead"}</strong>
                    <div style={{ fontSize: "0.8rem", color: "var(--neutral-500)" }}>
                      {l.phone || l.email || `#${l.id.slice(0, 8)}`}
                    </div>
                  </td>
                  <td>
                    <div>
                      {[l.transaction_type, l.property_type]
                        .filter(Boolean)
                        .join(" · ") || "—"}
                    </div>
                    {l.bedrooms && (
                      <span
                        style={{
                          fontSize: "0.75rem",
                          background: "var(--orange-100)",
                          color: "var(--orange-700)",
                          padding: "2px 6px",
                          borderRadius: "4px",
                          display: "inline-block",
                          marginTop: "3px",
                        }}
                      >
                        {l.bedrooms} Bedroom{l.bedrooms > 1 ? "s" : ""}
                      </span>
                    )}
                  </td>
                  <td>{l.location || "—"}</td>
                  <td>
                    <div style={{ fontWeight: 600, color: "var(--orange-700)" }}>
                      {formatNaira(l.budget_max) || (l.budget_min ? formatNaira(l.budget_min) : "—")}
                    </div>
                    {l.timeline && (
                      <div style={{ fontSize: "0.75rem", color: "var(--neutral-500)" }}>
                        {l.timeline.replace(/_/g, " ").toLowerCase()}
                      </div>
                    )}
                  </td>
                  <td>
                    {l.score != null ? (
                      <div style={{ display: "flex", alignItems: "center", gap: "0.4rem" }}>
                        <span style={{ fontWeight: 700 }}>{l.score}</span>
                        {l.classification && (
                          <span className={`badge ${badgeClass(l.classification)}`}>
                            {l.classification}
                          </span>
                        )}
                      </div>
                    ) : (
                      "—"
                    )}
                  </td>
                  <td>
                    <span
                      style={{
                        fontSize: "0.8rem",
                        fontWeight: 500,
                        color: l.status === "QUALIFIED" ? "var(--success)" : "var(--neutral-700)",
                      }}
                    >
                      {l.status}
                    </span>
                  </td>
                  <td style={{ fontSize: "0.8rem", color: "var(--neutral-500)" }}>
                    {new Date(l.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}, {new Date(l.created_at).toLocaleDateString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

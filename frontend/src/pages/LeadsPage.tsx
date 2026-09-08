import { useEffect, useState } from "react";
import { Lead, listLeads } from "../services/api";

function badgeClass(c?: string) {
  if (!c) return "unqualified";
  return c.toLowerCase();
}

export default function LeadsPage() {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    listLeads()
      .then((res) => setLeads(res.items))
      .catch((e) => setError(e instanceof Error ? e.message : "Failed to load leads"))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div>
      <div className="leads-header">
        <h2>Leads</h2>
      </div>

      {error && <div className="error-banner">{error}</div>}

      <div className="card table-wrap">
        {loading ? (
          <div className="empty">Loading leads…</div>
        ) : leads.length === 0 ? (
          <div className="empty">
            No leads yet. Start a chat and send a message to create one.
          </div>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Customer</th>
                <th>Requirement</th>
                <th>Location</th>
                <th>Score</th>
                <th>Status</th>
                <th>Created</th>
              </tr>
            </thead>
            <tbody>
              {leads.map((l) => (
                <tr key={l.id}>
                  <td>
                    <strong>{l.name || "—"}</strong>
                    <div style={{ fontSize: "0.8rem", color: "#737373" }}>
                      {l.phone || l.email || l.id.slice(0, 8)}
                    </div>
                  </td>
                  <td>
                    {[l.transaction_type, l.property_type, l.bedrooms ? `${l.bedrooms} bed` : null]
                      .filter(Boolean)
                      .join(" · ") || "—"}
                  </td>
                  <td>{l.location || "—"}</td>
                  <td>
                    {l.score != null ? (
                      <>
                        <strong>{l.score}</strong>{" "}
                        {l.classification && (
                          <span className={`badge ${badgeClass(l.classification)}`}>
                            {l.classification}
                          </span>
                        )}
                      </>
                    ) : (
                      "—"
                    )}
                  </td>
                  <td>{l.status}</td>
                  <td>{new Date(l.created_at).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

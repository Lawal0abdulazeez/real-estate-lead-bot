import { NavLink, Route, Routes } from "react-router-dom";
import ChatPage from "./pages/ChatPage";
import LeadsPage from "./pages/LeadsPage";

export default function App() {
  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="brand">
          <div className="brand-mark">PH</div>
          <span>PrimeHomes Lead Bot</span>
        </div>
        <nav className="nav">
          <NavLink to="/" end className={({ isActive }) => (isActive ? "active" : "")}>
            Chat
          </NavLink>
          <NavLink to="/leads" className={({ isActive }) => (isActive ? "active" : "")}>
            Leads
          </NavLink>
        </nav>
      </header>

      <Routes>
        <Route path="/" element={<ChatPage />} />
        <Route path="/leads" element={<LeadsPage />} />
      </Routes>
    </div>
  );
}

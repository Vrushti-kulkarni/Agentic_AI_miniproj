import pandas as pd
import streamlit as st
from core import database as db, rbac_engine as eng, ui
from core.tools import TOOLS, RISK_ICON

ui.setup_page("AI Agent Access Control", "🛡️",
              "This system controls what AI agents can and cannot do. "
              "Each agent has a role that determines which tools it may use. "
              "Select an agent from the sidebar pages to put it to work.")

agents = db.query(
    "SELECT a.*, r.name AS role_name FROM agents a LEFT JOIN roles r ON r.id=a.role_id ORDER BY a.id"
)

# Agent cards in grid
if agents:
    st.subheader("🤖 Agent Fleet")
    cols = st.columns(4)
    for i, a in enumerate(agents):
        with cols[i % 4]:
            with st.container(border=True):
                status_badge = "🟢 Active" if a["status"] == "active" else "🔴 Suspended"
                st.markdown(f"### {a.get('avatar', '🤖')} {a['name']}")
                st.caption(f"Role: **{a['role_name'] or 'None'}** | {status_badge}")
                st.markdown(f"{a['description']}")

# Permission matrix
st.subheader("🗓️ Permission Matrix")
st.caption("What each agent is allowed (✅) or blocked (❌) from doing.")
if agents:
    rows = []
    for a in agents:
        row = {"Agent": f"{a.get('avatar','🤖')} {a['name']}", "Role": a["role_name"] or "None"}
        for tool_name, tool_info in TOOLS.items():
            d = eng.evaluate(a["name"], tool_name, tool_info["example"], log=False)
            row[f"{RISK_ICON[tool_info['risk']]} {tool_info['label']}"] = "✅" if d.allowed else "❌"
        rows.append(row)
    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)

st.divider()
st.caption("🔒 Go to the **Admin Panel** page (sidebar) to manage roles, permissions, and agents.")

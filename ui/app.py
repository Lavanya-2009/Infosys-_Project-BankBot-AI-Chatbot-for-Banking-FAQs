# import streamlit as st

# # ---------------- PAGE CONFIG ----------------
# st.set_page_config(
#     page_title="BankBot AI",
#     page_icon="🏦",
#     layout="wide"
# )

# # ---------------- CSS ----------------
# st.markdown("""
# <style>
# #MainMenu, footer, header {visibility: hidden;}

# /* -------- BACKGROUND -------- */
# .stApp {
#     background: linear-gradient(135deg, #0f172a, #0b3a3f);
#     color: #f1f5f9;
# }

# /* -------- SIDEBAR -------- */
# section[data-testid="stSidebar"] {
#     background: linear-gradient(180deg, #020617, #062e2e);
#     border-right: 1px solid rgba(255,255,255,0.08);
# }

# section[data-testid="stSidebar"] * {
#     color: #e5e7eb;
# }

# /* Sidebar title */
# .sidebar-title {
#     font-size: 1.5rem;
#     font-weight: 800;
#     margin-bottom: 0.3rem;
# }

# /* Sidebar subtitle */
# .sidebar-subtitle {
#     font-size: 0.9rem;
#     opacity: 0.75;
#     margin-bottom: 1.2rem;
# }

# /* -------- HERO -------- */
# .hero {
#     text-align: center;
#     padding: 4rem 1rem 2rem;
# }

# .hero-title {
#     font-size: 3rem;
#     font-weight: 800;
# }

# .hero-subtitle {
#     font-size: 1.1rem;
#     opacity: 0.8;
#     margin-top: 0.5rem;
# }

# /* -------- DIVIDER -------- */
# .divider {
#     width: 70px;
#     height: 3px;
#     background: #2dd4bf;
#     margin: 1.5rem auto;
#     border-radius: 6px;
# }

# /* -------- CARDS -------- */
# .card {
#     background: rgba(255,255,255,0.08);
#     border-radius: 16px;
#     padding: 1.8rem;
#     box-shadow: 0 12px 32px rgba(0,0,0,0.35);
#     transition: transform 0.3s ease;
# }

# .card:hover {
#     transform: translateY(-6px);
# }

# .card-title {
#     font-size: 1.25rem;
#     font-weight: 700;
#     margin-bottom: 0.5rem;
# }

# .card-text {
#     font-size: 0.95rem;
#     opacity: 0.8;
# }

# /* -------- FOOTER -------- */
# .footer {
#     text-align: center;
#     margin-top: 4rem;
#     font-size: 0.85rem;
#     opacity: 0.6;
# }
# """, unsafe_allow_html=True)

# # ---------------- SIDEBAR ----------------
# with st.sidebar:
#     st.markdown("""
#     <div class="sidebar-title">🏦 BankBot AI</div>
#     <div class="sidebar-subtitle">
#         Smart Banking Assistant
#     </div>
#     """, unsafe_allow_html=True)

#     st.divider()

#     menu = st.radio(
#         "Navigation",
#         ["🏠 Home", "🤖 Chatbot", "🔐 Security", "📊 Dashboard", "ℹ️ About"]
#     )

#     st.divider()

#     st.caption("© 2025 BankBot AI")

# # ---------------- MAIN CONTENT ----------------
# if menu == "🏠 Home":
#     st.markdown("""
#     <div class="hero">
#         <div class="hero-title">BankBot AI</div>
#         <div class="hero-subtitle">
#             Secure • Intelligent • Banking-Ready
#         </div>
#         <div class="divider"></div>
#     </div>
#     """, unsafe_allow_html=True)

#     col1, col2, col3 = st.columns(3)

#     with col1:
#         st.markdown("""
#         <div class="card">
#             <div class="card-title">🔐 Secure</div>
#             <div class="card-text">
#                 Enterprise-level security built for banks.
#             </div>
#         </div>
#         """, unsafe_allow_html=True)

#     with col2:
#         st.markdown("""
#         <div class="card">
#             <div class="card-title">🤖 Intelligent</div>
#             <div class="card-text">
#                 AI-powered NLP for accurate banking support.
#             </div>
#         </div>
#         """, unsafe_allow_html=True)

#     with col3:
#         st.markdown("""
#         <div class="card">
#             <div class="card-title">⚡ Efficient</div>
#             <div class="card-text">
#                 Fast response times with low compute cost.
#             </div>
#         </div>
#         """, unsafe_allow_html=True)

# elif menu == "🤖 Chatbot":
#     st.header("🤖 BankBot Chat")
#     st.info("Chat interface will be integrated here.")

# elif menu == "🔐 Security":
#     st.header("🔐 Security")
#     st.write("Encryption, authentication, and compliance details.")

# elif menu == "📊 Dashboard":
#     st.header("📊 Dashboard")
#     st.write("Admin analytics and insights.")

# elif menu == "ℹ️ About":
#     st.header("ℹ️ About BankBot AI")
#     st.write("AI-powered banking assistant built with security-first design.")

# # ---------------- FOOTER ----------------
# st.markdown("""
# <div class="footer">
#     © 2025 BankBot AI • Built for modern banking
# </div>
# """, unsafe_allow_html=True)
import streamlit as st

st.set_page_config(
    page_title="BankBot AI",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- SESSION REDIRECT ----------------
if "user_name" in st.session_state:
    if st.session_state.get("role") == "admin":
        st.switch_page("ui/pages/6_Admin.py")
    else:
        st.switch_page("ui/pages/4_Chatbot.py")

# ---------------- THEME TOGGLE ----------------
if "theme" not in st.session_state:
    st.session_state["theme"] = "Dark"

top_spacer, theme_col = st.columns([6, 1.4])
with theme_col:
    use_light = st.toggle(
        "Light theme",
        value=(st.session_state["theme"] == "Light"),
        key="theme_toggle"
    )

st.session_state["theme"] = "Light" if use_light else "Dark"
current_theme = st.session_state["theme"]

# ---------------- GLOBAL CSS (DARK & LIGHT) ----------------
dark_css = """
<style>
#MainMenu, footer, header { visibility: hidden; }

/* App background */
.stApp {
    background:
        radial-gradient(circle at 0% 0%, #1e293b 0, transparent 55%),
        radial-gradient(circle at 100% 0%, #0f766e 0, transparent 55%),
        radial-gradient(circle at 0% 100%, #1d4ed8 0, transparent 55%),
        radial-gradient(circle at 100% 100%, #7c3aed 0, transparent 55%),
        linear-gradient(135deg, #020617, #0f172a, #020617);
    background-size: 220% 220%;
    animation: backgroundShift 26s ease-in-out infinite;
    color: #e5e7eb;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

/* Layout shell */
.home-shell {
    max-width: 1100px;
    margin: 2.5rem auto 3.5rem auto;
    padding: 0 1.0rem 3.0rem 1.0rem;
}

/* Middle title */
.mid-title {
    margin-top: 2.0rem;
    margin-bottom: 1.4rem;
    text-align: center;
    font-size: 1.6rem;
    font-weight: 750;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #e5e7eb;
    opacity: 0.92;
}

/* HERO CARD */
.hero-card {
    border-radius: 28px;
    padding: 2.4rem 2.5rem 2.3rem 2.5rem;
    background:
        radial-gradient(circle at top left, rgba(59,130,246,0.35), transparent 65%),
        radial-gradient(circle at bottom right, rgba(45,212,191,0.25), transparent 60%),
        linear-gradient(135deg, rgba(15,23,42,0.95), rgba(15,23,42,0.86));
    border: 1px solid rgba(148, 163, 184, 0.6);
    box-shadow:
        0 30px 70px rgba(15, 23, 42, 0.85),
        0 0 0 1px rgba(15,23,42,0.9);
    position: relative;
    overflow: hidden;
}

/* subtle glow border */
.hero-card::before {
    content: "";
    position: absolute;
    inset: -1px;
    border-radius: inherit;
    padding: 1px;
    background: linear-gradient(135deg, rgba(59,130,246,0.85), rgba(14,165,233,0.8), rgba(45,212,191,0.8));
    -webkit-mask:
        linear-gradient(#000 0 0) content-box,
        linear-gradient(#000 0 0);
    -webkit-mask-composite: xor;
            mask-composite: exclude;
    opacity: 0.85;
    pointer-events: none;
}

/* light sweep */
.hero-card::after {
    content: "";
    position: absolute;
    inset: -70%;
    background: conic-gradient(
        from 210deg,
        rgba(59,130,246,0.0),
        rgba(59,130,246,0.35),
        rgba(45,212,191,0.0),
        rgba(56,189,248,0.32),
        rgba(59,130,246,0.0)
    );
    opacity: 0.0;
    transform: translate3d(0,0,0) rotate(0deg);
    transition: opacity 1.0s ease, transform 1.8s ease-out;
    pointer-events: none;
}

.hero-card:hover::after {
    opacity: 0.6;
    transform: translate3d(0,0,0) rotate(18deg);
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.22rem 0.7rem;
    border-radius: 999px;
    background: rgba(15,23,42,0.92);
    border: 1px solid rgba(56,189,248,0.7);
    font-size: 0.75rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #e0f2fe;
}

.hero-title {
    margin-top: 0.9rem;
    font-size: 2.8rem;
    line-height: 1.1;
    font-weight: 850;
    letter-spacing: 0.03em;
    background: linear-gradient(120deg, #e5e7eb, #38bdf8, #a5b4fc, #facc15, #e5e7eb);
    background-size: 260% 260%;
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    animation: titleGlow 9s ease-in-out infinite;
}

.hero-subtitle {
    margin-top: 0.6rem;
    font-size: 1.02rem;
    max-width: 640px;
    color: #cbd5e1;
    opacity: 0.92;
}

.hero-pills {
    margin-top: 1.2rem;
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}

.hero-pill {
    padding: 0.25rem 0.7rem;
    border-radius: 999px;
    background: rgba(15,23,42,0.9);
    border: 1px solid rgba(148,163,184,0.7);
    font-size: 0.8rem;
    color: #e5e7eb;
}

/* CTA row */
.cta-row {
    margin-top: 1.6rem;
}

/* Generic button styling */
.stButton > button {
    background-image: linear-gradient(120deg, #0ea5e9, #6366f1, #22c55e);
    background-size: 220% 220%;
    color: #f9fafb;
    font-weight: 750;
    border-radius: 999px;
    padding: 0.78rem 1.6rem;
    border: 1px solid rgba(15, 23, 42, 0.9);
    letter-spacing: 0.04em;
    text-transform: uppercase;
    box-shadow:
        0 14px 32px rgba(15, 23, 42, 0.95),
        0 0 24px rgba(56, 189, 248, 0.75);
    transition:
        transform 0.18s ease-out,
        box-shadow 0.22s ease-out,
        background-position 0.3s ease-out,
        filter 0.25s ease-out;
    cursor: pointer;
}

.stButton > button:hover {
    background-position: 100% 0%;
    transform: translateY(-2px) scale(1.01);
    box-shadow:
        0 22px 48px rgba(15, 23, 42, 1),
        0 0 36px rgba(56, 189, 248, 0.95);
    filter: saturate(125%);
}

.stButton > button:active {
    transform: translateY(0px) scale(0.995);
    box-shadow:
        0 10px 22px rgba(15, 23, 42, 0.9),
        0 0 20px rgba(56, 189, 248, 0.8);
}

/* FEATURE GRID */
.section-heading {
    margin-top: 2.6rem;
    margin-bottom: 0.4rem;
    font-size: 1.15rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #e5e7eb;
    opacity: 0.9;
}

.section-subtitle {
    font-size: 0.9rem;
    color: #cbd5e1;
    opacity: 0.85;
    margin-bottom: 1.2rem;
}

.feature-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0,1fr));
    gap: 1.1rem;
}

@media (max-width: 980px) {
    .feature-grid {
        grid-template-columns: repeat(2, minmax(0,1fr));
    }
}
@media (max-width: 640px) {
    .feature-grid {
        grid-template-columns: minmax(0,1fr);
    }
}

.feature-card {
    border-radius: 18px;
    padding: 1.2rem 1.25rem 1.3rem 1.25rem;
    background: radial-gradient(circle at top left, rgba(30, 64, 175, 0.45), transparent 65%),
                rgba(15, 23, 42, 0.96);
    border: 1px solid rgba(30, 64, 175, 0.65);
    box-shadow:
        0 18px 40px rgba(15, 23, 42, 0.9),
        0 0 0 1px rgba(15,23,42,0.9);
    position: relative;
    overflow: hidden;
}

.feature-card::after {
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at bottom right, rgba(56,189,248,0.25), transparent 60%);
    opacity: 0;
    transition: opacity 0.25s ease;
}

.feature-card:hover::after {
    opacity: 1;
}

.feature-icon {
    font-size: 1.1rem;
    margin-bottom: 0.4rem;
}

.feature-title {
    font-size: 1.02rem;
    font-weight: 700;
    color: #e5e7eb;
    margin-bottom: 0.25rem;
}

.feature-body {
    font-size: 0.9rem;
    color: #cbd5e1;
    opacity: 0.9;
}

/* STATS ROW */
.stats-row {
    margin-top: 2.2rem;
    display: grid;
    grid-template-columns: repeat(3, minmax(0,1fr));
    gap: 1.0rem;
}

@media (max-width: 860px) {
    .stats-row {
        grid-template-columns: repeat(2, minmax(0,1fr));
    }
}
@media (max-width: 640px) {
    .stats-row {
        grid-template-columns: minmax(0,1fr);
    }
}

.stat-card {
    border-radius: 20px;
    padding: 0.95rem 1.15rem 1.1rem;
    background: rgba(15, 23, 42, 0.92);
    border: 1px solid rgba(148, 163, 184, 0.7);
    box-shadow:
        0 16px 32px rgba(15, 23, 42, 0.95),
        0 0 0 1px rgba(15,23,42,0.9);
}

.stat-label {
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #94a3b8;
}

.stat-value {
    margin-top: 0.25rem;
    font-size: 1.4rem;
    font-weight: 800;
    color: #e5e7eb;
}

.stat-sub {
    margin-top: 0.1rem;
    font-size: 0.8rem;
    color: #cbd5e1;
    opacity: 0.85;
}

/* FOOTER */
.home-footer {
    text-align: center;
    margin-top: 2.8rem;
    font-size: 0.83rem;
    color: #94a3b8;
    opacity: 0.8;
}

/* Animations */
@keyframes backgroundShift {
    0% { background-position: 0% 10%; }
    50% { background-position: 100% 90%; }
    100% { background-position: 0% 10%; }
}

@keyframes titleGlow {
    0% {
        text-shadow: 0 0 16px rgba(56,189,248,0.75),
                     0 0 36px rgba(37,99,235,0.9);
    }
    50% {
        text-shadow: 0 0 10px rgba(56,189,248,0.8),
                     0 0 24px rgba(129,140,248,0.9);
    }
    100% {
        text-shadow: 0 0 16px rgba(56,189,248,0.75),
                     0 0 36px rgba(37,99,235,0.9);
    }
}
</style>
"""

light_css = """
<style>
#MainMenu, footer, header { visibility: hidden; }

/* App background */
.stApp {
    background:
        radial-gradient(circle at 0% 0%, #e0f2fe 0, transparent 55%),
        radial-gradient(circle at 100% 0%, #fce7f3 0, transparent 55%),
        radial-gradient(circle at 0% 100%, #dcfce7 0, transparent 55%),
        radial-gradient(circle at 100% 100%, #e0e7ff 0, transparent 55%),
        linear-gradient(135deg, #eff6ff, #ffffff, #e0f2fe, #f5f3ff);
    background-size: 220% 220%;
    animation: backgroundShift 26s ease-in-out infinite;
    color: #0f172a;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

/* Layout shell */
.home-shell {
    max-width: 1100px;
    margin: 2.5rem auto 3.5rem auto;
    padding: 0 1.0rem 3.0rem 1.0rem;
}

/* Middle title */
.mid-title {
    margin-top: 2.0rem;
    margin-bottom: 1.4rem;
    text-align: center;
    font-size: 1.6rem;
    font-weight: 750;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #0f172a;
    opacity: 0.9;
}

/* HERO CARD */
.hero-card {
    border-radius: 28px;
    padding: 2.4rem 2.5rem 2.3rem 2.5rem;
    background:
        radial-gradient(circle at top left, rgba(59,130,246,0.14), transparent 65%),
        radial-gradient(circle at bottom right, rgba(45,212,191,0.16), transparent 60%),
        linear-gradient(135deg, #ffffff, #f9fafb);
    border: 1px solid #d1d5db;
    box-shadow:
        0 20px 50px rgba(15, 23, 42, 0.14),
        0 0 0 1px rgba(226,232,240,0.9);
    position: relative;
    overflow: hidden;
}

.hero-card::before {
    content: "";
    position: absolute;
    inset: -1px;
    border-radius: inherit;
    padding: 1px;
    background: linear-gradient(135deg, rgba(59,130,246,0.55), rgba(14,165,233,0.55), rgba(45,212,191,0.55));
    -webkit-mask:
        linear-gradient(#000 0 0) content-box,
        linear-gradient(#000 0 0);
    -webkit-mask-composite: xor;
            mask-composite: exclude;
    opacity: 0.85;
    pointer-events: none;
}

.hero-card::after {
    content: "";
    position: absolute;
    inset: -70%;
    background: conic-gradient(
        from 210deg,
        rgba(59,130,246,0.0),
        rgba(59,130,246,0.22),
        rgba(45,212,191,0.0),
        rgba(56,189,248,0.24),
        rgba(59,130,246,0.0)
    );
    opacity: 0.0;
    transform: translate3d(0,0,0) rotate(0deg);
    transition: opacity 1.0s ease, transform 1.8s ease-out;
    pointer-events: none;
}

.hero-card:hover::after {
    opacity: 0.5;
    transform: translate3d(0,0,0) rotate(18deg);
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.22rem 0.7rem;
    border-radius: 999px;
    background: #eff6ff;
    border: 1px solid #93c5fd;
    font-size: 0.75rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #1d4ed8;
}

.hero-title {
    margin-top: 0.9rem;
    font-size: 2.8rem;
    line-height: 1.1;
    font-weight: 850;
    letter-spacing: 0.03em;
    background: linear-gradient(120deg, #0f172a, #2563eb, #7c3aed, #22c55e, #0f172a);
    background-size: 260% 260%;
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    animation: titleGlow 9s ease-in-out infinite;
}

.hero-subtitle {
    margin-top: 0.6rem;
    font-size: 1.02rem;
    max-width: 640px;
    color: #4b5563;
    opacity: 0.95;
}

.hero-pills {
    margin-top: 1.2rem;
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}

.hero-pill {
    padding: 0.25rem 0.7rem;
    border-radius: 999px;
    background: #eff6ff;
    border: 1px solid #cbd5e1;
    font-size: 0.8rem;
    color: #0f172a;
}

/* CTA row */
.cta-row {
    margin-top: 1.6rem;
}

/* Generic button styling (keep gradients, softer shadow) */
.stButton > button {
    background-image: linear-gradient(120deg, #0ea5e9, #6366f1, #22c55e);
    background-size: 220% 220%;
    color: #f9fafb;
    font-weight: 750;
    border-radius: 999px;
    padding: 0.78rem 1.6rem;
    border: 1px solid rgba(15, 23, 42, 0.05);
    letter-spacing: 0.04em;
    text-transform: uppercase;
    box-shadow:
        0 14px 28px rgba(37, 99, 235, 0.35),
        0 0 18px rgba(56, 189, 248, 0.55);
    transition:
        transform 0.18s ease-out,
        box-shadow 0.22s ease-out,
        background-position 0.3s ease-out,
        filter 0.25s ease-out;
    cursor: pointer;
}

.stButton > button:hover {
    background-position: 100% 0%;
    transform: translateY(-2px) scale(1.01);
    box-shadow:
        0 20px 40px rgba(37, 99, 235, 0.45),
        0 0 26px rgba(56, 189, 248, 0.85);
    filter: saturate(120%);
}

.stButton > button:active {
    transform: translateY(0px) scale(0.995);
    box-shadow:
        0 10px 20px rgba(37, 99, 235, 0.30),
        0 0 18px rgba(56, 189, 248, 0.65);
}

/* FEATURE GRID */
.section-heading {
    margin-top: 2.6rem;
    margin-bottom: 0.4rem;
    font-size: 1.15rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #0f172a;
    opacity: 0.9;
}

.section-subtitle {
    font-size: 0.9rem;
    color: #4b5563;
    opacity: 0.85;
    margin-bottom: 1.2rem;
}

.feature-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0,1fr));
    gap: 1.1rem;
}

@media (max-width: 980px) {
    .feature-grid {
        grid-template-columns: repeat(2, minmax(0,1fr));
    }
}
@media (max-width: 640px) {
    .feature-grid {
        grid-template-columns: minmax(0,1fr);
    }
}

.feature-card {
    border-radius: 18px;
    padding: 1.2rem 1.25rem 1.3rem 1.25rem;
    background:
        radial-gradient(circle at top left, rgba(191,219,254,0.55), transparent 70%),
        #ffffff;
    border: 1px solid #d1d5db;
    box-shadow:
        0 16px 32px rgba(15,23,42,0.08),
        0 0 0 1px rgba(243,244,246,0.95);
    position: relative;
    overflow: hidden;
}

.feature-card::after {
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at bottom right, rgba(191,219,254,0.7), transparent 65%);
    opacity: 0;
    transition: opacity 0.25s ease;
}

.feature-card:hover::after {
    opacity: 1;
}

.feature-icon {
    font-size: 1.1rem;
    margin-bottom: 0.4rem;
}

.feature-title {
    font-size: 1.02rem;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 0.25rem;
}

.feature-body {
    font-size: 0.9rem;
    color: #4b5563;
    opacity: 0.95;
}

/* STATS ROW */
.stats-row {
    margin-top: 2.2rem;
    display: grid;
    grid-template-columns: repeat(3, minmax(0,1fr));
    gap: 1.0rem;
}

@media (max-width: 860px) {
    .stats-row {
        grid-template-columns: repeat(2, minmax(0,1fr));
    }
}
@media (max-width: 640px) {
    .stats-row {
        grid-template-columns: minmax(0,1fr);
    }
}

.stat-card {
    border-radius: 20px;
    padding: 0.95rem 1.15rem 1.1rem;
    background: #ffffff;
    border: 1px solid #e5e7eb;
    box-shadow:
        0 14px 28px rgba(15, 23, 42, 0.10),
        0 0 0 1px rgba(243,244,246,0.95);
}

.stat-label {
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #6b7280;
}

.stat-value {
    margin-top: 0.25rem;
    font-size: 1.4rem;
    font-weight: 800;
    color: #0f172a;
}

.stat-sub {
    margin-top: 0.1rem;
    font-size: 0.8rem;
    color: #4b5563;
    opacity: 0.9;
}

/* FOOTER */
.home-footer {
    text-align: center;
    margin-top: 2.8rem;
    font-size: 0.83rem;
    color: #6b7280;
    opacity: 0.85;
}

/* Animations (reuse) */
@keyframes backgroundShift {
    0% { background-position: 0% 10%; }
    50% { background-position: 100% 90%; }
    100% { background-position: 0% 10%; }
}

@keyframes titleGlow {
    0% {
        text-shadow: 0 0 12px rgba(129,140,248,0.65),
                     0 0 26px rgba(59,130,246,0.8);
    }
    50% {
        text-shadow: 0 0 8px rgba(129,140,248,0.7),
                     0 0 20px rgba(59,130,246,0.9);
    }
    100% {
        text-shadow: 0 0 12px rgba(129,140,248,0.65),
                     0 0 26px rgba(59,130,246,0.8);
    }
}
</style>
"""

# inject CSS for current theme
st.markdown(dark_css if current_theme == "Dark" else light_css, unsafe_allow_html=True)

# ---------------- HOME PAGE UI ----------------
st.markdown("<div class='home-shell'>", unsafe_allow_html=True)

# HERO
st.markdown(
    """
    <div class="hero-card">
        <div class="hero-badge">⚡ New • Smart Banking Assistant</div>
        <h1 class="hero-title">BankBot AI</h1>
        <p class="hero-subtitle">
            Conversational banking for your customers – securely handle balances, transactions,
            and support, powered by AI fine‑tuned for financial workflows.
        </p>
        <div class="hero-pills">
            <span class="hero-pill">🔐 Enterprise‑grade security</span>
            <span class="hero-pill">🤖 Natural language understanding</span>
            <span class="hero-pill">📈 Real‑time insights</span>
            <span class="hero-pill">⚙️ Easy integration</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# CTA ROW (buttons are real Streamlit components)
st.markdown("<div class='cta-row'>", unsafe_allow_html=True)
cta_left, cta_right, _ = st.columns([1.1, 1.1, 0.4])

with cta_left:
    if st.button("🚀 Login / Get Started", use_container_width=True, key="cta_login"):
        st.switch_page("pages/3_Login.py")

with cta_right:
    if st.button("🆕 Open New Account", use_container_width=True, key="cta_open_acct"):
        st.switch_page("pages/2_Create_Account.py")
st.markdown("</div>", unsafe_allow_html=True)

# MIDDLE TITLE
st.markdown(
    "<div class='mid-title'>Experience Intelligent Banking</div>",
    unsafe_allow_html=True,
)

# FEATURES
st.markdown(
    """
    <div class="section-heading">Why BankBot AI?</div>
    <div class="section-subtitle">
        Built for modern banking teams that need speed, safety, and an excellent customer experience.
    </div>
    <div class="feature-grid">
        <div class="feature-card">
            <div class="feature-icon">🔐</div>
            <div class="feature-title">Security‑first design</div>
            <div class="feature-body">
                Fine‑grained access control, encrypted channels, and clear audit trails for every interaction.
            </div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <div class="feature-title">Banking‑aware intelligence</div>
            <div class="feature-body">
                Understands balances, transfers, and statements with domain‑specific prompts and guardrails.
            </div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">Fast and scalable</div>
            <div class="feature-body">
                Optimized for low latency and horizontal scaling so you can support thousands of users.
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# STATS
st.markdown(
    """
    <div class="section-heading" style="margin-top:2.4rem;">At a glance</div>
    <div class="section-subtitle">
        Key metrics when deploying BankBot AI in production environments.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='stats-row'>", unsafe_allow_html=True)
col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-label">Avg. response time</div>
            <div class="stat-value">150 ms</div>
            <div class="stat-sub">Optimized for snappy conversations</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_b:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-label">Uptime</div>
            <div class="stat-value">99.9%</div>
            <div class="stat-sub">Designed for always‑on banking</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_c:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-label">Languages</div>
            <div class="stat-value">15+</div>
            <div class="stat-sub">Serve customers across regions</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("</div>", unsafe_allow_html=True)

# FAQ / DETAILS
with st.expander("💬 What can I do from here?"):
    st.markdown(
        """
        - Use **Login / Get Started** to access your personalized banking assistant.
        - Use **Open New Account** to quickly create a user and linked bank account.
        - Once logged in, you can chat with **BankBot AI**, review accounts, and more.
        """.strip()
    )

with st.expander("🔐 How is security handled?"):
    st.markdown(
        """
        - All sensitive operations can be guarded by server‑side checks.
        - Authentication and authorization are enforced before exposing account data.
        - Actions can be logged for audit and compliance requirements.
        """.strip()
    )

# FOOTER
st.markdown(
    """
    <div class="home-footer">
        © 2025 BankBot AI • Secure, intelligent banking assistant
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("</div>", unsafe_allow_html=True)  # close home-shell

import sys
import os
import json
import joblib
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay, accuracy_score

# --------------------------------------------------
# PATH SETUP
# --------------------------------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

INTENTS_PATH = os.path.join(BASE_DIR, "nlu_engine", "intents.json")
MODEL_DIR = os.path.join(BASE_DIR, "ui", "models", "intent_model")
MODEL_PATH = os.path.join(MODEL_DIR, "intent_model.pkl")

# --------------------------------------------------
# DB IMPORTS
# --------------------------------------------------
from database.bank_crud import (
    get_chat_logs,
    get_intent_distribution,
    get_top_queries
)

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Admin Panel | BankBot AI",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# ADMIN CHECK (must come after set_page_config)
# --------------------------------------------------
if "user_name" not in st.session_state or st.session_state.get("role") != "admin":
    st.error("🚫 Access Denied: Admins only")
    st.stop()
st.markdown("""
<style>
/* ---------------- GLOBAL ---------------- */
header, footer {visibility: hidden;}
.stApp {
    background: radial-gradient(circle at top left, #e0f2fe 0%, #f9fafb 40%, #fee2e2 100%);
    color: #111827;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    animation: bgFloat 18s ease-in-out infinite alternate;
}

/* animated soft blobs in background */
.stApp::before {
    content: "";
    position: fixed;
    inset: -120px;
    background:
        radial-gradient(circle at 10% 20%, rgba(59,130,246,0.16) 0, transparent 55%),
        radial-gradient(circle at 80% 10%, rgba(236,72,153,0.16) 0, transparent 55%),
        radial-gradient(circle at 10% 80%, rgba(52,211,153,0.18) 0, transparent 55%);
    opacity: 0.9;
    z-index: -1;
    filter: blur(4px);
    animation: blobMove 26s ease-in-out infinite alternate;
}

@keyframes bgFloat {
    0%   {background-position: 0% 0%;}
    50%  {background-position: 50% 50%;}
    100% {background-position: 100% 0%;}
}

@keyframes blobMove {
    0%   {transform: translate3d(0,0,0) scale(1);}
    50%  {transform: translate3d(-30px,10px,0) scale(1.05);}
    100% {transform: translate3d(20px,-20px,0) scale(1.08);}
}

/* ---------------- TOP NAVBAR ---------------- */
.top-nav {
    position: sticky;
    top: 0.5rem;
    z-index: 1000;
    margin-bottom: 1.25rem;
}

.glass-nav {
    background: linear-gradient(135deg, rgba(255,255,255,0.92), rgba(239,246,255,0.96));
    backdrop-filter: blur(18px);
    border-radius: 999px;
    padding: 0.55rem 1.2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 18px 45px rgba(15,23,42,0.18);
    border: 1px solid rgba(148,163,184,0.45);
}

.nav-left {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.nav-logo {
    width: 28px;
    height: 28px;
    border-radius: 999px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: radial-gradient(circle at 30% 0, #f97316 0, #ef4444 40%, #4f46e5 100%);
    color: #f9fafb;
    box-shadow: 0 10px 30px rgba(148,163,184,0.6);
    font-size: 1.1rem;
}

.nav-title {
    font-weight: 800;
    font-size: 0.95rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: #0f172a;
}

.nav-right {
    display: flex;
    align-items: center;
    gap: 0.35rem;
}

.nav-pill {
    padding: 0.25rem 0.7rem;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 600;
    border: 1px solid rgba(148,163,184,0.5);
    background: rgba(248,250,252,0.95);
    color: #0f172a;
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
}

.nav-pill-primary {
    background: linear-gradient(120deg, #4f46e5, #06b6d4);
    border: none;
    color: #f9fafb;
    box-shadow: 0 10px 25px rgba(37,99,235,0.45);
}

/* ---------------- GLASS CARDS ---------------- */
.glass {
    background: rgba(255,255,255,0.9);
    backdrop-filter: blur(18px);
    border-radius: 20px;
    padding: 1.5rem;
    box-shadow: 0 18px 45px rgba(15,23,42,0.12);
    border: 1px solid rgba(148,163,184,0.35);
    animation: fadeUp 0.6s ease;
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
}

.glass:hover {
    transform: translateY(-4px);
    box-shadow: 0 26px 70px rgba(15,23,42,0.2);
    border-color: rgba(59,130,246,0.6);
}

@keyframes fadeUp {
    from {opacity:0; transform: translateY(18px);}
    to   {opacity:1; transform: translateY(0);}
}

/* ---------------- METRIC CARDS ---------------- */
.metric-box {
    background: linear-gradient(135deg, #3b82f6, #22c55e);
    border-radius: 18px;
    padding: 1.4rem;
    color: white;
    text-align: center;
    box-shadow: 0 16px 40px rgba(15,23,42,0.35);
    transition: transform 0.25s ease, box-shadow 0.25s ease, filter 0.25s ease;
    position: relative;
    overflow: hidden;
}

.metric-box::after {
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at top, rgba(255,255,255,0.22), transparent 60%);
    opacity: 0;
    transition: opacity 0.25s ease;
}

.metric-box:hover::after {
    opacity: 1;
}

.metric-box:hover {
    transform: translateY(-6px) scale(1.02);
    box-shadow: 0 24px 60px rgba(15,23,42,0.45);
    filter: brightness(1.05);
}

.metric-title {
    font-size: 0.8rem;
    opacity: 0.9;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.metric-value {
    font-size: 1.9rem;
    font-weight: 900;
}

/* ---------------- SECTION TITLES ---------------- */
.section-title {
    font-size: 1.35rem;
    font-weight: 900;
    margin-bottom: 10px;
    background: linear-gradient(90deg, #4f46e5, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* ---------------- DATAFRAME ---------------- */
[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 14px 35px rgba(15,23,42,0.12);
    border: 1px solid rgba(209,213,219,0.8);
}

/* ---------------- BUTTONS ---------------- */
.stButton button {
    background: linear-gradient(90deg, #4f46e5, #06b6d4);
    color: white;
    font-weight: 700;
    border-radius: 999px;
    padding: 0.6rem 1.4rem;
    border: none;
    box-shadow: 0 12px 30px rgba(15,23,42,0.35);
    transition: transform 0.2s ease, box-shadow 0.2s ease, filter 0.2s ease;
}

.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 18px 45px rgba(15,23,42,0.45);
    filter: brightness(1.05);
}

/* ---------------- TABS (light accent) ---------------- */
[data-testid="stTabs"] button {
    border-radius: 999px !important;
    padding: 0.45rem 1.0rem;
    margin-right: 0.35rem;
    font-weight: 600;
    font-size: 0.85rem;
    border: 1px solid transparent;
    background: rgba(248,250,252,0.85);
    color: #4b5563;
    transition: background 0.2s ease, color 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease, transform 0.15s ease;
}

[data-testid="stTabs"] button[aria-selected="true"] {
    background: linear-gradient(120deg, #4f46e5, #ec4899);
    color: #f9fafb;
    box-shadow: 0 10px 32px rgba(79,70,229,0.4);
    border-color: transparent;
    transform: translateY(-1px);
}

/* ---------------- SMALL UTILITIES ---------------- */
h1, h2, h3, h4, h5 {
    color: #0f172a;
}

hr {
    border-color: rgba(148,163,184,0.5);
}

/* ---------------- SCROLLBAR ---------------- */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}
::-webkit-scrollbar-track {
    background: transparent;
}
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #4f46e5, #ec4899);
    border-radius: 999px;
}

/* ---------------- TAB 5 PERFORMANCE CARDS ---------------- */
.perf-row {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    margin-bottom: 1rem;
}
.perf-card {
    flex: 1 1 0;
    min-width: 190px;
    background: linear-gradient(135deg, #eef2ff, #e0f2fe);
    border-radius: 16px;
    padding: 0.9rem 1.1rem;
    box-shadow: 0 14px 35px rgba(15,23,42,0.18);
    border: 1px solid rgba(129,140,248,0.55);
    position: relative;
    overflow: hidden;
}
.perf-card::before {
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at 0 0, rgba(255,255,255,0.55), transparent 55%);
    opacity: 0.7;
    pointer-events: none;
}
.perf-card-label {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #4b5563;
    margin-bottom: 0.25rem;
}
.perf-card-value {
    font-size: 1.5rem;
    font-weight: 800;
    color: #111827;
}
.perf-card-sub {
    font-size: 0.8rem;
    color: #6b7280;
    margin-top: 0.15rem;
}
</style>
""", unsafe_allow_html=True)

# ✅ ADD BACK PAGE TITLE + TOP NAVBAR HERE
st.title("🛠️ Admin Panel – BankBot AI")
st.caption("Milestone 4: Admin Dashboard & Knowledge Base")

st.markdown("""
<div class="top-nav">
  <div class="glass-nav">
    <div class="nav-left">
      <div class="nav-logo">🏦</div>
      <div class="nav-title">BankBot AI · Admin Console</div>
    </div>
    <div class="nav-right">
      <span class="nav-pill nav-pill-primary">Admin Panel</span>
      <span class="nav-pill">Model Monitor</span>
      <span class="nav-pill">v1.0</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD INTENTS
# --------------------------------------------------
if not os.path.exists(INTENTS_PATH):
    with open(INTENTS_PATH, "w") as f:
        json.dump({"intents": []}, f, indent=4)

with open(INTENTS_PATH) as f:
    intents_list = json.load(f)["intents"]

if "show_retrain" not in st.session_state:
    st.session_state.show_retrain = False

# --------------------------------------------------
# TABS
# --------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Analytics",
    "🧾 Chat Logs",
    "📚 Knowledge Base",
    "👤 Admin Dashboard",
    "🧪 Model Performance"
])

# ==================================================
# TAB 1: ANALYTICS
# ==================================================
with tab1:
    st.subheader("📊 Chatbot Analytics")
    col1, col2 = st.columns(2)

    # Intent Distribution
    with col1:
        st.markdown("### 🎯 Intent Distribution")
        data = get_intent_distribution()
        if data:
            df = pd.DataFrame(data, columns=["Intent", "Count"])
            st.bar_chart(df.set_index("Intent"))
        else:
            st.info("No data available")

    # Top Queries
    with col2:
        st.markdown("### 🔥 Top User Queries")
        queries = get_top_queries()
        if queries:
            st.table(pd.DataFrame(queries, columns=["Query", "Count"]))
        else:
            st.info("No queries found")

    st.markdown("---")

    # Small Pie Chart for Average Confidence
    st.markdown("### 🥧 Average Confidence per Intent")
    logs = get_chat_logs(200)
    if logs:
        df_logs = pd.DataFrame(
            logs,
            columns=["User", "Query", "Intent", "Confidence", "Timestamp"]
        )
        df_conf = df_logs.groupby("Intent")["Confidence"].mean()
        pie_col1, pie_col2, pie_col3 = st.columns([1, 1, 2])
        with pie_col2:
            fig, ax = plt.subplots(figsize=(2.8, 2.8))
            ax.pie(df_conf.values, labels=df_conf.index, autopct="%1.0f%%", startangle=90, textprops={"fontsize": 8})
            ax.axis("equal")
            st.pyplot(fig)

    # Training Strength
    if intents_list:
        df_train = pd.DataFrame({
            "Intent": [i["name"] for i in intents_list],
            "Examples": [len(i["examples"]) for i in intents_list]
        })
        st.markdown("### 📊 Training Strength")
        st.bar_chart(df_train.set_index("Intent"))

# ==================================================
# TAB 2: CHAT LOGS
# ==================================================
with tab2:
    st.subheader("🧾 User Chat Logs")
    logs = get_chat_logs(200)
    if logs:
        df = pd.DataFrame(
            logs,
            columns=["User", "Query", "Intent", "Confidence", "Timestamp"]
        )
        st.dataframe(df, use_container_width=True)
        st.download_button("⬇️ Download Logs", df.to_csv(index=False), "chat_logs.csv", "text/csv")
    else:
        st.info("No chat logs available")

# ==================================================
# TAB 3: KNOWLEDGE BASE
# ==================================================
with tab3:
    st.subheader("📚 Knowledge Base – Intent Training")
    col1, col2, col3 = st.columns([2.5, 2.5, 1.5])

    # VIEW EXISTING INTENTS
    with col1:
        st.markdown("### 🧠 Existing Intents")
        for intent in intents_list:
            with st.expander(f"{intent['name']} ({len(intent['examples'])} examples)"):
                for ex in intent["examples"]:
                    st.write(f"• {ex}")

    # ADD EXAMPLES
    with col2:
        st.markdown("### ➕ Add Example")
        intent_names = [i["name"] for i in intents_list]
        selected = st.selectbox("Select Intent", intent_names + ["➕ Other (New Intent)"])
        if selected == "➕ Other (New Intent)":
            intent_name = st.text_input("New Intent Name")
        else:
            intent_name = selected
        example = st.text_area("Training Example")

        if st.button("Add Example"):
            if not intent_name or not example:
                st.warning("All fields required")
            else:
                intent = next((i for i in intents_list if i["name"] == intent_name), None)
                if intent:
                    intent["examples"].append(example)
                else:
                    intents_list.append({"name": intent_name, "examples": [example]})
                with open(INTENTS_PATH, "w") as f:
                    json.dump({"intents": intents_list}, f, indent=4)
                st.session_state.show_retrain = True
                st.success("Example added successfully")

    # RETRAIN
    with col3:
        st.markdown("### 🔁 Model Training")
        if st.session_state.show_retrain:
            if st.button("Retrain Model"):
                X, y = [], []
                for i in intents_list:
                    for ex in i["examples"]:
                        X.append(ex)
                        y.append(i["name"])
                model = Pipeline([("tfidf", TfidfVectorizer()), ("lr", LogisticRegression(max_iter=500))])
                model.fit(X, y)
                os.makedirs(MODEL_DIR, exist_ok=True)
                joblib.dump(model, MODEL_PATH)
                st.success("Model retrained successfully")
                st.session_state.show_retrain = False
        else:
            st.info("No pending changes")

# ==================================================
# TAB 4: ADMIN DASHBOARD
# ==================================================
with tab4:
    st.subheader("👤 Admin Dashboard")

    # ------------------- Basic Stats -------------------
    total_intents = len(intents_list)
    total_examples = sum(len(i["examples"]) for i in intents_list)
    top_intent = max(
        intents_list,
        key=lambda x: len(x["examples"]),
        default={"name": "N/A"}
    )["name"]

    model_trained = os.path.exists(MODEL_PATH)

    # st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">👤 Admin Overview</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-title">📌 Total Intents</div>
            <div class="metric-value">{total_intents}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-box" style="background:linear-gradient(135deg,#22c55e,#4ade80)">
            <div class="metric-title">📝 Total Examples</div>
            <div class="metric-value">{total_examples}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-box" style="background:linear-gradient(135deg,#f97316,#facc15)">
            <div class="metric-title">🔥 Top Intent</div>
            <div class="metric-value">{top_intent}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-box" style="background:linear-gradient(135deg,#a855f7,#ec4899)">
            <div class="metric-title">🤖 Model Status</div>
            <div class="metric-value">{'Trained' if model_trained else 'Not Trained'}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # ------------------- Dataset Readiness -------------------
    st.markdown("### 📊 Dataset Readiness")

    avg_examples = total_examples / max(total_intents, 1)

    readiness = min(avg_examples / 10, 1.0)  # 10 examples = ideal
    st.progress(readiness)

    st.caption(
        f"Average examples per intent: **{avg_examples:.1f}** "
        "(Recommended ≥ 10)"
    )

    if avg_examples < 5:
        st.warning("⚠️ Dataset is very small. Model may overfit.")
    elif avg_examples < 10:
        st.info("ℹ️ Dataset is moderate. Adding more examples will improve accuracy.")
    else:
        st.success("✅ Dataset size is healthy.")

    # ------------------- Intent Distribution -------------------
    st.markdown("### 🧩 Intent Distribution")

    intent_df = pd.DataFrame([
        {"Intent": i["name"], "Examples": len(i["examples"])}
        for i in intents_list
    ]).sort_values("Examples", ascending=False)

    fig_intent, ax_intent = plt.subplots(figsize=(4.5, 2.5))
    fig_intent.set_dpi(120)

    ax_intent.bar(
        intent_df["Intent"],
        intent_df["Examples"]
    )

    ax_intent.set_ylabel("Examples", fontsize=8)
    plt.xticks(rotation=30, ha="right", fontsize=8)
    plt.yticks(fontsize=8)
    plt.tight_layout(pad=0.4)

    st.pyplot(fig_intent)
    plt.close(fig_intent)

    # ------------------- Admin Insights -------------------
    st.markdown("### 🧠 Admin Insights")

    st.info(
        f"""
        • **{total_intents} intents** configured in the chatbot  
        • Most trained intent: **{top_intent}**  
        • Model is **{'ready for testing' if model_trained else 'not trained yet'}**  
        • Add more real user queries to improve robustness
        """
    )

# ==================================================
# TAB 5: MODEL PERFORMANCE (FINAL NEAT VERSION)
# ==================================================
from datetime import datetime
from io import BytesIO

with tab5:
    # st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.subheader("🧪 Model Performance Evaluation")

    # ------------------- Prepare Dataset -------------------
    X, y = [], []
    for intent in intents_list:
        for ex in intent["examples"]:
            X.append(ex)
            y.append(intent["name"])

    total_examples = len(X)
    unique_intents = set(y)
    min_examples_per_intent = min([y.count(label) for label in unique_intents])

    # ------------------- Dataset Validation -------------------
    if total_examples < 10:
        st.warning("⚠️ Dataset is too small for reliable evaluation. Add more examples per intent.")
        st.stop()

    if min_examples_per_intent < 3:
        st.warning("⚠️ Some intents have less than 3 examples. Metrics will be very unstable.")
        st.stop()

    # ------------------- Train / Test Split -------------------
    stratify_param = y
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=stratify_param
    )

    st.info(
        f"Dataset Split: {len(X_train)} training / {len(X_test)} testing samples "
        f"across {len(unique_intents)} intents"
    )

    # ------------------- Train evaluation model ONLY on train split -------------------
    # (ignore any previously saved chatbot model to avoid data leakage)
    model = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("lr", LogisticRegression(max_iter=500))
    ])
    model.fit(X_train, y_train)

    # ------------------- Predictions -------------------
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    train_acc = accuracy_score(y_train, y_train_pred)
    test_acc = accuracy_score(y_test, y_test_pred)

    # ------------------- Accuracy Metrics (cards) -------------------
    st.markdown("### ⚙️ Performance Snapshot")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="perf-card">
          <div class="perf-card-label">Train Accuracy</div>
          <div class="perf-card-value">{train_acc*100:.2f}%</div>
          <div class="perf-card-sub">On {len(X_train)} samples</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="perf-card">
          <div class="perf-card-label">Test Accuracy</div>
          <div class="perf-card-value">{test_acc*100:.2f}%</div>
          <div class="perf-card-sub">On {len(X_test)} samples</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="perf-card">
          <div class="perf-card-label">Dataset Size</div>
          <div class="perf-card-value">{total_examples}</div>
          <div class="perf-card-sub">{len(unique_intents)} intents</div>
        </div>
        """, unsafe_allow_html=True)

    # ------------------- Overfitting / too-perfect metrics notice -------------------
    if train_acc == 1.0 or test_acc == 1.0:
        st.warning(
            "⚠️ Accuracy is 100%. This usually means:\n"
            "• Very small dataset, or\n"
            "• Examples are almost identical per intent.\n\n"
            "Add more diverse user queries per intent and rerun this evaluation."
        )

    # ------------------- Cross Validation (robust) -------------------
    st.markdown("### 🔁 Cross-Validation")

    # avoid ValueError when some intents have too few examples
    if min_examples_per_intent < 2 or len(unique_intents) < 1 or len(X) < 3:
        st.info("Not enough data for reliable cross-validation.")
    else:
        n_splits = min(5, min_examples_per_intent, len(X))
        if n_splits < 2:
            st.info("Not enough samples per intent for cross-validation.")
        else:
            cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
            cv_scores = cross_val_score(model, X, y, cv=cv, scoring="accuracy")
            mean_cv = cv_scores.mean() * 100

            cv_col1, cv_col2 = st.columns([1, 2])
            with cv_col1:
                st.markdown(f"""
                <div class="perf-card">
                  <div class="perf-card-label">Mean CV Accuracy</div>
                  <div class="perf-card-value">{mean_cv:.2f}%</div>
                  <div class="perf-card-sub">{n_splits} folds</div>
                </div>
                """, unsafe_allow_html=True)
            with cv_col2:
                st.caption(f"Fold Accuracies: {[f'{s*100:.1f}%' for s in cv_scores]}")

    # ------------------- Classification Report -------------------
    st.markdown("### 📄 Classification Report")
    report = classification_report(
        y_test,
        y_test_pred,
        labels=model.classes_,
        output_dict=True,
        zero_division=0
    )
    df_report = pd.DataFrame(report).transpose().round(2)
    st.dataframe(df_report, height=220, width="stretch")

    # ==========================================================
    # MODEL DIAGNOSTICS
    # ==========================================================
    st.markdown("## 📊 Model Diagnostics")

    col1, col2 = st.columns(2)

    # ================= CONFUSION MATRIX =================
    with col1:
        st.markdown("### 🧮 Confusion Matrix")

        cm = confusion_matrix(y_test, y_test_pred)

        fig_cm, ax_cm = plt.subplots(figsize=(2.8, 2.8))
        fig_cm.set_dpi(130)

        disp = ConfusionMatrixDisplay(
            confusion_matrix=cm,
            display_labels=model.classes_
        )

        disp.plot(
            ax=ax_cm,
            cmap="Blues",
            colorbar=False,
            values_format="d",
            text_kw={"fontsize": 7}
        )

        ax_cm.set_xlabel("Predicted", fontsize=7)
        ax_cm.set_ylabel("Actual", fontsize=7)
        plt.xticks(rotation=30, ha="right", fontsize=7)
        plt.yticks(fontsize=7)
        plt.tight_layout(pad=0.3)

        st.pyplot(fig_cm)

        buf_cm = BytesIO()
        fig_cm.savefig(buf_cm, format="png", dpi=300, bbox_inches="tight")
        st.download_button(
            "⬇️ Download CM",
            buf_cm.getvalue(),
            file_name="confusion_matrix.png",
            mime="image/png"
        )

        plt.close(fig_cm)

    # ================= F1 SCORE =================
    with col2:
        st.markdown("### 🎯 Intent-wise F1 Score")

        # robust to classes missing in y_test
        f1_scores = [
            report.get(label, {}).get("f1-score", 0.0)
            for label in model.classes_
        ]
        df_f1 = pd.DataFrame({"Intent": model.classes_, "F1": f1_scores})

        fig_f1, ax_f1 = plt.subplots(figsize=(3.2, 2.0))
        fig_f1.set_dpi(130)

        ax_f1.bar(df_f1["Intent"], df_f1["F1"])
        ax_f1.set_ylim(0, 1.05)
        ax_f1.set_ylabel("F1", fontsize=7)

        plt.xticks(rotation=30, ha="right", fontsize=7)
        plt.yticks(fontsize=7)

        for i, v in enumerate(df_f1["F1"]):
            ax_f1.text(i, v + 0.02, f"{v:.2f}", ha="center", fontsize=6)

        plt.tight_layout(pad=0.3)

        st.pyplot(fig_f1)

        buf_f1 = BytesIO()
        fig_f1.savefig(buf_f1, format="png", dpi=300, bbox_inches="tight")
        st.download_button(
            "⬇️ Download F1",
            buf_f1.getvalue(),
            file_name="f1_score.png",
            mime="image/png"
        )

        plt.close(fig_f1)

    # ------------------- Prediction Confidence -------------------
    st.markdown("### 🔍 Prediction Confidence (Sample)")
    sample_texts = X_test[:5]
    probas = model.predict_proba(sample_texts)
    preds = model.predict(sample_texts)

    df_conf = pd.DataFrame([
        {
            "Input Text": t,
            "Predicted Intent": p,
            "Confidence (%)": round(max(pr) * 100, 2)
        }
        for t, p, pr in zip(sample_texts, preds, probas)
    ])

    st.dataframe(df_conf, height=200, width="stretch")

    # ------------------- Intent Examples Count -------------------
    st.markdown("### 📝 Examples per Intent")
    df_counts = pd.DataFrame([
        {"Intent": i["name"], "Examples": len(i["examples"])}
        for i in intents_list
    ]).sort_values("Examples", ascending=False)

    st.dataframe(df_counts, height=200, width="stretch")

    # ------------------- Last Retrain Info -------------------
    if os.path.exists(MODEL_PATH):
        last_retrain = datetime.fromtimestamp(
            os.path.getmtime(MODEL_PATH)
        ).strftime("%Y-%m-%d %H:%M:%S")
        st.markdown(f"**Last Model Retrain:** {last_retrain}")
    else:
        st.markdown("**Model has not been trained yet.**")

    # ------------------- Final Note -------------------
    if min_examples_per_intent < 5:
        st.info("ℹ️ Few examples per intent — metrics are indicative, not absolute.")

    st.markdown('</div>', unsafe_allow_html=True)

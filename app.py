
from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# RR AUCTION INTELLIGENCE | IPL 2027
# Data-driven scouting interface. Not a live auction feed.
# ============================================================

st.set_page_config(
    page_title="RR Auction Intelligence | IPL 2027",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_DIR = Path("data")
FILES = {
    "strategy": "rr_final_auction_strategy.csv",
    "middle": "rr_final_middle_order_recruitment.csv",
    "squad": "rr_squad_audit.csv",
    "bowling": "rr_bowling_evidence.csv",
    "gaps": "rr_gap_matrix.csv",
    "opening_conclusion": "rr_opening_role_conclusion.csv",
    "opening_ranking": "rr_opening_combined_ranking.csv",
    "opening_evidence": "rr_opening_player_evidence.csv",
}

# ---------- Theme ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800&family=Inter:wght@400;500;600;700;800&display=swap');
:root {
  --rr-pink: #ec3f8b;
  --rr-pink-light: #ff75ad;
  --rr-navy: #07152f;
  --rr-panel: #102344;
  --rr-panel2: #142b50;
  --rr-line: rgba(166,190,226,.16);
  --rr-text: #f4f7ff;
  --rr-muted: #aab9d2;
  --rr-teal: #38d6b0;
}
.stApp {
  background:
    radial-gradient(ellipse at 78% -8%, rgba(236,63,139,.18), transparent 34%),
    radial-gradient(ellipse at 4% 22%, rgba(38,103,180,.16), transparent 35%),
    linear-gradient(135deg, #06132b 0%, #091a37 52%, #07152f 100%);
  color: var(--rr-text);
  font-family: 'Inter', sans-serif;
}
[data-testid="stHeader"] { background: rgba(5,15,34,.82); }
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #081630 0%, #0d2040 100%);
  border-right: 1px solid var(--rr-line);
}
[data-testid="stSidebar"] * { color: #eaf0ff; }
.block-container { padding-top: 1.25rem; padding-bottom: 2.4rem; max-width: 1600px; }
h1,h2,h3 { font-family: 'Barlow Condensed','Inter',sans-serif !important; letter-spacing: .3px; color: #fff; }
h1 { font-size: 2.7rem !important; }
h2 { font-size: 1.8rem !important; }
h3 { font-size: 1.35rem !important; }
p, label, span, div { }
.rr-topbar {
  display:flex; align-items:center; justify-content:space-between; gap:16px;
  padding: 17px 21px; margin-bottom: 18px; border:1px solid var(--rr-line);
  border-radius:16px; background:linear-gradient(105deg,rgba(16,35,68,.96),rgba(10,25,50,.9));
  box-shadow:0 12px 34px rgba(0,0,0,.20);
}
.rr-brand { font-family:'Barlow Condensed'; font-weight:800; font-size:25px; letter-spacing:1px; color:#fff; line-height:1; }
.rr-brand span { color:var(--rr-pink-light); }
.rr-sub { color:var(--rr-muted); font-size:10px; letter-spacing:2px; margin-top:6px; }
.rr-live { color:#071b31; background:var(--rr-teal); border-radius:30px; padding:7px 12px; font-size:10px; font-weight:800; letter-spacing:1px; }
.rr-panel {
  background:linear-gradient(145deg,rgba(19,43,79,.96),rgba(11,29,57,.96));
  border:1px solid var(--rr-line); border-radius:15px; padding:16px 18px;
  box-shadow:0 10px 26px rgba(0,0,0,.16); min-height:100%;
}
.rr-kpi-label { color:#aab9d2; font-size:11px; text-transform:uppercase; letter-spacing:1.2px; font-weight:700; }
.rr-kpi-value { color:#fff; font-family:'Barlow Condensed'; font-size:34px; font-weight:800; margin-top:3px; }
.rr-kpi-note { color:#91a5c5; font-size:11px; margin-top:2px; }
.rr-pink { color:var(--rr-pink-light); }
.rr-section { color:#fff; font-family:'Barlow Condensed'; font-size:22px; font-weight:700; margin:8px 0 12px; }
.rr-muted { color:var(--rr-muted); font-size:12px; }
div[data-testid="stMetric"] {
  background:linear-gradient(145deg,#142b50,#0e2040);
  border:1px solid var(--rr-line); border-radius:14px; padding:14px 16px;
}
div[data-testid="stMetric"] label { color:#aab9d2 !important; text-transform:uppercase; font-size:10px !important; letter-spacing:1px; }
div[data-testid="stMetric"] [data-testid="stMetricValue"] { color:#fff !important; font-family:'Barlow Condensed'; }
.stTabs [data-baseweb="tab-list"] { gap:8px; background:transparent; }
.stTabs [data-baseweb="tab"] { background:#102344; border:1px solid var(--rr-line); border-radius:8px 8px 0 0; color:#dbe6fa; }
.stTabs [aria-selected="true"] { background:#ec3f8b !important; color:white !important; }
.stButton button, .stDownloadButton button {
  background:linear-gradient(90deg,#ec3f8b,#c92e78); color:white; border:0; border-radius:9px; font-weight:700;
}
.stButton button:hover, .stDownloadButton button:hover { color:white; border:1px solid #ff9bc2; }
.stSelectbox [data-baseweb="select"] > div, .stMultiSelect [data-baseweb="select"] > div,
.stTextInput input { background:#102344; color:white; border-color:var(--rr-line); }
.stDataFrame, [data-testid="stDataFrame"] { border:1px solid var(--rr-line); border-radius:10px; overflow:hidden; }
hr { border-color:var(--rr-line); }
small { color:var(--rr-muted); }
footer {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ---------- Helpers ----------
@st.cache_data
def load_csv(filename):
    path = DATA_DIR / filename
    if not path.exists():
        return None
    try:
        return pd.read_csv(path)
    except Exception as exc:
        st.error(f"Could not read {filename}: {exc}")
        return None

data = {key: load_csv(filename) for key, filename in FILES.items()}

def has(key):
    return data.get(key) is not None and not data[key].empty

def first_existing(df, candidates):
    if df is None:
        return None
    for c in candidates:
        if c in df.columns:
            return c
    return None

def safe_num(series):
    return pd.to_numeric(series, errors="coerce")

def fmt_num(v, digits=1):
    try:
        if pd.isna(v): return "—"
        return f"{float(v):,.{digits}f}"
    except Exception:
        return str(v)

def panel_metric(label, value, note=""):
    st.markdown(
        f'<div class="rr-panel"><div class="rr-kpi-label">{label}</div>'
        f'<div class="rr-kpi-value">{value}</div><div class="rr-kpi-note">{note}</div></div>',
        unsafe_allow_html=True
    )

def show_table(df, columns=None, height=390):
    if df is None or df.empty:
        st.info("No records available in this dataset.")
        return
    view = df.copy()
    if columns:
        view = view[[c for c in columns if c in view.columns]]
    st.dataframe(view, use_container_width=True, hide_index=True, height=height)

def chart_layout(fig, height=340):
    fig.update_layout(
        height=height, template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#eaf0ff", family="Inter"),
        margin=dict(l=12,r=12,t=38,b=12), legend_title_text=""
    )
    fig.update_xaxes(gridcolor="rgba(166,190,226,.12)", zerolinecolor="rgba(166,190,226,.12)")
    fig.update_yaxes(gridcolor="rgba(166,190,226,.12)", zerolinecolor="rgba(166,190,226,.12)")
    return fig

def csv_download(df, label, filename):
    if df is not None and not df.empty:
        st.download_button(label, df.to_csv(index=False).encode("utf-8"), filename, "text/csv")

# ---------- Header ----------
st.markdown("""
<div class="rr-topbar">
  <div>
    <div class="rr-brand">RAJASTHAN <span>ROYALS</span> | AUCTION INTELLIGENCE</div>
    <div class="rr-sub">IPL 2027 · SCOUTING & RECRUITMENT STRATEGY · HISTORICAL WINDOW 2022–2026</div>
  </div>
  <div class="rr-live">● STRATEGY MODE</div>
</div>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
st.sidebar.markdown("## 🏏 RR INTELLIGENCE")
st.sidebar.caption("IPL 2027 · Auction Strategy Platform")
page = st.sidebar.radio(
    "WORKSPACE",
    ["Auction Arena", "Squad Matrix", "Opening Analysis", "Middle-Order Lab",
     "Bowling Lab", "Strategy Board", "Methodology & Data"]
)
st.sidebar.divider()
st.sidebar.markdown("**DATA STATUS**")
for key, label in [
    ("strategy","Auction strategy"),("middle","Middle-order shortlist"),
    ("squad","Squad audit"),("bowling","Bowling evidence"),
    ("gaps","Role gap matrix"),("opening_evidence","Opening evidence")
]:
    status = "LOADED" if has(key) else "MISSING"
    st.sidebar.markdown(f"{'🟢' if has(key) else '🔴'} {label}: `{status}`")
st.sidebar.divider()
st.sidebar.caption("Historical analysis is not a live auction feed.")
st.sidebar.caption("2027 availability / retention: verify independently.")

# ---------- Page: Auction Arena ----------
if page == "Auction Arena":
    st.title("Live Bidding Arena")
    st.caption("Strategic command centre · Research-backed auction preparation")
    strategy = data["strategy"]
    middle = data["middle"]
    squad = data["squad"]
    bowling = data["bowling"]

    c1,c2,c3,c4 = st.columns(4)
    with c1: panel_metric("Roles assessed", len(strategy) if strategy is not None else "—", "Recruitment role map")
    with c2: panel_metric("Middle-order shortlist", len(middle) if middle is not None else "—", "Qualified candidates")
    with c3:
        high_count = int(strategy["priority"].astype(str).str.lower().eq("high").sum()) if strategy is not None and "priority" in strategy else 0
        panel_metric("High-priority roles", high_count, "Based on current strategy table")
    with c4: panel_metric("Squad records", len(squad) if squad is not None else "—", "Historical RR squad audit")

    left,right = st.columns([1.08,1])
    with left:
        st.markdown('<div class="rr-section">AUCTION STATUS</div>',unsafe_allow_html=True)
        st.markdown('<div class="rr-panel"><div class="rr-kpi-label">CURRENT RESEARCH POSITION</div><div class="rr-kpi-value rr-pink">SCOUTING BOARD READY</div><div class="rr-kpi-note">Historical IPL evidence · 2022–2026</div><hr><b>Highest identified role priority</b><h2 style="color:#ff75ad;margin:4px 0">Death Bowling</h2><span class="rr-muted">Provisional phase metrics; validate bowling calculations before final submission.</span></div>',unsafe_allow_html=True)
    with right:
        st.markdown('<div class="rr-section">PRIMARY MIDDLE-ORDER TARGETS</div>',unsafe_allow_html=True)
        if middle is not None:
            pcol = first_existing(middle,["priority"])
            ncol = first_existing(middle,["striker_name","player_name","name"])
            if pcol and ncol:
                primary = middle[middle[pcol].astype(str).str.contains("Primary",case=False,na=False)]
                for _,r in primary.head(4).iterrows():
                    scorecol=first_existing(middle,["middle_order_score"])
                    score=fmt_num(r.get(scorecol),1) if scorecol else "—"
                    st.markdown(f'<div class="rr-panel" style="padding:10px 14px;margin-bottom:8px"><b>{r[ncol]}</b><span style="float:right;color:#ff75ad;font-weight:800">{score}</span><div class="rr-muted">{r.get(pcol,"")}</div></div>',unsafe_allow_html=True)
            else: show_table(middle.head(5))
        else: st.warning("Middle-order shortlist CSV not loaded.")

    st.markdown('<div class="rr-section">ROLE PRIORITY MATRIX</div>',unsafe_allow_html=True)
    if strategy is not None:
        cols=["role","priority","recommendation","confidence"]
        show_table(strategy,cols,280)
        priority_col=first_existing(strategy,["priority"])
        role_col=first_existing(strategy,["role"])
        if priority_col and role_col:
            counts=strategy[priority_col].fillna("Unspecified").value_counts().rename_axis("Priority").reset_index(name="Roles")
            fig=px.bar(counts,x="Priority",y="Roles",color="Priority",color_discrete_sequence=["#ec3f8b","#f59bc1","#5477b5","#38d6b0","#8998b3"])
            st.plotly_chart(chart_layout(fig,260),use_container_width=True)
    else:
        st.error("Missing rr_final_auction_strategy.csv")

# ---------- Page: Squad Matrix ----------
elif page == "Squad Matrix":
    st.title("Squad Matrix")
    st.caption("Historical RR squad audit · status labels are not confirmation of 2027 retention")
    df=data["squad"]
    if df is None:
        st.error("Add data/rr_squad_audit.csv to view squad analysis.")
    else:
        role=first_existing(df,["primary_role","batting_role","player_type"])
        name=first_existing(df,["player_name","name"])
        status=first_existing(df,["status_for_2027"])
        a,b,c=st.columns(3)
        with a: panel_metric("Squad records",len(df),"Rows in historical audit")
        with b: panel_metric("Role categories",df[role].nunique() if role else "—","Available role labels")
        with c: panel_metric("2027 status", "Pending verification","Do not infer retention")
        if role:
            counts=df[role].fillna("Unclassified").value_counts().reset_index()
            counts.columns=["Role","Players"]
            fig=px.bar(counts,x="Players",y="Role",orientation="h",color="Players",color_continuous_scale=["#713052","#ec3f8b"])
            st.plotly_chart(chart_layout(fig,360),use_container_width=True)
        st.markdown("### Squad records")
        if status:
            choices=["All"]+sorted(df[status].dropna().astype(str).unique().tolist())
            filt=st.selectbox("2027 status filter",choices)
            if filt!="All": df=df[df[status].astype(str)==filt]
        show_table(df,height=470)
        csv_download(df,"Download filtered squad audit","rr_filtered_squad_audit.csv")

# ---------- Page: Opening Analysis ----------
elif page == "Opening Analysis":
    st.title("Opening Partnership & Top-Order Analysis")
    st.caption("Recovered historical opening analysis · interpret shortlist using its source metrics")
    conclusion=data["opening_conclusion"]
    ranking=data["opening_ranking"]
    evidence=data["opening_evidence"]
    if conclusion is not None:
        st.markdown("### Role conclusion")
        show_table(conclusion,height=180)
    else:
        st.info("Opening role conclusion CSV not loaded.")
    if ranking is not None:
        st.markdown("### Combined candidate ranking")
        score=first_existing(ranking,["combined_score","opening_score","average_model_rank","rank_score"])
        player=first_existing(ranking,["player_name","striker_name","batter","name"])
        if score and player:
            plot=ranking.copy()
            plot[score]=safe_num(plot[score])
            plot=plot.dropna(subset=[score]).sort_values(score,ascending=True).tail(15)
            fig=px.bar(plot,x=score,y=player,orientation="h",color=score,color_continuous_scale=["#6d3154","#ec3f8b"])
            st.plotly_chart(chart_layout(fig,420),use_container_width=True)
        show_table(ranking,height=420)
        csv_download(ranking,"Download opening ranking","rr_opening_ranking_filtered.csv")
    if evidence is not None:
        st.markdown("### Player-level evidence")
        show_table(evidence,height=400)
    if ranking is None and evidence is None:
        st.warning("No opening player-level data found. Check the two opening CSV filenames.")

# ---------- Page: Middle Order ----------
elif page == "Middle-Order Lab":
    st.title("Middle-Order Recruitment Lab")
    st.caption("Batting positions 4–7 · comparative score across the qualified candidate pool")
    df=data["middle"]
    if df is None:
        st.error("Add data/rr_final_middle_order_recruitment.csv.")
    else:
        player=first_existing(df,["striker_name","player_name","name"])
        score=first_existing(df,["middle_order_score"])
        priority=first_existing(df,["priority"])
        nation=first_existing(df,["nationality"])
        if priority:
            options=sorted(df[priority].dropna().astype(str).unique().tolist())
            chosen=st.multiselect("Recruitment tier",options,default=options)
            df=df[df[priority].astype(str).isin(chosen)]
        if nation:
            nations=["All"]+sorted(df[nation].dropna().astype(str).unique().tolist())
            nsel=st.selectbox("Nationality",nations)
            if nsel!="All": df=df[df[nation].astype(str)==nsel]
        if score:
            df[score]=safe_num(df[score])
            chartdf=df.dropna(subset=[score]).sort_values(score,ascending=True)
            if player:
                fig=px.bar(chartdf,x=score,y=player,orientation="h",color=score,color_continuous_scale=["#61304e","#ec3f8b"])
                st.plotly_chart(chart_layout(fig,max(330,25*len(chartdf))),use_container_width=True)
        m1,m2,m3=st.columns(3)
        with m1: panel_metric("Candidates",len(df),"After active filters")
        with m2: panel_metric("Mean relative score",fmt_num(df[score].mean(),2) if score and len(df) else "—","Percentile-style comparative score")
        with m3: panel_metric("Indian candidates",int(df[nation].astype(str).str.lower().eq("indian").sum()) if nation else "—","In filtered shortlist")
        st.markdown("### Candidate evidence table")
        cols=["middle_order_rank","striker_name","nationality","priority","middle_order_score","pressure_runs","pressure_balls","pressure_strike_rate","pressure_batting_average","middle_order_matches","decision"]
        show_table(df,cols,420)
        csv_download(df,"Download filtered shortlist","rr_middle_order_filtered.csv")
        if player and not df.empty:
            names=df[player].dropna().astype(str).unique().tolist()
            selected=st.selectbox("Open player profile",names)
            r=df[df[player].astype(str)==selected].iloc[0]
            st.markdown(f"### {selected}")
            metric_fields=[("Relative score","middle_order_score"),("Pressure runs","pressure_runs"),("Pressure strike rate","pressure_strike_rate"),("Pressure average","pressure_batting_average"),("Middle-order matches","middle_order_matches")]
            cols=st.columns(len(metric_fields))
            for col,(label,key) in zip(cols,metric_fields):
                with col: panel_metric(label,fmt_num(r.get(key),2), "Historical dataset value")
            for key in ["strength","risk","target_role","decision"]:
                if key in r.index and pd.notna(r[key]):
                    st.markdown(f"**{key.replace('_',' ').title()}:** {r[key]}")

# ---------- Page: Bowling ----------
elif page == "Bowling Lab":
    st.title("Bowling Phase Intelligence")
    st.caption("Phase-wise historical evidence · provisional figures pending full extras/legal-ball validation")
    df=data["bowling"]
    if df is None:
        st.error("Add data/rr_bowling_evidence.csv.")
    else:
        phase=first_existing(df,["phase"])
        bowler=first_existing(df,["bowler_name","player_name","name"])
        rank=first_existing(df,["phase_rank","average_rank"])
        if phase:
            phases=["All"]+sorted(df[phase].dropna().astype(str).unique().tolist())
            selected=st.selectbox("Bowling phase",phases)
            view=df.copy() if selected=="All" else df[df[phase].astype(str)==selected]
        else: view=df.copy()
        econ=first_existing(view,["pooled_economy","economy"])
        wickets=first_existing(view,["total_wickets","wickets"])
        balls=first_existing(view,["total_balls","balls"])
        a,b,c=st.columns(3)
        with a: panel_metric("Bowlers in view",len(view),"Historical evidence records")
        with b: panel_metric("Total wickets",fmt_num(safe_num(view[wickets]).sum(),0) if wickets else "—","Across visible records")
        with c: panel_metric("Mean pooled economy",fmt_num(safe_num(view[econ]).mean(),2) if econ else "—","Use cautiously; provisional")
        if bowler and econ:
            plot=view.copy()
            plot[econ]=safe_num(plot[econ])
            plot=plot.dropna(subset=[econ]).sort_values(econ,ascending=False)
            fig=px.bar(plot,x=econ,y=bowler,orientation="h",color=econ,color_continuous_scale=["#38d6b0","#ec3f8b"],hover_data=[c for c in ["total_wickets","seasons_played","robustness_label"] if c in plot.columns])
            st.plotly_chart(chart_layout(fig,max(360,24*len(plot))),use_container_width=True)
        show_table(view,height=440)
        csv_download(view,"Download filtered bowling evidence","rr_bowling_filtered.csv")

# ---------- Page: Strategy Board ----------
elif page == "Strategy Board":
    st.title("Auction Strategy Board")
    st.caption("Role-by-role decisions, target pools and evidence confidence")
    strategy=data["strategy"]
    gaps=data["gaps"]
    if strategy is not None:
        priority=first_existing(strategy,["priority"])
        role=first_existing(strategy,["role"])
        if priority:
            opts=["All"]+sorted(strategy[priority].dropna().astype(str).unique().tolist())
            p=st.selectbox("Filter priority",opts)
            view=strategy if p=="All" else strategy[strategy[priority].astype(str)==p]
        else: view=strategy
        show_table(view,height=350)
        for _,r in view.iterrows():
            title=f"{r.get('role','Role')} · {r.get('priority','Priority')}"
            with st.expander(title):
                for key in ["existing_rr_coverage","recommended_targets","recommendation","evidence","confidence"]:
                    if key in r.index:
                        st.markdown(f"**{key.replace('_',' ').title()}**")
                        st.write(r[key])
        csv_download(view,"Download strategy view","rr_strategy_filtered.csv")
    if gaps is not None:
        st.markdown("### Historical role-gap evidence")
        show_table(gaps,height=300)

# ---------- Page: Methodology ----------
elif page == "Methodology & Data":
    st.title("Methodology, Assumptions & Data Quality")
    st.caption("Audit trail for decision-makers · distinguish observed data from scouting judgement")
    st.markdown("""
    <div class="rr-panel">
      <h3 style="color:#ff75ad">Interpretation guardrails</h3>
      <ul>
        <li>Middle-order candidate analysis uses batting positions 4–7.</li>
        <li>The middle-order score is a weighted comparative score among the qualified candidate pool, not a probability of future success.</li>
        <li>Pressure batting average uses dismissals within the defined pressure-delivery subset; it is not necessarily a conventional career batting average.</li>
        <li>Consistency features may represent overall batting performance rather than role-specific performance.</li>
        <li>Bowling figures are provisional because extras and legal-ball assumptions require further validation.</li>
        <li>Historical performance does not prove 2027 auction availability, eligibility, retention or purse position.</li>
        <li>All squad references are historical audit records; verify the official 2027 squad before final decisions.</li>
      </ul>
    </div>
    """,unsafe_allow_html=True)
    st.markdown("### Dataset inventory")
    rows=[]
    for key,filename in FILES.items():
        df=data[key]
        rows.append({"Dataset":filename,"Status":"Loaded" if df is not None else "Missing","Rows":len(df) if df is not None else 0,"Columns":len(df.columns) if df is not None else 0})
    show_table(pd.DataFrame(rows),height=360)
    if st.button("Clear cached data and reload"):
        st.cache_data.clear()
        st.rerun()

st.divider()
st.markdown('<div style="text-align:center;color:#8295b5;font-size:11px;letter-spacing:1px">RAJASTHAN ROYALS AUCTION INTELLIGENCE · IPL 2027 · HISTORICAL SCOUTING WORKSPACE</div>',unsafe_allow_html=True)

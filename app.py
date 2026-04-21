import streamlit as st
import json
import requests
import plotly.graph_objects as go

st.set_page_config(
    page_title="BrandIQ - Personal Brand Intelligence",
    page_icon="🎯",
    layout="centered"
)

st.markdown("""
<style>
    .stApp { background-color: #0D1117; color: #E6EDF3; }
    .stTextArea textarea { background-color: #161B22 !important; color: #E6EDF3 !important; border: 1px solid #30363D !important; }
    .stTextInput input { background-color: #161B22 !important; color: #E6EDF3 !important; border: 1px solid #30363D !important; }
    .stButton button { background-color: #00C2FF !important; color: #0D1117 !important; font-weight: 600 !important; width: 100% !important; border: none !important; padding: 12px !important; border-radius: 8px !important; font-size: 16px !important; }
    .stButton button:hover { background-color: #00D4FF !important; }
    div[data-testid="stForm"] { background-color: #161B22; border: 1px solid #30363D; border-radius: 12px; padding: 24px; }
    .metric-card { background: #161B22; border: 1px solid #30363D; border-radius: 12px; padding: 20px; margin-bottom: 16px; }
    .score-green { color: #00FF87; }
    .score-yellow { color: #FFB800; }
    .score-red { color: #FF4444; }
    h1 { color: #E6EDF3 !important; }
    h2 { color: #00C2FF !important; }
    h3 { color: #E6EDF3 !important; }
    p { color: #E6EDF3 !important; }
    .stMarkdown { color: #E6EDF3; }
    hr { border-color: #30363D !important; }
    .stAlert { background-color: #161B22 !important; border: 1px solid #30363D !important; }
    .stSpinner { color: #00C2FF !important; }
    label { color: #8B949E !important; font-size: 13px !important; }
</style>
""", unsafe_allow_html=True)

# Header
col1, col2 = st.columns([1, 4])
with col1:
    st.markdown("""
    <div style="width:50px;height:50px;background:#00C2FF;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;color:#0D1117;font-size:20px;margin-top:8px;">B</div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("<h2 style='margin:0;color:#E6EDF3;'>BrandIQ</h2>", unsafe_allow_html=True)
    st.markdown("<p style='margin:0;color:#8B949E;font-size:13px;'>Personal Brand Intelligence · Powered by GPT-4o Mini</p>", unsafe_allow_html=True)

st.markdown("---")

st.markdown("<h1 style='text-align:center;font-size:32px;'>Analyze Your Personal Brand</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#8B949E;'>Enter your background — AI scores your brand, analyzes strengths, and gives you a strategic action plan.</p>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Input Form
with st.form("brand_form"):
    experience = st.text_area(
        "Experience Summary *",
        placeholder="e.g. 5+ years building ML systems at Flipkart, Airtel, and Aiera. Built production RAG pipelines and MCP servers for Wall Street clients.",
        height=120
    )
    col1, col2 = st.columns(2)
    with col1:
        target_role = st.text_input("Target Role *", placeholder="e.g. Senior ML Engineer")
    with col2:
        target_company = st.text_input("Target Company *", placeholder="e.g. Anthropic, Google, Stripe")

    submitted = st.form_submit_button("⚡ Analyze My Brand")
    st.markdown("<p style='text-align:center;color:#484F58;font-size:12px;'>Analysis takes ~10 seconds · Free to use · No data stored</p>", unsafe_allow_html=True)

# Validation + API Call
if submitted:
    if not experience or not target_role or not target_company:
        st.error("Please fill in all required fields.")
    else:
        with st.spinner("Analyzing your brand with AI..."):
            try:
                api_key = st.secrets["OPENAI_KEY"]

                prompt = f"""You are a personal brand strategist. Analyze this person and return ONLY valid JSON, no markdown, no explanation.

Experience: {experience}
Target Role: {target_role}
Target Company: {target_company}

Return this exact JSON:
{{
  "brand_score": <integer 0-100>,
  "score_label": "<EXCELLENT/GOOD/NEEDS WORK>",
  "brand_summary": "<2 sentence brand summary>",
  "archetype": "<Hero/Sage/Creator/Explorer/Ruler>",
  "fit_score": <integer 0-100>,
  "strengths": ["<strength1>", "<strength2>", "<strength3>"],
  "gaps": ["<gap1>", "<gap2>"],
  "brand_pillars": [
    {{"name": "<pillar1>", "score": <0-100>, "description": "<short desc>"}},
    {{"name": "<pillar2>", "score": <0-100>, "description": "<short desc>"}},
    {{"name": "<pillar3>", "score": <0-100>, "description": "<short desc>"}}
  ],
  "score_breakdown": {{
    "Visibility": <0-100>,
    "Authority": <0-100>,
    "Consistency": <0-100>,
    "Differentiation": <0-100>,
    "Engagement": <0-100>
  }},
  "recommendations": [
    {{"priority": "HIGH", "action": "<action>", "impact": "<impact>"}},
    {{"priority": "HIGH", "action": "<action>", "impact": "<impact>"}},
    {{"priority": "MEDIUM", "action": "<action>", "impact": "<impact>"}},
    {{"priority": "MEDIUM", "action": "<action>", "impact": "<impact>"}}
  ],
  "positioning_statement": "<one powerful positioning statement>"
}}"""

                response = requests.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "gpt-4o-mini",
                        "max_tokens": 1500,
                        "messages": [{"role": "user", "content": prompt}]
                    }
                )

                data = response.json()
                text = data["choices"][0]["message"]["content"]
                import re
                match = re.search(r'\{[\s\S]*\}', text)
                result = json.loads(match.group(0))

                # ── RESULTS ──────────────────────────────────────

                st.markdown("---")

                # Section 01 — Brand Score
                st.markdown("### 01 — Brand Score")
                score = result.get("brand_score", 0)
                score_color = "#00FF87" if score >= 80 else "#FFB800" if score >= 60 else "#FF4444"

                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=score,
                    number={"font": {"size": 48, "color": score_color}},
                    gauge={
                        "axis": {"range": [0, 100], "tickcolor": "#30363D", "tickfont": {"color": "#8B949E"}},
                        "bar": {"color": score_color},
                        "bgcolor": "#161B22",
                        "bordercolor": "#30363D",
                        "steps": [
                            {"range": [0, 60], "color": "#1a0a0a"},
                            {"range": [60, 80], "color": "#1a1500"},
                            {"range": [80, 100], "color": "#0a1a0a"}
                        ]
                    }
                ))
                fig_gauge.update_layout(
                    paper_bgcolor="#0D1117",
                    plot_bgcolor="#0D1117",
                    font={"color": "#E6EDF3"},
                    height=250,
                    margin=dict(t=20, b=20, l=40, r=40)
                )
                st.plotly_chart(fig_gauge, use_container_width=True)

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"<div style='text-align:center;background:#161B22;padding:12px;border-radius:8px;border:1px solid #30363D;'><div style='color:{score_color};font-size:18px;font-weight:700;'>{result.get('score_label','')}</div><div style='color:#8B949E;font-size:12px;'>Brand Score</div></div>", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"<div style='text-align:center;background:#161B22;padding:12px;border-radius:8px;border:1px solid #30363D;'><div style='color:#00C2FF;font-size:18px;font-weight:700;'>{result.get('archetype','')}</div><div style='color:#8B949E;font-size:12px;'>Archetype</div></div>", unsafe_allow_html=True)
                with col3:
                    st.markdown(f"<div style='text-align:center;background:#161B22;padding:12px;border-radius:8px;border:1px solid #30363D;'><div style='color:#7B61FF;font-size:18px;font-weight:700;'>{result.get('fit_score',0)}%</div><div style='color:#8B949E;font-size:12px;'>Role Fit</div></div>", unsafe_allow_html=True)

                st.markdown(f"<br><p style='text-align:center;color:#E6EDF3;font-size:15px;'>{result.get('brand_summary','')}</p>", unsafe_allow_html=True)

                # Strengths + Gaps
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("<div style='background:#0D2518;border:1px solid #1A4731;border-radius:8px;padding:14px;'>", unsafe_allow_html=True)
                    st.markdown("<div style='color:#00FF87;font-size:12px;font-weight:700;margin-bottom:8px;'>✅ STRENGTHS</div>", unsafe_allow_html=True)
                    for s in result.get("strengths", []):
                        st.markdown(f"<div style='color:#E6EDF3;font-size:13px;margin-bottom:4px;'>• {s}</div>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                with col2:
                    st.markdown("<div style='background:#1a1200;border:1px solid #3d2f00;border-radius:8px;padding:14px;'>", unsafe_allow_html=True)
                    st.markdown("<div style='color:#FFB800;font-size:12px;font-weight:700;margin-bottom:8px;'>⚠️ GAPS TO ADDRESS</div>", unsafe_allow_html=True)
                    for g in result.get("gaps", []):
                        st.markdown(f"<div style='color:#E6EDF3;font-size:13px;margin-bottom:4px;'>• {g}</div>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                st.markdown("---")

                # Section 02 — Score Breakdown
                st.markdown("### 02 — Score Breakdown")
                breakdown = result.get("score_breakdown", {})
                if breakdown:
                    fig_bar = go.Figure(go.Bar(
                        x=list(breakdown.values()),
                        y=list(breakdown.keys()),
                        orientation='h',
                        marker=dict(color="#00C2FF", line=dict(color="#0099CC", width=1)),
                        text=[f"{v}%" for v in breakdown.values()],
                        textposition='outside',
                        textfont=dict(color="#E6EDF3", size=12)
                    ))
                    fig_bar.update_layout(
                        paper_bgcolor="#0D1117",
                        plot_bgcolor="#161B22",
                        font={"color": "#E6EDF3"},
                        height=280,
                        margin=dict(t=10, b=10, l=10, r=60),
                        xaxis=dict(range=[0, 110], showgrid=False, zeroline=False, tickfont=dict(color="#8B949E")),
                        yaxis=dict(showgrid=False, tickfont=dict(color="#E6EDF3", size=13))
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)

                st.markdown("---")

                # Section 03 — Brand Pillars
                st.markdown("### 03 — Brand Pillars")
                pillars = result.get("brand_pillars", [])
                if pillars:
                    fig_radar = go.Figure(go.Scatterpolar(
                        r=[p["score"] for p in pillars] + [pillars[0]["score"]],
                        theta=[p["name"] for p in pillars] + [pillars[0]["name"]],
                        fill='toself',
                        fillcolor='rgba(0, 194, 255, 0.2)',
                        line=dict(color="#00C2FF", width=2),
                        marker=dict(color="#00C2FF", size=8)
                    ))
                    fig_radar.update_layout(
                        paper_bgcolor="#0D1117",
                        plot_bgcolor="#0D1117",
                        font={"color": "#E6EDF3"},
                        height=320,
                        polar=dict(
                            bgcolor="#161B22",
                            radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(color="#8B949E"), gridcolor="#30363D"),
                            angularaxis=dict(tickfont=dict(color="#E6EDF3", size=13), gridcolor="#30363D")
                        ),
                        margin=dict(t=20, b=20, l=40, r=40)
                    )
                    st.plotly_chart(fig_radar, use_container_width=True)

                    for p in pillars:
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            st.markdown(f"<div style='font-size:13px;font-weight:500;color:#E6EDF3;'>{p['name']} <span style='color:#8B949E;font-weight:400;'>— {p['description']}</span></div>", unsafe_allow_html=True)
                            st.progress(p["score"] / 100)
                        with col2:
                            st.markdown(f"<div style='text-align:right;color:#00C2FF;font-weight:600;font-size:14px;padding-top:4px;'>{p['score']}%</div>", unsafe_allow_html=True)

                st.markdown("---")

                # Section 04 — Action Plan
                st.markdown("### 04 — Action Plan")
                for rec in result.get("recommendations", []):
                    priority = rec.get("priority", "MEDIUM")
                    badge_color = "#00FF87" if priority == "HIGH" else "#FFB800"
                    bg_color = "#0D2518" if priority == "HIGH" else "#1a1200"
                    border_color = "#1A4731" if priority == "HIGH" else "#3d2f00"
                    st.markdown(f"""
                    <div style='background:{bg_color};border:1px solid {border_color};border-radius:8px;padding:14px;margin-bottom:10px;display:flex;gap:12px;align-items:flex-start;'>
                        <span style='background:{badge_color}22;color:{badge_color};padding:2px 8px;border-radius:4px;font-size:11px;font-weight:700;white-space:nowrap;'>{priority}</span>
                        <div>
                            <div style='color:#E6EDF3;font-weight:500;font-size:14px;margin-bottom:3px;'>{rec.get('action','')}</div>
                            <div style='color:#8B949E;font-size:12px;'>{rec.get('impact','')}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("---")

                # Section 05 — Positioning Statement
                st.markdown("### 05 — Your Positioning Statement")
                st.markdown(f"""
                <div style='background:linear-gradient(135deg,#0D1B2A,#112240);border:1px solid #00C2FF;border-radius:12px;padding:28px;text-align:center;margin-top:8px;'>
                    <div style='color:#00C2FF;font-size:11px;font-weight:700;letter-spacing:0.1em;margin-bottom:12px;'>YOUR POSITIONING STATEMENT</div>
                    <div style='color:#E6EDF3;font-size:20px;font-style:italic;line-height:1.6;'>"{result.get('positioning_statement','')}"</div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")
                st.info("Make sure your OpenAI API key is set in Streamlit secrets.")

# Footer
st.markdown("---")
st.markdown("<p style='text-align:center;color:#484F58;font-size:12px;'>Built by <a href='https://gunashree.substack.com' style='color:#00C2FF;'>Gunashree Rajakumar</a> · Systems That Scale · Powered by GPT-4o Mini · n8n backend</p>", unsafe_allow_html=True)

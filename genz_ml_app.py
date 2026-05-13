import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import plotly.express as px

# --- Configuration & Styling ---
st.set_page_config(page_title="Ghosted.ai 👻", layout="wide", page_icon="👻")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;500;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif !important;
    }
    
    /* Sleek Dark Animated Background */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #1e1b4b, #09090b, #000000);
        background-size: 200% 200%;
        animation: pulseBG 15s ease infinite;
        color: #f8fafc;
    }
    
    @keyframes pulseBG {
        0% { background-position: 0% 0%; }
        50% { background-position: 100% 100%; }
        100% { background-position: 0% 0%; }
    }
    
    /* Premium Glassmorphism Tabs and Panels */
    div[role="tabpanel"] {
        background: rgba(15, 23, 42, 0.4);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 0 16px 16px 16px;
        padding: 15px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }

    button[data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 10px 10px 0 0 !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-bottom: none !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        background: rgba(30, 27, 75, 0.8) !important;
        border-bottom: none !important;
        box-shadow: inset 0 2px 15px rgba(139, 92, 246, 0.4), 0 -2px 10px rgba(99, 102, 241, 0.3) !important;
    }
    
    button[data-baseweb="tab"][aria-selected="true"] p {
        color: #d8b4fe !important;
        text-shadow: 0 0 10px rgba(168, 85, 247, 0.6);
        font-weight: 700;
    }
    
    /* Antigravity Float Physics */
    @keyframes orbit1 {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-10px) rotate(0.5deg); }
    }
    
    @keyframes orbit2 {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-14px) rotate(-0.5deg); }
    }

    div[data-testid="column"] {
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    div[data-testid="column"]:nth-child(1) {
        animation: orbit1 8s ease-in-out infinite;
    }
    
    div[data-testid="column"]:nth-child(2) {
        animation: orbit2 11s ease-in-out infinite;
        animation-delay: -3s;
    }
    
    div[data-testid="column"]:hover {
        animation-play-state: paused;
        transform: translateY(-5px) scale(1.01) !important;
        box-shadow: 0 15px 40px rgba(139, 92, 246, 0.2);
    }
    
    /* Button Aesthetics */
    .stButton>button {
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
        background-size: 200% auto;
        color: white;
        border-radius: 30px;
        border: none;
        padding: 15px 30px;
        font-size: 18px;
        font-weight: 700;
        transition: 0.5s;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        width: 100%;
    }
    
    .stButton>button:hover {
        background-position: right center;
        transform: scale(1.05);
        box-shadow: 0 10px 25px rgba(168, 85, 247, 0.6);
        color: white;
    }
    
    /* Slider Restyling */
    div[data-baseweb="slider"] {
        padding-top: 10px;
    }
    
    div[data-baseweb="slider"] div[role="slider"] {
        background-color: #fff !important;
        border: 2px solid #a855f7 !important;
        box-shadow: 0 0 15px rgba(168, 85, 247, 0.8) !important;
        transition: transform 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        width: 18px !important;
        height: 18px !important;
    }
    
    div[data-baseweb="slider"] div[role="slider"]:hover, div[data-baseweb="slider"] div[role="slider"]:active {
        transform: scale(1.4) !important;
        box-shadow: 0 0 25px rgba(217, 70, 239, 1) !important;
        border-color: #d946ef !important;
    }
    
    /* Smooth drag transition for the track fill */
    div[data-baseweb="slider"] div {
        transition: width 0.1s ease-out, left 0.1s ease-out, transform 0.1s ease-out !important;
    }
    
    /* Neon Gradient Track Fill */
    /* Target the dynamically filled inline-styled track segment */
    div[data-baseweb="slider"] div[style*="background-color"] {
        background-image: linear-gradient(90deg, #6366f1, #d946ef) !important;
        background-color: transparent !important;
        height: 6px !important;
        border-radius: 3px !important;
        box-shadow: 0 0 10px rgba(168, 85, 247, 0.6) !important;
    }
    
    h1, h2, h3 {
        text-shadow: 0 2px 10px rgba(139, 92, 246, 0.3);
    }
    
    /* Starfield Background Layering */
    div[data-testid="column"], div.stTabs {
        position: relative;
        z-index: 10;
    }
    
    .space-background {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: 0;
        pointer-events: none;
        overflow: hidden;
    }
    
    .stars-layer {
        position: absolute;
        top: -100vh; left: 0; width: 100vw; height: 300vh;
        background-image: 
            radial-gradient(2px 2px at 20px 30px, #eee, rgba(0,0,0,0)),
            radial-gradient(2px 2px at 40px 70px, #fff, rgba(0,0,0,0)),
            radial-gradient(2px 2px at 50px 160px, #ddd, rgba(0,0,0,0)),
            radial-gradient(2px 2px at 90px 40px, #fff, rgba(0,0,0,0)),
            radial-gradient(2px 2px at 130px 80px, #fff, rgba(0,0,0,0)),
            radial-gradient(2px 2px at 160px 120px, #ddd, rgba(0,0,0,0));
        background-repeat: repeat;
        background-size: 200px 200px;
        animation: starDrift 60s linear infinite;
        opacity: 0.6;
    }
    
    .stars-layer-2 {
        background-image: 
            radial-gradient(3px 3px at 50px 50px, #fff, rgba(0,0,0,0)),
            radial-gradient(3px 3px at 150px 100px, #ddd, rgba(0,0,0,0)),
            radial-gradient(2px 2px at 200px 150px, #fff, rgba(0,0,0,0));
        background-size: 350px 350px;
        animation: starDrift 120s linear infinite;
        opacity: 0.3;
    }
    
    @keyframes starDrift {
        from { transform: translateY(0); }
        to { transform: translateY(200px); }
    }
    
    .shooting-star {
        position: absolute;
        width: 2px; height: 80px;
        background: linear-gradient(to top, rgba(255,255,255,0), rgba(0, 242, 254, 1));
        opacity: 0;
        animation: shoot 5s linear infinite;
        transform: rotate(45deg);
    }
    
    @keyframes shoot {
        0% { transform: translate(80vw, -20vh) rotate(45deg); opacity: 1; height: 80px; }
        15% { transform: translate(-20vw, 80vh) rotate(45deg); opacity: 0; height: 0px; }
        100% { opacity: 0; }
    }
    /* Title Animations */
    .levitate-title {
        animation: levitate 4s ease-in-out infinite;
        display: inline-block;
        margin: 0;
        padding-top: 0.5rem;
        font-size: 3rem;
        font-weight: 700;
    }
    
    @keyframes levitate {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    .ghost-emoji {
        display: inline-block;
        animation: ghostPulse 3s ease-in-out infinite;
    }
    
    @keyframes ghostPulse {
        0%, 100% { filter: drop-shadow(0 0 8px rgba(168, 85, 247, 0.3)); transform: scale(1); }
        50% { filter: drop-shadow(0 0 25px rgba(168, 85, 247, 0.9)); transform: scale(1.15) rotate(5deg); }
    }
</style>

<div class="space-background">
    <div class="stars-layer"></div>
    <div class="stars-layer stars-layer-2"></div>
    <div class="shooting-star" style="top: 10%; left: 80%; animation-delay: 2s;"></div>
    <div class="shooting-star" style="top: -10%; left: 50%; animation-delay: 8s;"></div>
</div>
""", unsafe_allow_html=True)

# Logo & Branding
col_logo, col_title = st.columns([1, 8])
with col_logo:
    st.image("ghosted_logo.png", width=80)
with col_title:
    st.markdown("<h1 class='levitate-title'>Ghosted.ai <span class='ghost-emoji'>👻</span></h1>", unsafe_allow_html=True)
    st.subheader("Advanced ML Predictive Engine: Are they drifting away?")

# --- Dummy Data Generation (18 Features) ---
@st.cache_data
def get_advanced_data():
    np.random.seed(42)
    n = 1000
    
    # 1. Timing Signals
    reply_consistency = np.random.randint(1, 10, n)
    late_night_texts = np.random.choice([0, 1], n, p=[0.7, 0.3])
    days_since_deep_convo = np.random.randint(0, 30, n)
    
    # 2. Convo Quality
    msg_len_ratio = np.random.uniform(0.1, 2.5, n) # Theirs vs Yours
    question_rate = np.random.randint(0, 100, n)
    initiation_ratio = np.random.randint(0, 100, n)
    
    # 3. Plans & Follow Through
    cancel_rate = np.random.randint(0, 100, n)
    days_between_meets = np.random.randint(1, 60, n)
    suggests_dates = np.random.randint(0, 100, n)
    
    # 4. Sentiment & Tone
    compliment_freq = np.random.randint(0, 10, n)
    arg_recovery_hrs = np.random.randint(1, 72, n)
    dry_reply_rate = np.random.randint(0, 100, n) # % of 'k', 'lol'
    
    # 5. Social Context
    met_friends = np.random.choice([0, 1], n)
    dtr_score = np.random.randint(0, 4, n) # Defined relationship level
    ex_toxicity = np.random.randint(1, 6, n)
    
    # 6. Trends over time
    vibe_delta = np.random.randint(-5, 6, n) # Week over week
    reply_trend = np.random.choice([-1, 1], n) # -1 = slowing down
    total_days = np.random.randint(14, 365, n)

    # Logic: Weighted scoring to determine if they Ghosted or not
    target = []
    for i in range(n):
        risk_score = 0
        risk_score += days_since_deep_convo[i] * 2
        risk_score += (100 - question_rate[i]) * 0.5
        risk_score += (100 - initiation_ratio[i]) * 0.5
        risk_score += cancel_rate[i] * 1.5
        risk_score += dry_reply_rate[i] * 1.2
        risk_score += (72 - arg_recovery_hrs[i]) * -0.5
        risk_score -= vibe_delta[i] * 10
        if reply_trend[i] == -1: risk_score += 30
        if met_friends[i] == 1: risk_score -= 40
        if msg_len_ratio[i] < 0.5: risk_score += 20
        
        if risk_score > 150:
            target.append("Ghosted 👻")
        else:
            target.append("Safe 💌")
            
    df = pd.DataFrame({
        "Reply Consistency": reply_consistency, "Late Night Texts": late_night_texts, "Days Since Deep Convo": days_since_deep_convo,
        "Message Length Ratio": msg_len_ratio, "Question Rate (%)": question_rate, "Initiation Ratio (%)": initiation_ratio,
        "Cancel Rate (%)": cancel_rate, "Days Between Meets": days_between_meets, "Suggests Dates (%)": suggests_dates,
        "Compliment Freq": compliment_freq, "Arg Recovery (Hrs)": arg_recovery_hrs, "Dry Reply Rate (%)": dry_reply_rate,
        "Met Friends": met_friends, "DTR Score": dtr_score, "Ex Toxicity": ex_toxicity,
        "Vibe Delta": vibe_delta, "Reply Trend": reply_trend, "Total Days Talking": total_days,
        "Status": target
    })
    return df

df = get_advanced_data()

# --- ML Model Training ---
X = df.drop(columns=["Status"])
y = df["Status"]
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X.values, y)

# --- UI Setup ---
col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown("### 🧩 Input Subject Data")
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "⏱️ Timing", "💬 Convo", "📅 Plans", "🎭 Sentiment", "👥 Social", "📈 Trends"
    ])
    
    with tab1:
        i_reply_consist = st.slider("Consistency of reply time (1-10)", 1, 10, 5)
        i_late_night = st.radio("Time of day they text", ["Normal Hours", "3 AM Texts"], horizontal=True)
        i_late_night_val = 1 if i_late_night == "3 AM Texts" else 0
        i_days_deep = st.slider("Days since last meaningful convo", 0, 30, 2)
        
    with tab2:
        i_msg_len = st.slider("Message length ratio (Theirs / Yours)", 0.1, 3.0, 1.0)
        i_question = st.slider("Question-asking rate (%)", 0, 100, 50)
        i_init = st.slider("Convo initiation ratio (Who starts? % Them)", 0, 100, 50)
        
    with tab3:
        i_cancel = st.slider("Plans cancelled rate (%)", 0, 100, 10)
        i_days_meet = st.slider("Days between asking to meet", 1, 60, 7)
        i_suggest = st.slider("Who suggests dates? (% Them)", 0, 100, 50)
        
    with tab4:
        i_comp = st.slider("Compliment frequency (0-10)", 0, 10, 5)
        i_arg = st.slider("Argument recovery time (Hours)", 1, 72, 5)
        i_dry = st.slider("Dry/low-effort reply rate (%)", 0, 100, 20)
        
    with tab5:
        i_friends = st.radio("Met their friends yet?", ["No", "Yes"], horizontal=True)
        i_friends_val = 1 if i_friends == "Yes" else 0
        i_dtr = st.slider("Defined the relationship? (0=No, 3=Official)", 0, 3, 1)
        i_ex = st.slider("How they talk about ex (1=Bitter, 5=Healthy)", 1, 5, 3)
        
    with tab6:
        i_vibe_delta = st.slider("Vibe score delta (week over week)", -5, 5, 0)
        i_reply_trend = st.radio("Reply time trend", ["Speeding up", "Slowing down"], horizontal=True)
        i_reply_trend_val = -1 if i_reply_trend == "Slowing down" else 1
        i_total_days = st.number_input("Total days talking", 7, 365, 30)
        
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔮 PREDICT FUTURE"):
        user_input = [[
            i_reply_consist, i_late_night_val, i_days_deep, i_msg_len, i_question, i_init,
            i_cancel, i_days_meet, i_suggest, i_comp, i_arg, i_dry, i_friends_val, i_dtr, i_ex,
            i_vibe_delta, i_reply_trend_val, i_total_days
        ]]
        
        prob = clf.predict_proba(user_input)[0]
        ghost_prob = prob[0] if clf.classes_[0] == "Ghosted 👻" else prob[1]
        
        st.markdown("---")
        st.markdown("## 🧠 AI Verdict")
        if ghost_prob > 0.6:
            st.error(f"**High Risk ({ghost_prob*100:.1f}%)**: They are drifting. Ghosting protocol detected. 👻")
            color_theme = "ghosted"
        elif ghost_prob > 0.3:
            st.warning(f"**Moderate Risk ({ghost_prob*100:.1f}%)**: Mixed signals. Proceed with caution. ⚠️")
            color_theme = "mixed"
        else:
            st.success(f"**Safe ({100 - ghost_prob*100:.1f}%)**: Strong signals! Lock it in. 💌")
            color_theme = "safe"
            
        # Physics Particle Explosion
        js_code = f"""
        <script>
        (function() {{
            const theme = '{color_theme}';
            const parent = window.parent.document;
            const buttons = Array.from(parent.querySelectorAll('button'));
            const btn = buttons.find(b => b.innerText.includes('PREDICT FUTURE'));
            const rect = btn ? btn.getBoundingClientRect() : {{left: window.innerWidth/2, top: window.innerHeight/2, width: 0, height: 0}};
            
            const centerX = rect.left + rect.width / 2;
            const centerY = rect.top + rect.height / 2;
            
            // Create Shockwave
            const shockwave = parent.createElement('div');
            shockwave.style.position = 'fixed';
            shockwave.style.left = centerX + 'px';
            shockwave.style.top = centerY + 'px';
            shockwave.style.width = '10px';
            shockwave.style.height = '10px';
            shockwave.style.borderRadius = '50%';
            
            let colorBorder = theme === 'ghosted' ? '#ff416c' : (theme === 'safe' ? '#00f2fe' : '#f6d365');
            shockwave.style.border = '6px solid ' + colorBorder;
            shockwave.style.transform = 'translate(-50%, -50%)';
            shockwave.style.zIndex = '99999';
            shockwave.style.pointerEvents = 'none';
            shockwave.style.transition = 'all 0.8s cubic-bezier(0.1, 0.8, 0.2, 1)';
            shockwave.style.opacity = '1';
            parent.body.appendChild(shockwave);
            
            requestAnimationFrame(() => {{
                shockwave.style.width = '800px';
                shockwave.style.height = '800px';
                shockwave.style.opacity = '0';
            }});
            setTimeout(() => shockwave.remove(), 800);
            
            // Create Particles
            const particleCount = Math.floor(Math.random() * 40) + 80; // 80-120
            
            const getColors = () => {{
                if (theme === 'ghosted') return ['#ff0844', '#ffb199', '#ff416c', '#ff4b1f'];
                if (theme === 'safe') return ['#00ff00', '#00f2fe', '#4facfe', '#43e97b'];
                return ['#f6d365', '#fda085', '#ffecd2', '#fcb69f']; // Mixed
            }};
            const colors = getColors();
            
            for (let i = 0; i < particleCount; i++) {{
                const p = parent.createElement('div');
                const color = colors[Math.floor(Math.random() * colors.length)];
                p.style.position = 'fixed';
                p.style.left = centerX + 'px';
                p.style.top = centerY + 'px';
                p.style.width = Math.random() * 8 + 4 + 'px';
                p.style.height = p.style.width;
                p.style.backgroundColor = color;
                p.style.borderRadius = '50%';
                p.style.zIndex = '99999';
                p.style.pointerEvents = 'none';
                p.style.boxShadow = '0 0 10px ' + color;
                parent.body.appendChild(p);
                
                // Physics
                const angle = Math.random() * Math.PI * 2;
                const velocity = Math.random() * 25 + 5;
                let vx = Math.cos(angle) * velocity;
                let vy = Math.sin(angle) * velocity - 15; // Upward burst bias
                let x = centerX;
                let y = centerY;
                let life = 1.0;
                let gravity = 0.8;
                
                function animateP() {{
                    x += vx;
                    y += vy;
                    vy += gravity; // Gravity pull
                    vx *= 0.98; // Air Friction
                    life -= 0.015;
                    p.style.left = x + 'px';
                    p.style.top = y + 'px';
                    p.style.opacity = life;
                    
                    if (life > 0) {{
                        requestAnimationFrame(animateP);
                    }} else {{
                        p.remove();
                    }}
                }}
                requestAnimationFrame(animateP);
            }}
        }})();
        </script>
        """
        import streamlit.components.v1 as components
        components.html(js_code, height=0, width=0)

with col2:
    st.markdown("### 📊 Feature Importance Engine")
    st.write("What our Random Forest values most in this prediction:")
    
    # Calculate feature importances
    importances = clf.feature_importances_
    feat_df = pd.DataFrame({"Feature": X.columns, "Importance": importances})
    feat_df = feat_df.sort_values(by="Importance", ascending=True).tail(10) # Top 10
    
    fig = px.bar(feat_df, x="Importance", y="Feature", orientation='h',
                 color="Importance", color_continuous_scale="Purp")
                 
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=30, b=0),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )
    st.plotly_chart(fig, use_container_width=True)

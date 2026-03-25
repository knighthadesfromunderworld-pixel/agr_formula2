import streamlit as st
import matplotlib.pyplot as plt
from gtts import gTTS
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Agro Twin Economics", page_icon="💰", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .card { background-color: #ffffff; padding: 20px; border-radius: 15px; border-left: 6px solid #2e7d32; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .money-text { color: #2e7d32; font-weight: bold; font-size: 1.2em; }
    .time-text { color: #1976d2; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- ADVANCED PSEUDO-FORMULA ENGINE ---
def calculate_agro_logic(n, p, k, moisture, ph, soil_type):
    # Profiles: [N, P, K, Moisture, pH, Soil_Type_Match, Base_Price, Growth_Months]
    # Soil Types: 0:Sandy, 1:Loamy, 2:Clay, 3:Black
    crop_db = {
        "Teak": {"vals": [40, 20, 30, 35, 7.0, 1], "ta": "தேக்கு", "price": 500000, "time": "240 Months"},
        "Turmeric": {"vals": [70, 45, 50, 75, 6.5, 2], "ta": "மஞ்சள்", "price": 120000, "time": "9 Months"},
        "Banana": {"vals": [55, 35, 85, 80, 6.5, 1], "ta": "வாழை", "price": 80000, "time": "12 Months"},
        "Pepper": {"vals": [50, 40, 40, 85, 6.0, 3], "ta": "மிளகு", "price": 150000, "time": "36 Months"},
        "Cashew": {"vals": [30, 20, 20, 25, 5.5, 0], "ta": "முந்திரி", "price": 200000, "time": "60 Months"}
    }
    
    results = {}
    for crop, data in crop_db.items():
        ideals = data["vals"]
        
        # 1. Nutrient Suitability Score
        n_penalty = abs(ideals[0] - n) * 1.2
        p_penalty = abs(ideals[1] - p) * 1.2
        k_penalty = abs(ideals[2] - k) * 1.2
        ph_penalty = abs(ideals[4] - ph) * 20.0
        
        suitability = 100 - (n_penalty + p_penalty + k_penalty + ph_penalty)
        if soil_type != ideals[5]: suitability -= 20 # Soil mismatch penalty
        
        final_score = max(5, min(100, suitability))
        
        # 2. Economic Projection Formula
        # Revenue = Base Price * (Suitability / 100) -> Higher suitability = Better yield
        projected_revenue = data["price"] * (final_score / 100)
        
        results[crop] = {
            "score": round(final_score, 1),
            "ta": data["ta"],
            "revenue": int(projected_revenue),
            "time": data["time"]
        }
    return results

# --- SIDEBAR: ROVER CONTROLS ---
st.sidebar.title("🎮 Rover Telemetry")
with st.sidebar:
    n = st.slider("Nitrogen (N)", 0, 100, 45)
    p = st.slider("Phosphorus (P)", 0, 100, 30)
    k = st.sidebar.slider("Potassium (K)", 0, 100, 50)
    ph = st.slider("pH Level", 4.0, 9.0, 6.5)
    moisture = st.slider("Moisture %", 0, 100, 40)
    soil_map = {"Sandy": 0, "Loamy": 1, "Clay": 2, "Black": 3}
    soil_select = st.selectbox("Soil Type", list(soil_map.keys()))

# --- MAIN DASHBOARD ---
st.title("🛰️ Agro Twin: Economic & Biological Intelligence")
st.write(f"Digital Twin Status: **Connected** | Target: **Optimal Yield Projection**")

analysis = calculate_agro_logic(n, p, k, moisture, ph, soil_map[soil_select])

# TOP METRICS
m1, m2, m3 = st.columns(3)
top_crop = max(analysis, key=lambda x: analysis[x]['score'])
m1.metric("Prime Recommendation", top_crop)
m2.metric("Max Suitability", f"{analysis[top_crop]['score']}%")
m3.metric("Est. Revenue (per acre)", f"₹{analysis[top_crop]['revenue']:,}")

st.divider()

col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("📊 Crop Suitability Index")
    fig, ax = plt.subplots(figsize=(6, 5))
    crops = list(analysis.keys())
    scores = [v["score"] for v in analysis.values()]
    colors = ['#2e7d32' if s > 70 else '#fbc02d' if s > 40 else '#d32f2f' for s in scores]
    ax.barh(crops, scores, color=colors)
    ax.set_xlim(0, 100)
    st.pyplot(fig)

with col_right:
    st.subheader("💡 Business Insights & Growth Time")
    
    for crop, info in analysis.items():
        st.markdown(f"""
        <div class="card">
            <b style='font-size:1.2em;'>{crop} ({info['ta']})</b><br>
            Suitability: <b>{info['score']}%</b><br>
            Projected Revenue: <span class="money-text">₹{info['revenue']:,}</span><br>
            Time to Harvest: <span class="time-text">⏱ {info['time']}</span>
        </div>
        """, unsafe_allow_html=True)

# VOICE ADVISORY
if st.button("🔊 Generate Financial Voice Advisory"):
    voice_text = f"சிறந்த தேர்வு: {top_crop}. இதன் மூலம் எதிர்பார்க்கப்படும் வருமானம் {analysis[top_crop]['revenue']} ரூபாய். அறுவடை காலம் {analysis[top_crop]['time']}."
    tts = gTTS(text=voice_text, lang='ta')
    tts.save("econ_voice.mp3")
    st.audio("econ_voice.mp3")

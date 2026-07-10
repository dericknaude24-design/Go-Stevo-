import streamlit as st
import os

# ==========================================
# 1. THE CORE MASTER PROMPTS (THE BRAIN)
# ==========================================

MASTER_SYSTEM_DIRECTIVE = """
You are the "Main Brain" core engine for the Downtown Stevo Town Home Recovery System. 
Your objective is to act as an empathetic, grounded, and clinical-grade rehabilitation collaborator. 
You guide the user through their daily recovery while monitoring for psychological distress.
CRITICAL: You must always prioritize physical safety and adhere strictly to the daily phase instructions.
"""

DAY_PROMPTS = {
    "Days 1-7": "Phase: Acute Detox Phase. Focus strictly on physical stability, hydration, rest, and managing immediate withdrawal cravings. Keep dialogues short and highly supportive.",
    "Days 8-24": "Phase: Stabilization & Pattern Dissection. Begin gently exploring underlying behavioral triggers, routines, and constructing long-term coping mechanisms."
}

CLINICAL_NOTE_SYNTHESIZER = """
You are an automated clinical data compiler. Review the following day's conversation and synthesize it into a structured medical note.
Format as:
- Quantitative Metrics Summary
- Qualitative Behavioral Patterns
- Risk Assessment Status
- Caregiver Action Items
"""

# ==========================================
# 2. STREAMLIT APP CONFIGURATION & UI
# ==========================================

st.set_page_config(page_title="Stevo Rehab App", page_icon="🏥", layout="centered")

st.title("🏥 Downtown Stevo Town")
st.subtitle("Home Recovery System Dashboard")

# Initialize session states for storing text history securely
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "session_blocked" not in st.session_state:
    st.session_state.session_blocked = False

# Phase Selection based on Day Profile
phase = st.selectbox("Select Current Recovery Phase:", ["Days 1-7", "Days 8-24"])

st.markdown("---")
st.subheader("📋 Step 1: Morning Intake & Safety Matrix")

# Ingestion Matrix Inputs
heart_rate = st.number_input("Heart Rate (BPM):", min_value=0, max_value=200, value=75)
distress_level = st.slider("Psychological Distress Level (1-10):", 1, 10, 5)
thoughts_of_self_harm = st.radio("Are you experiencing any thoughts of self-harm today?", ["No", "Yes"])

st.markdown("---")

# ==========================================
# 3. THE NON-NEGOTIABLE SAFETY GATE
# ==========================================
if st.button("Submit Metrics & Unlock Session"):
    if thoughts_of_self_harm == "Yes" or heart_rate > 130 or heart_rate < 50 or distress_level >= 9:
        st.session_state.session_blocked = True
        st.error("🚨 EMERGENCY OVERRIDE TRIGGERED 🚨")
    else:
        st.session_state.session_blocked = False
        st.success("✅ Safety Gate Passed. Session unlocked.")

# ==========================================
# 4. CHAT INTERFACE & APP PROCESSING
# ==========================================
if st.session_state.session_blocked:
    st.markdown("<h2 style='color:red;'>⚠️ SESSION BLOCKED</h2>", unsafe_style=True)
    st.error("Critical red lines crossed. Please contact emergency medical services or your primary caregiver immediately.")
else:
    st.subheader("💬 Therapeutic Dialogue Session")
    
    # Mocking the interaction layout visually for the user
    user_input = st.text_input("Speak with the Main Brain:")
    
    if st.button("Send message"):
        if user_input:
            st.session_state.chat_history.append(f"User: {user_input}")
            # Dynamic prompt building simulation
            system_payload = f"{MASTER_SYSTEM_DIRECTIVE}\n\n{DAY_PROMPTS[phase]}"
            st.session_state.chat_history.append(f"Main Brain Engine: [Acknowledged Phase: {phase}]. Stay strong. We are tracking your physical metrics closely.")
            
    # Display Chat
    for message in st.session_state.chat_history:
        st.write(message)

    # ==========================================
    # 5. AUTOMATED CLINICAL SUMMARY
    # ==========================================
    st.markdown("---")
    if st.button("🔒 Close Day & Generate Clinical Log"):
        st.info("Compiling daily records history...")
        st.text_area("Generated Summary (For Caregiver Review):", 
                     value=f"{CLINICAL_NOTE_SYNTHESIZER}\n\n--- AUTO LOG ---\nMetrics: HR={heart_rate}, Distress={distress_level}\nPhase Context: {DAY_PROMPTS[phase]}", 
                     height=150)

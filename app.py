import streamlit as st
import time

# --- STATE CONTROLS ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_mode" not in st.session_state:
    st.session_state.user_mode = None
if "username" not in st.session_state:
    st.session_state.username = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "assistant", "content": "Greetings. I am your localized AI Nutrition Assistant."}]
if "health_data" not in st.session_state:
    st.session_state.health_data = {"systolic": 120, "diastolic": 80, "blood_sugar": 5.4, "water_ml": 1500, "sleep_hours": 7.0, "steps": 6000, "temperature": 36.6}

# --- UNLOGGED LANDING GATEWAY ---
if not st.session_state.authenticated and st.session_state.user_mode is None:
    st.title("🤖 Project jetsMMC")
    st.subheader("AI for Health and Nutrition Detection Platform")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🔐 Registered Access Portal")
        with st.form("secure_gateway"):
            u_in = st.text_input("Username / Email Registration ID", value="student@jets.org")
            p_in = st.text_input("Secure Passkey", type="password", value="password123")
            role_sel = st.selectbox("Assign System Interface Mode", ["Personal Mode", "Professional (Clinic) Mode"])
            if st.form_submit_button("Authenticate Secure Session Layer"):
                if u_in and p_in:
                    st.session_state.authenticated = True
                    st.session_state.username = u_in
                    st.session_state.user_mode = "Personal" if role_sel == "Personal Mode" else "Professional"
                    st.rerun()
    with col2:
        st.markdown("### 🌐 Public Access")
        st.write("Temporary sandbox layer.")
        if st.button("Continue Session as Guest ➔", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.username = "Anonymous Guest"
            st.session_state.user_mode = "Guest"
            st.rerun()

# --- LOGGED ROUTING PORTAL ---
else:
    with st.sidebar:
        st.markdown(f"### 👤 Active User: `{st.session_state.username}`")
        st.info(f"Configuration: **{st.session_state.user_mode}**")
        if st.button("Log Out / Close Session", type="primary", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_mode = None
            st.rerun()

    # --- MODE: PERSONAL ARCHITECTURE ---
    if st.session_state.user_mode == "Personal":
        t_home, t_track, t_health, t_chat = st.tabs(["🏠 Home Layout", "📊 Track Metrics", "🍎 Health & Nutrition", "💬 AI Chat Hub"])
        
        with t_home:
            st.title("Welcome to Your Health Center")
            sys_v = abs(st.session_state.health_data["systolic"] - 120)
            sugar_v = abs(st.session_state.health_data["blood_sugar"] - 5.5) * 12
            w_r = min(100.0, (st.session_state.health_data["water_ml"] / 2500.0) * 100.0)
            sl_r = min(100.0, (st.session_state.health_data["sleep_hours"] / 8.0) * 100.0)
            st_r = min(100.0, (st.session_state.health_data["steps"] / 10000.0) * 100.0)
            raw = int(100 - (sys_v + sugar_v) + ((w_r + sl_r + st_r) / 3)) // 1.5
            score = max(0, min(100, int(raw)))
            
            st.metric(label="Calculated Dashboard NutriScore", value=f"{score} / 100")
            if score >= 80: st.success("🟢 Homeostatic State Optimal: Core biometrics within expected limits.")
            else: st.warning("🟡 Systemic Equilibrium Warning: Sub-optimal behavioral variables checked.")
            
            st.markdown("---")
            st.subheader("🚨 Automated Health Risk Stratification Alerts")
            if st.session_state.health_data["systolic"] > 130: st.error("⚠️ Cardiovascular Parameter Alert: Pre-Hypertensive indicators active.")
            if st.session_state.health_data["water_ml"] < 2000: st.error("⚠️ Metabolic Dehydration Hazard: Fluid intake below baseline benchmarks.")
            
        with t_track:
            st.title("Telemetry Processing Intake Panel")
            with st.form("intake_form"):
                nsys = st.number_input("Systolic Blood Pressure (mmHg)", value=st.session_state.health_data["systolic"])
                nsug = st.number_input("Fasting Plasma Glucose (mmol/L)", value=st.session_state.health_data["blood_sugar"])
                nwat = st.slider("Fluid Volumetric Ingestion (mL)", 0, 5000, int(st.session_state.health_data["water_ml"]))
                nsle = st.slider("Sleep Cycle Intercept Metric (Hours)", 0.0, 16.0, float(st.session_state.health_data["sleep_hours"]))
                nstp = st.number_input("Actigraphy Quantified Daily Footsteps", value=st.session_state.health_data["steps"])
                if st.form_submit_button("Commit Metrics Frame to System Memory", type="primary"):
                    st.session_state.health_data.update({"systolic": nsys, "blood_sugar": nsug, "water_ml": nwat, "sleep_hours": nsle, "steps": nstp})
                    st.success("Data Frame Synced!")
                    time.sleep(0.4)
                    st.rerun()
                    
        with t_health:
            st.title("Computer Vision Dietary Extraction Node")
            img = st.file_uploader("Upload meal image profile for analysis...", type=["png", "jpg", "jpeg"])
            if img is not None:
                st.image(img, width=350)
                c1, c2 = st.columns(2)
                c1.metric("Identified Food Group", "Poached Egg & Wheat Toast")
                c2.metric("Inferred Caloric Output", "310 kcal")
            st.markdown("---")
            st.subheader("📍 Geolocation Medical Routing Protocols")
            if st.checkbox("Grant Application Permission to Read Location Data via API"):
                st.success("Routing Sync Complete. Closest Option: 🏥 Central Core Medical Outpost (1.1 km away)")
                
        with t_chat:
            st.title("AI Assistant Processing Terminal")
            for m in st.session_state.chat_history: st.chat_message(m["role"]).markdown(m["content"])
            if pr := st.chat_input("Query the AI Assistant regarding logged vital variances..."):
                st.chat_message("user").markdown(pr)
                st.session_state.chat_history.append({"role": "user", "content": pr})
                with st.chat_message("assistant"):
                    res = f"Query parsed. Active system registry maintains a calculated baseline score of {score}/100."
                    if "pressure" in pr.lower(): res = f"Active resting blood pressure logs read {st.session_state.health_data['systolic']} mmHg. Reduce high-sodium inputs."
                    st.markdown(res)
                    st.session_state.chat_history.append({"role": "assistant", "content": res})

    # --- MODE: GUEST ARCHITECTURE ---
    elif st.session_state.user_mode == "Guest":
        st.title("🌐 Public Frameworks Interface (Guest Sandbox)")
        st.info("Public access repository promoting community health and nutrition literacy under SDG Goal 3 guidelines.")

    # --- MODE: CLINIC ARCHITECTURE ---
    elif st.session_state.user_mode == "Professional":
        st.title("🏥 Clinical Management Interface Console")
        p_sel = st.selectbox("Select Target Patient Telemetry Feed", ["Patient Record #0042", "Patient Record #0912"])
        pc1, pc2 = st.columns(2)
        pc1.metric("Arterial Pressure Matrix", "145 / 95 mmHg" if "#0042" in p_sel else "120 / 78 mmHg")
        pc2.metric("Mean Fasting Glucose", "7.2 mmol/L" if "#0042" in p_sel else "4.9 mmol/L")

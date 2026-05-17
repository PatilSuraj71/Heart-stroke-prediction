

import streamlit as st
import pandas as pd
import joblib
import time



st.set_page_config(
    page_title="Advanced Heart Disease Prediction",
    page_icon="❤️",
    layout="wide"
)



model = joblib.load("knn_heart.pkl")
scaler = joblib.load("scaler.pkl")
expected_columns = joblib.load("columns.pkl")



st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* Background */

.stApp {
    background: linear-gradient(-45deg, #0f172a, #111827, #1e293b, #0f2027);
    background-size: 400% 400%;
    animation: gradientBG 12s ease infinite;
    color: white;
}

@keyframes gradientBG {

    0% {
        background-position: 0% 50%;
    }

    50% {
        background-position: 100% 50%;
    }

    100% {
        background-position: 0% 50%;
    }
}

/* Hide Streamlit */

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* Title */

.main-title {
    text-align:center;
    font-size:60px;
    font-weight:800;
    color:white;
    animation:pulse 2s infinite;
}

.subtitle {
    text-align:center;
    font-size:20px;
    color:#cbd5e1;
    margin-bottom:35px;
}

@keyframes pulse {

    0% {transform:scale(1);}
    50% {transform:scale(1.03);}
    100% {transform:scale(1);}
}

/* Glass Effect */

.glass {
    background:rgba(255,255,255,0.08);
    border-radius:30px;
    padding:35px;
    backdrop-filter:blur(18px);
    border:1px solid rgba(255,255,255,0.12);
    box-shadow:0px 10px 40px rgba(0,0,0,0.4);
}

/* Button */

.stButton > button {

    width:100%;
    background:linear-gradient(90deg,#ff416c,#ff4b2b);
    color:white;
    font-size:22px;
    font-weight:bold;
    border:none;
    border-radius:18px;
    padding:16px;
    transition:0.4s;
}

.stButton > button:hover {

    transform:scale(1.03);
    box-shadow:0px 0px 25px rgba(255,75,75,0.7);
}

/* Cards */

.card {

    background:rgba(255,255,255,0.07);
    border-radius:22px;
    padding:25px;
    margin-top:20px;
    border:1px solid rgba(255,255,255,0.12);
    animation:slideUp 1s ease;
}

/* Doctor Card */

.doctor-card {

    background:rgba(255,255,255,0.09);
    border-radius:24px;
    padding:25px;
    margin-top:20px;
    border-left:5px solid #ff4b6e;
    animation:floating 3s ease-in-out infinite;
}

/* Result */

.result-box {

    padding:30px;
    border-radius:25px;
    text-align:center;
    font-size:32px;
    font-weight:bold;
    margin-top:25px;
    animation:slideUp 1s ease;
}

/* Animations */

@keyframes slideUp {

    from {
        opacity:0;
        transform:translateY(40px);
    }

    to {
        opacity:1;
        transform:translateY(0px);
    }
}

@keyframes floating {

    0% {transform:translateY(0px);}
    50% {transform:translateY(-8px);}
    100% {transform:translateY(0px);}
}

</style>
""", unsafe_allow_html=True)

# ================= HEADER ================= #

st.markdown("""
<div class="main-title">
❤️ Heart Disease Prediction
</div>

<div class="subtitle">
AI Powered Cardiac Health Intelligence System
</div>
""", unsafe_allow_html=True)

# ================= MAIN CONTAINER ================= #

with st.container():

    st.markdown('<div class="glass">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # ================= LEFT ================= #

    with col1:

        st.subheader("👤 Personal Information")

        age = st.slider("Age", 1, 100, 40)

        sex = st.selectbox(
            "Sex",
            ["M", "F"]
        )

        chest_pain = st.selectbox(
            "Chest Pain Type",
            ["ATA", "NAP", "TA", "ASY"]
        )

        fasting_bs = st.selectbox(
            "Diabetes / Sugar Level",
            [0, 1]
        )

        exercise_angina = st.selectbox(
            "Exercise-Induced Angina",
            ["Y", "N"]
        )

    # ================= RIGHT ================= #

    with col2:

        st.subheader("🩺 Medical Information")

        resting_bp = st.number_input(
            "Blood Pressure",
            80, 250, 120
        )

        cholesterol = st.number_input(
            "Cholesterol Level",
            100, 700, 200
        )

        resting_ecg = st.selectbox(
            "Resting ECG",
            ["Normal", "ST", "LVH"]
        )

        max_hr = st.slider(
            "Maximum Heart Rate",
            60, 220, 150
        )

        oldpeak = st.slider(
            "ST Depression",
            0.0, 6.0, 1.0
        )

        st_slope = st.selectbox(
            "ST Slope",
            ["Up", "Flat", "Down"]
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ================= PREDICT BUTTON ================= #

    if st.button("🔍 Predict Heart Disease"):

        progress = st.progress(0)

        for i in range(100):
            time.sleep(0.01)
            progress.progress(i + 1)

        # ================= INPUT ================= #

        raw_input = {

            'Age': age,
            'RestingBP': resting_bp,
            'Cholesterol': cholesterol,
            'FastingBS': fasting_bs,
            'MaxHR': max_hr,
            'Oldpeak': oldpeak,
            'Sex_' + sex: 1,
            'ChestPainType_' + chest_pain: 1,
            'RestingECG_' + resting_ecg: 1,
            'ExerciseAngina_' + exercise_angina: 1,
            'ST_Slope_' + st_slope: 1
        }

        input_df = pd.DataFrame([raw_input])

        for col in expected_columns:

            if col not in input_df.columns:
                input_df[col] = 0

        input_df = input_df[expected_columns]

        scaled_input = scaler.transform(input_df)

        prediction = model.predict(scaled_input)[0]

        # ================= HEART CAUSES ================= #

        heart_causes = []

        if cholesterol > 300:
            heart_causes.append("Coronary Artery Blockage")

        if resting_bp > 180:
            heart_causes.append("Severe Hypertension")

        if fasting_bs == 1:
            heart_causes.append("Diabetic Heart Risk")

        if chest_pain == "ASY":
            heart_causes.append("Silent Heart Disease")

        if chest_pain == "TA":
            heart_causes.append("Typical Angina")

        if chest_pain == "ATA":
            heart_causes.append("Atypical Angina")

        if oldpeak > 3:
            heart_causes.append("Heart Muscle Stress")

        if max_hr < 100:
            heart_causes.append("Low Cardiac Performance")

        if resting_ecg == "LVH":
            heart_causes.append("Left Ventricular Hypertrophy")

        if resting_ecg == "ST":
            heart_causes.append("Abnormal ECG Changes")

        # ================= DISEASE TYPE ================= #

        disease_type = "General Heart Risk"

        if cholesterol > 320 and resting_bp > 170:
            disease_type = "Heart Attack Risk"

        elif fasting_bs == 1 and cholesterol > 250:
            disease_type = "Diabetic Heart Disease"

        elif resting_bp > 180:
            disease_type = "Hypertensive Heart Disease"

        elif chest_pain == "ASY":
            disease_type = "Coronary Artery Disease"

        elif oldpeak > 3:
            disease_type = "Cardiac Stress Disorder"

        # ================= HIGH RISK ================= #

        if prediction == 1:

            st.markdown(f"""
            <div class="result-box"
            style="
            background:rgba(255,0,0,0.15);
            border:1px solid rgba(255,0,0,0.3);
            color:#ff6b6b;">

            ⚠️ HIGH HEART RISK DETECTED

            <br><br>

            ❤️ Possible Disease:
            <br>
            {disease_type}

            </div>
            """, unsafe_allow_html=True)

            # ================= HEART CAUSES ================= #

            st.markdown("""
            <div class="card">

            <h2>🩺 Detected Heart Causes</h2>

            """, unsafe_allow_html=True)

            for cause in heart_causes:
                st.write(f"⚠️ {cause}")

            st.markdown("</div>", unsafe_allow_html=True)

            # ================= SMART RECOMMENDATIONS ================= #

            st.markdown("""
            <div class="card">

            <h2>💡 Personalized Health Recommendations</h2>

            """, unsafe_allow_html=True)

            if cholesterol > 240:

                st.write("🥗 Reduce oily foods and fast food")
                st.write("🥬 Increase green vegetables and fiber")
                st.write("🚫 Avoid butter, cheese and fried items")

            if resting_bp > 140:

                st.write("🧂 Reduce salt intake")
                st.write("🧘 Practice meditation daily")
                st.write("😴 Sleep at least 7-8 hours")

            if fasting_bs == 1:

                st.write("🍬 Avoid sugar and soft drinks")
                st.write("🚶 Walk 30 minutes daily")
                st.write("🥣 Eat diabetic-friendly meals")

            if max_hr < 100:

                st.write("🏃 Improve heart fitness with cardio")
                st.write("🚴 Cycling and walking recommended")

            if oldpeak > 2:

                st.write("📋 ECG monitoring recommended")
                st.write("🏥 Consult cardiologist immediately")

            if chest_pain == "ASY":

                st.write("⚠️ Silent heart symptoms detected")
                st.write("🩺 Full body heart checkup advised")

            st.write("🚭 Avoid smoking and alcohol")
            st.write("💧 Drink 3-4 liters water daily")

            st.markdown("</div>", unsafe_allow_html=True)

            # ================= DOCTORS ================= #

            st.markdown("""
            <h1 style='text-align:center; margin-top:40px;'>
            👨‍⚕️ Recommended Heart Specialists
            </h1>
            """, unsafe_allow_html=True)

            if age <= 20:

                doctors = [

                    {
                        "name": "Dr. Krishna Kumar",
                        "hospital": "Apollo Hospitals",
                        "city": "Chennai",
                        "specialist": "Young Heart Specialist"
                    },

                    {
                        "name": "Dr. Gurunath Parale",
                        "hospital": "Parale Heart Hospital",
                        "city": "Solapur",
                        "specialist": "Pediatric Cardiology"
                    }

                ]

            elif age <= 35:

                doctors = [

                    {
                        "name": "Dr. Devi Shetty",
                        "hospital": "Narayana Health",
                        "city": "Bangalore",
                        "specialist": "Cardiac Surgery"
                    },

                    {
                        "name": "Dr. Rahul Sawant",
                        "hospital": "Hridaymitra Cardia Clinic",
                        "city": "Pune",
                        "specialist": "Heart Specialist"
                    }

                ]

            elif age <= 50:

                doctors = [

                    {
                        "name": "Dr. Ashok Seth",
                        "hospital": "Fortis Escorts Heart Institute",
                        "city": "Delhi",
                        "specialist": "Interventional Cardiology"
                    },

                    {
                        "name": "Dr. Chinmay Parale",
                        "hospital": "Spandan Cardiac Centre",
                        "city": "Solapur",
                        "specialist": "Heart Disease Expert"
                    }

                ]

            elif age <= 65:

                doctors = [

                    {
                        "name": "Dr. Naresh Trehan",
                        "hospital": "Medanta Hospital",
                        "city": "Gurgaon",
                        "specialist": "Senior Heart Specialist"
                    },

                    {
                        "name": "Dr. Rahul Patil",
                        "hospital": "Heart Clinic",
                        "city": "Pune",
                        "specialist": "Cardiology Expert"
                    }

                ]

            else:

                doctors = [

                    {
                        "name": "Dr. Ramakanta Panda",
                        "hospital": "Asian Heart Institute",
                        "city": "Mumbai",
                        "specialist": "Advanced Heart Surgery"
                    },

                    {
                        "name": "Dr. Suhas Hardas",
                        "hospital": "Hardas Heart Care",
                        "city": "Pune",
                        "specialist": "Senior Cardiology"
                    }

                ]

            # ================= SHOW DOCTORS ================= #

            for doc in doctors:

                st.markdown(f"""
                <div class="doctor-card">

                <h2 style="color:#ff4b6e;">
                👨‍⚕️ {doc['name']}
                </h2>

                <h4>
                🏥 {doc['hospital']}
                </h4>

                <p style="font-size:18px;">
                📍 {doc['city']}
                </p>

                <p style="color:#4ade80;">
                ⭐ Specialist: {doc['specialist']}
                </p>

                </div>
                """, unsafe_allow_html=True)

            # ================= AI REPORT ================= #

            st.markdown("""
            <div class="card">

            <h2 style="text-align:center;">
            ❤️ AI Heart Analysis Completed
            </h2>

            <p style="text-align:center; font-size:18px;">
            Advanced Machine Learning algorithms analyzed
            your heart health parameters successfully.
            </p>

            </div>
            """, unsafe_allow_html=True)

        # ================= LOW RISK ================= #

        else:

            st.markdown("""
            <div class="result-box"
            style="
            background:rgba(0,255,100,0.12);
            border:1px solid rgba(0,255,100,0.3);
            color:#4ade80;">

            ✅ LOW RISK OF HEART DISEASE

            <br><br>

            ❤️ Your Heart Looks Healthy

            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ================= FOOTER ================= #

st.markdown("""
<br><br>

<center>
<p style="color:gray; font-size:18px;">
Made by BME Aspirants❤️ 
</p>
</center>
""", unsafe_allow_html=True)
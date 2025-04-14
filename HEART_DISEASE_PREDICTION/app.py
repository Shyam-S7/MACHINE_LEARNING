import streamlit as st
import pickle
import numpy as np
import base64

# Load the trained model
model = pickle.load(open('model.pkl', 'rb'))

st.set_page_config(page_title="Heart Disease Predictor", layout="centered")

st.title("Heart Disease Prediction App")
st.write("Enter your details below to predict your heart disease risk.")

def set_background(image_file):
    with open(image_file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Set your background image
set_background("heart.webp")  # Change this to your image file name

# About section
with st.expander("About this App"):
    st.markdown("""
        This is a Machine Learning-based web application that predicts the risk of heart disease.
        
        **Developer**: **Shyam S**

        *Instructions:*
        - Enter valid health details.
        - Click *Predict* to see the result.
        - Use *Download* button to save the result.
    """)
# Input features
age = st.number_input("Age", min_value=1, max_value=120, value=45)
sex = st.selectbox("Sex", options=[0, 1], format_func=lambda x: "Female" if x == 0 else "Male")
cp = st.selectbox("Chest Pain Type", options=[0, 1, 2, 3], format_func=lambda x: [
    "Typical Angina", "Atypical Angina", "Non-anginal Pain", "Asymptomatic"
][x])
trestbps = st.number_input("Resting Blood Pressure")
chol = st.number_input("Cholesterol")
fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", [0, 1])
restecg = st.selectbox("Resting ECG Results", [0, 1, 2], format_func=lambda x: [
    "Normal", "ST-T wave abnormality", "Left ventricular hypertrophy"
][x])
thalach = st.number_input("Max Heart Rate Achieved")
exang = st.selectbox("Exercise Induced Angina", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
oldpeak = st.number_input("Oldpeak (ST depression it should be between 0 and 6)")
slope = st.selectbox("Slope of the peak exercise ST segment", [0, 1, 2], format_func=lambda x: [
    "Upsloping", "Flat", "Downsloping"
][x])

# Predict button
if st.button("Predict"):
    input_data = np.array([[age, sex, cp, trestbps, chol, fbs, restecg,
                            thalach, exang, oldpeak, slope]])
    
    prediction = model.predict(input_data)[0]

    st.subheader("Prediction Result:")
    if prediction == 1:
        result_text = "⚠️ High risk of heart disease detected!\nPlease consult a cardiologist as soon as possible."
        st.error("*High risk of heart disease detected!*")
        st.write("Please consult a cardiologist as soon as possible.")
    else:
        result_text = "✅ No heart disease detected.\nYour heart seems healthy — keep up the good habits!"
        st.success("*No heart disease detected.*")
        st.write("Your heart seems healthy — keep up the good habits!")

    # Download result
    result_text = f"""
    Heart Disease Prediction Result:

    Age: {age}
    Sex: {sex}
    Chest Pain Type: {cp}
    Resting Blood Pressure: {trestbps}
    Max Heart Rate: {thalach}
    Exercise Induced Angina: {exang}
    Oldpeak: {oldpeak}
    Slope of the peak exercise ST segmen: {slope}
    Result: {prediction}
    """
    st.download_button("Download Result", result_text, file_name="heart_report.txt")





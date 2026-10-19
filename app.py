import streamlit as st
import pandas as pd
from datetime import datetime
import os

rules = {
    "paracetamol": {"per_kg": 15, "max": 1000},
    "ibuprofen": {"per_kg": 10, "max": 400},
    "amoxicillin": {"per_kg": 20, "max": 500},
    "artemether": {"per_kg": 4, "max": 80}
}

def check_dose_v2(weight, drug):
    drug = drug.lower()
    if drug not in rules:
        return "NOT FOUND", 0
    per_kg = rules[drug]["per_kg"]
    max_dose = rules[drug]["max"]
    needed = weight * per_kg
    if needed > max_dose:
        return f"OVERDOSE! Needs {needed}mg but Max is {max_dose}mg", needed
    else:
        return f"SAFE - Give {needed}mg", needed

st.set_page_config(page_title="Dr-Carbon Hospital", page_icon="💊")
st.title("💊 Dr-Carbon Hospital Pharmacy System")
st.write("An app for hospital pharmacy that will ease record keeping and data tracking")

col1, col2 = st.columns(2)
with col1:
    patient_name = st.text_input("Patient Name")
    weight = st.number_input("Weight (kg)", min_value=1.0, value=60.0)
with col2:
    drug = st.selectbox("Select Drug", list(rules.keys()))
    department = st.selectbox("Department", ["OPD", "Pharmacy", "Emergency", "Paediatrics"])

if st.button("CHECK & SAVE"):
    status, dose = check_dose_v2(weight, drug)
    if "SAFE" in status:
        st.success(status)
    else:
        st.error(status)
    new_record = {"Time": datetime.now().strftime("%Y-%m-%d %H:%M"), "Patient": patient_name, "Weight": weight, "Drug": drug, "Dose": dose, "Status": status, "Dept": department}
    if os.path.exists("hospital_database.csv"):
        df = pd.read_csv("hospital_database.csv")
        df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
    else:
        df = pd.DataFrame([new_record])
    df.to_csv("hospital_database.csv", index=False)
    st.toast("Saved!")

st.divider()
st.subheader("Daily Report")
if os.path.exists("hospital_database.csv"):
    df = pd.read_csv("hospital_database.csv")
    st.metric("Total Patients", len(df))
    st.dataframe(df, use_container_width=True)
else:
    st.info("No patients yet.")

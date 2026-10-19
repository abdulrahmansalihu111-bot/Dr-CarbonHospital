import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- FULL HOSPITAL FORMULARY - 30 DRUGS ---
rules = {
    "paracetamol": {"per_kg": 15, "max": 1000, "use": "Pain/Fever"},
    "ibuprofen": {"per_kg": 10, "max": 400, "use": "Pain/Inflammation"},
    "amoxicillin": {"per_kg": 20, "max": 500, "use": "Antibiotic"},
    "artemether": {"per_kg": 4, "max": 80, "use": "Malaria"},
    "ciprofloxacin": {"per_kg": 15, "max": 750, "use": "Antibiotic"},
    "metronidazole": {"per_kg": 10, "max": 500, "use": "Antibiotic"},
    "azithromycin": {"per_kg": 10, "max": 500, "use": "Antibiotic"},
    "ceftriaxone": {"per_kg": 50, "max": 2000, "use": "Antibiotic Injection"},
    "gentamicin": {"per_kg": 5, "max": 160, "use": "Antibiotic Injection"},
    "ampiclox": {"per_kg": 25, "max": 500, "use": "Antibiotic"},
    "diclofenac": {"per_kg": 1, "max": 75, "use": "Pain"},
    "tramadol": {"per_kg": 2, "max": 100, "use": "Severe Pain"},
    "omeprazole": {"per_kg": 1, "max": 40, "use": "Ulcer"},
    "lansoprazole": {"per_kg": 1, "max": 30, "use": "Ulcer"},
    "metformin": {"per_kg": 10, "max": 1000, "use": "Diabetes"},
    "glibenclamide": {"per_kg": 0.1, "max": 10, "use": "Diabetes"},
    "lisinopril": {"per_kg": 0.1, "max": 20, "use": "Hypertension"},
    "amlodipine": {"per_kg": 0.1, "max": 10, "use": "Hypertension"},
    "losartan": {"per_kg": 0.7, "max": 100, "use": "Hypertension"},
    "furosemide": {"per_kg": 1, "max": 80, "use": "Diuretic"},
    "salbutamol": {"per_kg": 0.15, "max": 4, "use": "Asthma"},
    "prednisolone": {"per_kg": 1, "max": 60, "use": "Steroid"},
    "dexamethasone": {"per_kg": 0.2, "max": 10, "use": "Steroid"},
    "chlorpheniramine": {"per_kg": 0.2, "max": 4, "use": "Allergy"},
    "cetirizine": {"per_kg": 0.2, "max": 10, "use": "Allergy"},
    "albendazole": {"per_kg": 10, "max": 400, "use": "Worm"},
    "quinine": {"per_kg": 10, "max": 600, "use": "Malaria"},
    "artesunate": {"per_kg": 4, "max": 200, "use": "Malaria"},
    "coartem": {"per_kg": 4, "max": 80, "use": "Malaria"},
    "ORS": {"per_kg": 15, "max": 1000, "use": "Dehydration"}
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
        return f"SAFE - Give {needed}mg ({rules[drug]['use']})", needed

st.set_page_config(page_title="Dr-Carbon Hospital", page_icon="💊")
st.title("💊 Dr-Carbon Hospital V6")
st.caption(f"Full Formulary: {len(rules)} drugs - Hospital Pharmacy System")

# Searchable drug
search = st.text_input("🔍 Search Drug (type e.g. malar, pain, amox)")
if search:
    filtered = [d for d in rules.keys() if search.lower() in d.lower() or search.lower() in rules[d]["use"].lower()]
else:
    filtered = list(rules.keys())

col1, col2 = st.columns(2)
with col1:
    patient_name = st.text_input("Patient Name")
    weight = st.number_input("Weight (kg)", min_value=1.0, value=60.0)
with col2:
    drug = st.selectbox(f"Select Drug ({len(filtered)} found)", filtered)
    department = st.selectbox("Department", ["OPD", "Pharmacy", "Emergency", "Paediatrics", "ICU", "Maternity"])

if st.button("CHECK & SAVE"):
    status, dose = check_dose_v2(weight, drug)
    if "SAFE" in status:
        st.success(status)
    else:
        st.error(status)
    new_record = {"Time": datetime.now().strftime("%Y-%m-%d %H:%M"), "Patient": patient_name, "Weight": weight, "Drug": drug, "Dose": dose, "Status": status, "Dept": department, "Use": rules[drug]["use"]}
    df = pd.read_csv("hospital_database.csv") if os.path.exists("hospital_database.csv") else pd.DataFrame()
    df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
    df.to_csv("hospital_database.csv", index=False)
    st.toast("Saved!")

st.divider()
st.subheader("📊 Hospital Report")
if os.path.exists("hospital_database.csv"):
    df = pd.read_csv("hospital_database.csv")
    c1,c2,c3 = st.columns(3)
    c1.metric("Patients", len(df))
    c2.metric("Drugs in System", len(rules))
    c3.metric("Departments", df["Dept"].nunique() if "Dept" in df else 0)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No patients yet. Start adding to see report.")

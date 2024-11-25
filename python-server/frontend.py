import streamlit as st
import requests

API_BASE = "http://localhost:8000"  # Replace with your backend's URL if hosted elsewhere.

st.title("Organ Donation Registry")

# Tabs for different functionalities
tabs = st.tabs(["Register Patient", "Register Donor", "Find Matches", "View Matches"])

# Register Patient
with tabs[0]:
    st.header("Register Patient")
    name = st.text_input("Patient Name")
    required_organ = st.text_input("Required Organ")
    if st.button("Register Patient"):
        if name and required_organ:
            response = requests.post(f"{API_BASE}/register-patient", json={
                "name": name,
                "required_organ": required_organ
            })
            if response.status_code == 200:
                st.success(response.json()["message"])
            else:
                st.error(response.json().get("detail", "An error occurred."))
        else:
            st.warning("Please fill all fields.")

# Register Donor
with tabs[1]:
    st.header("Register Donor")
    name = st.text_input("Donor Name")
    organ_to_donate = st.text_input("Organ to Donate")
    if st.button("Register Donor"):
        if name and organ_to_donate:
            response = requests.post(f"{API_BASE}/register-donor", json={
                "name": name,
                "organ_to_donate": organ_to_donate
            })
            if response.status_code == 200:
                st.success(response.json()["message"])
            else:
                st.error(response.json().get("detail", "An error occurred."))
        else:
            st.warning("Please fill all fields.")

# Find Matches
with tabs[2]:
    st.header("Find Matches")
    if st.button("Find Matches"):
        response = requests.post(f"{API_BASE}/find-matches")
        if response.status_code == 200:
            st.success(response.json()["message"])
        else:
            st.error(response.json().get("detail", "An error occurred."))

# View Match
with tabs[3]:
    st.header("View Match")
    patient_id = st.number_input("Patient ID", min_value=1, step=1)
    if st.button("View Match"):
        if patient_id:
            response = requests.get(f"{API_BASE}/view-match/{patient_id}")
            if response.status_code == 200:
                data = response.json()
                st.write("Match Found" if data["is_matched"] else "No Match Found")
                if data["is_matched"]:
                    st.write(f"Donor ID: {data['donor_id']}")
                    st.write(f"Patient Hospital Approved: {data['patient_hospital_approved']}")
                    st.write(f"Donor Hospital Approved: {data['donor_hospital_approved']}")
            else:
                st.error(response.json().get("detail", "An error occurred."))
        else:
            st.warning("Please enter a valid Patient ID.")

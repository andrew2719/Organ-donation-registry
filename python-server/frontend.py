import streamlit as st
import requests

API_BASE = "http://localhost:8000"  # Replace with your backend's URL if hosted elsewhere.

st.title("Organ Donation Registry")

# Tabs for different functionalities
tabs = st.tabs([
    "Register Patient",
    "Register Donor",
    "Find Matches",
    "View Matches",
    "Approve Match",
    "Confirm Transaction"
])

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
    donor_name = st.text_input("Donor Name")
    organ_to_donate = st.text_input("Organ to Donate")
    if st.button("Register Donor"):
        if donor_name and organ_to_donate:
            response = requests.post(f"{API_BASE}/register-donor", json={
                "name": donor_name,
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

# View Matches
with tabs[3]:
    st.header("View Match")
    patient_id_view = st.number_input("Patient ID", min_value=1, step=1, key="view_patient_id")
    if st.button("View Match", key="view_match_button"):
        if patient_id_view:
            response = requests.get(f"{API_BASE}/view-match", params={"patient_id": int(patient_id_view)})
            if response.status_code == 200:
                data = response.json()
                if data["is_matched"]:
                    st.success("Match Found")
                    st.write(f"**Donor ID:** {data['donor_id']}")
                    st.write(f"**Patient Hospital Approved:** {data['patient_hospital_approved']}")
                    st.write(f"**Donor Hospital Approved:** {data['donor_hospital_approved']}")
                else:
                    st.warning("No Match Found")
            else:
                st.error(response.json().get("detail", "An error occurred."))
        else:
            st.warning("Please enter a valid Patient ID.")

# Approve Match
with tabs[4]:
    st.header("Approve Match")
    patient_id_approve = st.number_input("Patient ID", min_value=1, step=1, key="approve_patient_id")
    donor_id_approve = st.number_input("Donor ID", min_value=1, step=1, key="approve_donor_id")
    if st.button("Approve Match", key="approve_match_button"):
        if patient_id_approve and donor_id_approve:
            response = requests.post(f"{API_BASE}/approve-match", json={
                "patient_id": int(patient_id_approve),
                "donor_id": int(donor_id_approve)
            })
            if response.status_code == 200:
                st.success(response.json()["message"])
            else:
                st.error(response.json().get("detail", "An error occurred."))
        else:
            st.warning("Please enter valid Patient ID and Donor ID.")

# Confirm Transaction
with tabs[5]:
    st.header("Confirm Transaction")
    patient_id_confirm = st.number_input("Patient ID", min_value=1, step=1, key="confirm_patient_id")
    donor_id_confirm = st.number_input("Donor ID", min_value=1, step=1, key="confirm_donor_id")
    if st.button("Confirm Transaction", key="confirm_transaction_button"):
        if patient_id_confirm and donor_id_confirm:
            response = requests.post(f"{API_BASE}/confirm-transaction", json={
                "patient_id": int(patient_id_confirm),
                "donor_id": int(donor_id_confirm)
            })
            if response.status_code == 200:
                st.success(response.json()["message"])
            else:
                st.error(response.json().get("detail", "An error occurred."))
        else:
            st.warning("Please enter valid Patient ID and Donor ID.")

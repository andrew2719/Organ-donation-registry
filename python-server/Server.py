import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from web3 import Web3
import json

from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open('abi.json', 'r') as f:
    CONTRACT_ABI = json.load(f)

# Replace these with your keys
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
PUBLIC_ADDRESS = os.getenv("PUBLIC_ADDRESS")
INFURA_PROJECT_ID = os.getenv("INFURA_PROJECT_ID")

# Use the credentials
w3 = Web3(Web3.HTTPProvider(f'https://sepolia.infura.io/v3/{INFURA_PROJECT_ID}'))
CONTRACT_ADDRESS = '0x7A9453E92D95c8C89DB6C7E5a4707AdFAaF5587C'
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

class PatientRegistration(BaseModel):
    name: str
    required_organ: str

class DonorRegistration(BaseModel):
    name: str
    organ_to_donate: str

class MatchApproval(BaseModel):
    patient_id: int
    donor_id: int

class TransactionConfirmation(BaseModel):
    patient_id: int
    donor_id: int

def sign_and_send_transaction(transaction):
    signed_tx = w3.eth.account.sign_transaction(transaction, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return tx_hash.hex()

@app.post("/register-patient")
async def register_patient(patient: PatientRegistration):
    try:
        transaction = contract.functions.registerPatient(
            patient.name,
            patient.required_organ
        ).build_transaction({
            'from': PUBLIC_ADDRESS,
            'nonce': w3.eth.get_transaction_count(PUBLIC_ADDRESS),
            'gas': 200000,
            'gasPrice': w3.eth.gas_price
        })
        tx_hash = sign_and_send_transaction(transaction)
        return {"tx_hash": tx_hash, "message": "Patient registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/register-donor")
async def register_donor(donor: DonorRegistration):
    try:
        transaction = contract.functions.registerDonor(
            donor.name,
            donor.organ_to_donate
        ).build_transaction({
            'from': PUBLIC_ADDRESS,
            'nonce': w3.eth.get_transaction_count(PUBLIC_ADDRESS),
            'gas': 200000,
            'gasPrice': w3.eth.gas_price
        })
        tx_hash = sign_and_send_transaction(transaction)
        return {"tx_hash": tx_hash, "message": "Donor registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/find-matches")
async def find_matches():
    try:
        transaction = contract.functions.findAndLockMatch().build_transaction({
            'from': PUBLIC_ADDRESS,
            'nonce': w3.eth.get_transaction_count(PUBLIC_ADDRESS),
            'gas': 500000,
            'gasPrice': w3.eth.gas_price
        })
        tx_hash = sign_and_send_transaction(transaction)
        return {"tx_hash": tx_hash, "message": "Match finding executed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/approve-match")
async def approve_match(approval: MatchApproval):
    try:
        transaction = contract.functions.approveMatch(
            approval.patient_id,
            approval.donor_id
        ).build_transaction({
            'from': PUBLIC_ADDRESS,
            'nonce': w3.eth.get_transaction_count(PUBLIC_ADDRESS),
            'gas': 200000,
            'gasPrice': w3.eth.gas_price
        })
        tx_hash = sign_and_send_transaction(transaction)
        return {"tx_hash": tx_hash, "message": "Match approved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/view-match")
async def view_match(patient_id: int):
    try:
        match_info = contract.functions.viewMatch(patient_id).call()
        is_matched = match_info[0]
        donor_id = match_info[1]
        patient_hospital_approved = match_info[2]
        donor_hospital_approved = match_info[3]
        return {
            "is_matched": is_matched,
            "donor_id": donor_id,
            "patient_hospital_approved": patient_hospital_approved,
            "donor_hospital_approved": donor_hospital_approved
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/confirm-transaction")
async def confirm_transaction(confirmation: TransactionConfirmation):
    try:
        transaction = contract.functions.confirmTransactionComplete(
            confirmation.patient_id,
            confirmation.donor_id
        ).build_transaction({
            'from': PUBLIC_ADDRESS,
            'nonce': w3.eth.get_transaction_count(PUBLIC_ADDRESS),
            'gas': 200000,
            'gasPrice': w3.eth.gas_price
        })
        tx_hash = sign_and_send_transaction(transaction)
        return {"tx_hash": tx_hash, "message": "Transaction confirmed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)

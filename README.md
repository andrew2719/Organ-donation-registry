# Organ Donation Registry DApp

**This projects serves as a prototype, invalid requests like invalid ids, invalid confirmational executions need to be handled in the server side. Everything is working as intended in smartcontract like handling that invalidness.**

An Ethereum-based decentralized application (DApp) for managing organ donations and transplants, allowing hospitals to register patients and donors, find matches based on organ requirements, approve matches, and confirm organ donation transactions.

## Contract address : 0x7A9453E92D95c8C89DB6C7E5a4707AdFAaF5587C

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Setup](#environment-setup)
- [Smart Contract Deployment](#smart-contract-deployment)
- [Running the Backend Server](#running-the-backend-server)
- [Running the Frontend](#running-the-frontend)
- [How It Works](#how-it-works)
- [Technologies Used](#technologies-used)

## Introduction

This project is a decentralized application that facilitates the organ donation process between patients and donors through hospitals. It ensures transparency, security, and efficiency by leveraging blockchain technology. The smart contract handles patient and donor registrations, matches donors with patients based on organ requirements, and manages the approval and confirmation processes for organ transplants.

## Features

- **Patient Registration**: Hospitals can register patients in need of organ transplants.
- **Donor Registration**: Hospitals can register donors willing to donate organs.
- **Matching Algorithm**: Automatically finds and locks matches between patients and donors based on organ compatibility.
- **Approval Process**: Both patient's and donor's hospitals can approve matches.
- **Transaction Confirmation**: Hospitals can confirm the completion of organ donation transactions.
- **Frontend Interface**: User-friendly interface built with Streamlit for interacting with the system.
- **Backend Server**: FastAPI server acting as an intermediary between the frontend and the Ethereum blockchain.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.7+**
- **Node.js and npm** (for ApeWorx, if not installed via pip)
- **ApeWorx** (for smart contract development and testing)
- **MetaMask Wallet** (for managing Ethereum accounts)
- **Infura Account** (for Ethereum node access)

## Installation

Clone the repository:

```bash
git clone https://github.com/andrew2719/Organ-donation-registry.git
cd Organ-donation-registry
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Environment Setup

Create a `.env` file in the root directory and add the following variables:

```dotenv
PRIVATE_KEY=your_private_key
PUBLIC_ADDRESS=your_public_address
INFURA_PROJECT_ID=your_infura_project_id
```

- **PRIVATE_KEY**: Your Ethereum account's private key (keep this secure and do not share it).
- **PUBLIC_ADDRESS**: The public address associated with your private key.
- **INFURA_PROJECT_ID**: Your Infura project ID for accessing the Ethereum network.

**Important**: Never commit your `.env` file to a public repository.



## Smart Contract Deployment(if you want to deploy again)

The smart contract is developed using **ApeWorx**. Follow these steps to deploy it:

### Install ApeWorx

```bash
pip install eth-ape'[recommended-plugins]'
```

### Compile the Contract

```bash
ape compile
```

### Configure ApeWorx

Set up your Ethereum provider and account in `ape-config.yaml`:

```yaml
# ape-config.yaml
plugins:
  - name: solidity
  - name: infura
  - name: etherscan

default_ecosystem: ethereum

ethereum:
  default_network: sepolia # change if needed
  sepolia:
    default_provider: infura #change if needed
```

### Deploy the Contract

```bash
ape run deploy
```

This will deploy the contract to the specified network and output the contract address, which you'll need to update in your backend server code.

## Running the Backend Server

The backend server is built with **FastAPI** and interacts with the Ethereum blockchain via **Web3.py**.

### Update Contract Address and ABI

- **ABI**: Ensure the `abi.json` file in the root directory contains the ABI of your deployed smart contract.
- **Contract Address**: Update the `CONTRACT_ADDRESS` variable in the `Server.py` file with your deployed contract's address.

### Start the Server

```bash
python3 Server.py
```

- The server will start at `http://localhost:8000`.

## Running the Frontend

The frontend is built using **Streamlit**.

### Start the Streamlit App

```bash
streamlit run frontend.py
```

- The app will open in your default web browser at `http://localhost:8501`.

## How It Works

### Interaction Flow

1. **Registration**:
   - Hospitals register patients and donors via the frontend.
   - The backend server sends transactions to the smart contract to store this information on the blockchain.

2. **Finding Matches**:
   - Hospitals initiate the match-finding process.
   - The smart contract matches patients and donors based on organ compatibility and locks the match.

3. **Viewing Matches**:
   - Hospitals can view match details, including donor information and approval statuses.

4. **Approval**:
   - Both the patient's and donor's hospitals approve the match.
   - The smart contract records the approvals.

5. **Transaction Confirmation**:
   - After the organ donation is completed, hospitals confirm the transaction.
   - The smart contract updates the status, completing the process.

### Backend and Frontend Interaction

- **Frontend**: Provides a user-friendly interface for hospitals to interact with the system.
- **Backend**: Handles HTTP requests from the frontend, interacts with the smart contract, and returns responses.
- **Smart Contract**: Manages the core logic, data storage, and state changes on the Ethereum blockchain.

### Environment Variables

- The `.env` file contains sensitive information like private keys and should be kept secure.
- The backend server uses these variables to sign transactions and interact with the blockchain.

## Technologies Used

- **Ethereum Blockchain**: For decentralized data storage and management.
- **Solidity**: Smart contract programming language.
- **ApeWorx**: For smart contract development and testing.
- **Python**: Backend server and frontend scripting.
- **FastAPI**: High-performance backend framework.
- **Web3.py**: Ethereum blockchain interaction library.
- **Streamlit**: For building the frontend interface.
- **Infura**: Ethereum node provider.
- **dotenv**: For environment variable management.


---

**Disclaimer**: This project is for educational purposes. Ensure compliance with all legal and ethical guidelines when dealing with sensitive information like medical records and private keys.

# License

This project is licensed under the **MIT License**.

---

**End of README**
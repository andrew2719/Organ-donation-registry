// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract OrganDonationRegistry {
    // Structs to store patient and donor information with hospital addresses
    struct Patient {
        string name;
        uint256 patientId;
        string requiredOrgan;
        address hospitalAddress;
        bool isRegistered;
        bool hasReceivedOrgan;
        bool isLocked;
        uint256 matchedDonorId;
        bool hospitalApproved;
    }
    
    struct Donor {
        string name;    
        uint256 donorId;
        string organToDonate;
        address hospitalAddress;
        bool isRegistered;
        bool hasOrgansHarvested;
        bool isLocked;
        uint256 matchedPatientId;
        bool hospitalApproved;
    }
    
    // State variables
    uint256 public patientCounter;
    uint256 public donorCounter;
    
    // Mappings to store patient and donor data
    mapping(uint256 => Patient) public patients;
    mapping(uint256 => Donor) public donors;
    
    // Events
    event PatientRegistered(uint256 patientId, string name, string requiredOrgan, address hospital);
    event DonorRegistered(uint256 donorId, string name, string organToDonate, address hospital);
    event OrganMatched(uint256 patientId, uint256 donorId, string organ);
    event MatchLocked(uint256 patientId, uint256 donorId, address patientHospital, address donorHospital);
    event HospitalApproved(uint256 patientId, uint256 donorId, address approvingHospital);
    event TransactionCompleted(uint256 patientId, uint256 donorId);
    
    constructor() {
        patientCounter = 0;
        donorCounter = 0;
    }
    
    // Function to register a new patient
    function registerPatient(
        string memory _name,
        string memory _requiredOrgan
    ) public {
        patientCounter++;
        patients[patientCounter] = Patient({
            name: _name,
            patientId: patientCounter,
            requiredOrgan: _requiredOrgan,
            hospitalAddress: msg.sender,
            isRegistered: true,
            hasReceivedOrgan: false,
            isLocked: false,
            matchedDonorId: 0,
            hospitalApproved: false
        });
        
        emit PatientRegistered(patientCounter, _name, _requiredOrgan, msg.sender);
    }
    
    // Function to register a new donor
    function registerDonor(
        string memory _name,
        string memory _organToDonate
    ) public {
        donorCounter++;
        donors[donorCounter] = Donor({
            name: _name,
            donorId: donorCounter,
            organToDonate: _organToDonate,
            hospitalAddress: msg.sender,
            isRegistered: true,
            hasOrgansHarvested: false,
            isLocked: false,
            matchedPatientId: 0,
            hospitalApproved: false
        });
        
        emit DonorRegistered(donorCounter, _name, _organToDonate, msg.sender);
    }
    
    // Function to find and lock matching organs based on priority
    function findAndLockMatch() public {
        // Loop through patients from first to last (priority order)
        for (uint256 i = 1; i <= patientCounter; i++) {
            // Skip if patient is already matched or has received organ
            if (patients[i].isLocked || patients[i].hasReceivedOrgan || !patients[i].isRegistered) {
                continue;
            }
            
            // Look for matching donor
            for (uint256 j = 1; j <= donorCounter; j++) {
                if (!donors[j].isLocked && 
                    !donors[j].hasOrgansHarvested && 
                    donors[j].isRegistered &&
                    keccak256(abi.encodePacked(donors[j].organToDonate)) == 
                    keccak256(abi.encodePacked(patients[i].requiredOrgan))) {
                    
                    // Lock the match
                    patients[i].isLocked = true;
                    patients[i].matchedDonorId = j;
                    donors[j].isLocked = true;
                    donors[j].matchedPatientId = i;
                    
                    emit MatchLocked(i, j, patients[i].hospitalAddress, donors[j].hospitalAddress);
                    break;
                }
            }
        }
    }
    
    // Function for hospitals to approve the match
    function approveMatch(uint256 _patientId, uint256 _donorId) public {
        require(_patientId <= patientCounter && _donorId <= donorCounter, "Invalid IDs");
        require(patients[_patientId].isLocked && donors[_donorId].isLocked, "Match not locked");
        require(patients[_patientId].matchedDonorId == _donorId, "Invalid match");
        require(msg.sender == patients[_patientId].hospitalAddress || 
                msg.sender == donors[_donorId].hospitalAddress, "Not authorized");
        
        if (msg.sender == patients[_patientId].hospitalAddress) {
            require(!patients[_patientId].hospitalApproved, "Already approved");
            patients[_patientId].hospitalApproved = true;
        } else {
            require(!donors[_donorId].hospitalApproved, "Already approved");
            donors[_donorId].hospitalApproved = true;
        }
        
        emit HospitalApproved(_patientId, _donorId, msg.sender);
    }
    
    // Function to confirm organ donation completion
    function confirmTransactionComplete(uint256 _patientId, uint256 _donorId) public {
        require(_patientId <= patientCounter && _donorId <= donorCounter, "Invalid IDs");
        require(patients[_patientId].isLocked && donors[_donorId].isLocked, "Match not locked");
        require(patients[_patientId].hospitalApproved && donors[_donorId].hospitalApproved, 
                "Both hospitals must approve first");
        require(msg.sender == patients[_patientId].hospitalAddress || 
                msg.sender == donors[_donorId].hospitalAddress, "Not authorized");
        
        patients[_patientId].hasReceivedOrgan = true;
        donors[_donorId].hasOrgansHarvested = true;
        patients[_patientId].isLocked = false;
        donors[_donorId].isLocked = false;
        
        emit TransactionCompleted(_patientId, _donorId);
    }
    
    // Function to view current matches
    function viewMatch(uint256 _patientId) public view returns (
        bool isMatched,
        uint256 donorId,
        bool patientHospitalApproved,
        bool donorHospitalApproved
    ) {
        require(_patientId <= patientCounter, "Invalid patient ID");
        
        if (patients[_patientId].isLocked) {
            uint256 matchedDonorId = patients[_patientId].matchedDonorId;
            return (
                true,
                matchedDonorId,
                patients[_patientId].hospitalApproved,
                donors[matchedDonorId].hospitalApproved
            );
        }
        return (false, 0, false, false);
    }
}
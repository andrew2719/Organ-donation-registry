import pytest
from ape import accounts, project
from eth_utils import encode_hex

@pytest.fixture
def organ_donation_registry():
    deployer = accounts.test_accounts[0]
    return deployer.deploy(project.OrganDonationRegistry)

@pytest.fixture
def hospitals():
    return accounts.test_accounts[1:4]  # Get 3 test accounts for hospitals

def test_patient_registration(organ_donation_registry, hospitals):
    # Register a patient from hospital1
    tx = organ_donation_registry.registerPatient("Patient1", "kidney", sender=hospitals[0])
    
    # Verify patient registration
    patient = organ_donation_registry.patients(1)
    assert patient[0] == "Patient1"  # name
    assert patient[1] == 1  # patientId
    assert patient[2] == "kidney"  # requiredOrgan
    assert patient[3] == hospitals[0]  # hospitalAddress
    assert patient[4] == True  # isRegistered
    assert patient[5] == False  # hasReceivedOrgan
    assert patient[6] == False  # isLocked

def test_donor_registration(organ_donation_registry, hospitals):
    # Register a donor from hospital2
    tx = organ_donation_registry.registerDonor("Donor1", "kidney", sender=hospitals[1])
    
    # Verify donor registration
    donor = organ_donation_registry.donors(1)
    assert donor[0] == "Donor1"  # name
    assert donor[1] == 1  # donorId
    assert donor[2] == "kidney"  # organToDonate
    assert donor[3] == hospitals[1]  # hospitalAddress
    assert donor[4] == True  # isRegistered
    assert donor[5] == False  # hasOrgansHarvested
    assert donor[6] == False  # isLocked

def test_matching_process(organ_donation_registry, hospitals):
    # Register patients from different hospitals
    organ_donation_registry.registerPatient("Patient1", "kidney", sender=hospitals[0])
    organ_donation_registry.registerPatient("Patient2", "kidney", sender=hospitals[1])
    
    # Register donors from different hospitals
    organ_donation_registry.registerDonor("Donor1", "kidney", sender=hospitals[1])
    organ_donation_registry.registerDonor("Donor2", "liver", sender=hospitals[2])
    
    # Find and lock matches with sender specified
    organ_donation_registry.findAndLockMatch(sender=hospitals[0])
    
    # Check first patient's match
    match_info = organ_donation_registry.viewMatch(2)
    assert match_info[0] == True  # isMatched
    assert match_info[1] == 2     # matched with donorId 1

def test_approval_process(organ_donation_registry, hospitals):
    # Setup: Register patient and donor
    organ_donation_registry.registerPatient("Patient1", "kidney", sender=hospitals[0])
    organ_donation_registry.registerDonor("Donor1", "kidney", sender=hospitals[1])
    
    # Find matches
    organ_donation_registry.findAndLockMatch(sender=hospitals[0])
    
    # Both hospitals approve the match
    organ_donation_registry.approveMatch(1, 1, sender=hospitals[0])
    organ_donation_registry.approveMatch(1, 1, sender=hospitals[1])
    
    # Check approvals
    match_info = organ_donation_registry.viewMatch(1)
    assert match_info[2] == True  # patientHospitalApproved
    assert match_info[3] == True  # donorHospitalApproved

def test_complete_transaction(organ_donation_registry, hospitals):
    # Setup: Register, match, and approve
    organ_donation_registry.registerPatient("Patient1", "kidney", sender=hospitals[0])
    organ_donation_registry.registerDonor("Donor1", "kidney", sender=hospitals[1])
    organ_donation_registry.findAndLockMatch(sender=hospitals[0])
    organ_donation_registry.approveMatch(1, 1, sender=hospitals[0])
    organ_donation_registry.approveMatch(1, 1, sender=hospitals[1])
    
    # Complete the transaction
    organ_donation_registry.confirmTransactionComplete(1, 1, sender=hospitals[0])
    
    # Verify completion
    patient = organ_donation_registry.patients(1)
    donor = organ_donation_registry.donors(1)
    assert patient[5] == True  # hasReceivedOrgan
    assert donor[5] == True    # hasOrgansHarvested
    assert patient[6] == False # isLocked (should be unlocked after completion)
    assert donor[6] == False   # isLocked (should be unlocked after completion)

def test_priority_matching(organ_donation_registry, hospitals):
    # Register multiple patients needing kidney
    organ_donation_registry.registerPatient("Patient1", "kidney", sender=hospitals[0])
    organ_donation_registry.registerPatient("Patient2", "kidney", sender=hospitals[1])
    
    # Register one kidney donor
    organ_donation_registry.registerDonor("Donor1", "kidney", sender=hospitals[2])
    
    # Find matches
    organ_donation_registry.findAndLockMatch(sender=hospitals[0])
    
    # Verify first patient got the match (priority)
    match_info = organ_donation_registry.viewMatch(1)
    assert match_info[0] == True  # First patient should be matched
    
    match_info_2 = organ_donation_registry.viewMatch(2)
    assert match_info_2[0] == False  # Second patient should not be matched

def test_error_cases(organ_donation_registry, hospitals):
    # Setup
    organ_donation_registry.registerPatient("Patient1", "kidney", sender=hospitals[0])
    organ_donation_registry.registerDonor("Donor1", "kidney", sender=hospitals[1])
    
    # Try to approve match before matching
    with pytest.raises(Exception):
        organ_donation_registry.approveMatch(1, 1, sender=hospitals[0])
    
    # Match them
    organ_donation_registry.findAndLockMatch(sender=hospitals[0])
    
    # Try to complete transaction before both approvals
    with pytest.raises(Exception):
        organ_donation_registry.confirmTransactionComplete(1, 1, sender=hospitals[0])
    
    # Try to match with wrong hospital
    with pytest.raises(Exception):
        organ_donation_registry.approveMatch(1, 1, sender=hospitals[2])  # Wrong hospital

def test_multiple_organ_types(organ_donation_registry, hospitals):
    # Register different organ types
    organ_donation_registry.registerPatient("Patient1", "kidney", sender=hospitals[0])
    organ_donation_registry.registerPatient("Patient2", "liver", sender=hospitals[0])
    organ_donation_registry.registerDonor("Donor1", "liver", sender=hospitals[1])
    organ_donation_registry.registerDonor("Donor2", "kidney", sender=hospitals[1])
    
    # Find matches
    organ_donation_registry.findAndLockMatch(sender=hospitals[0])
    
    # Verify correct organ matching
    match_info_1 = organ_donation_registry.viewMatch(1)
    assert match_info_1[1] == 2  # Patient1 should match with Donor2 (kidney)
    
    match_info_2 = organ_donation_registry.viewMatch(2)
    assert match_info_2[1] == 1  # Patient2 should match with Donor1 (liver)
from ape import accounts, project

def main():
    """Deploy the OrganDonationRegistry contract."""
    
    # Get the account to deploy with
    account = accounts.load('andrew')
    print(f"Deploying from account: {account.address}")
    
    # Deploy the contract
    registry = account.deploy(project.OrganDonationRegistry)
    print(f"OrganDonationRegistry deployed at: {registry.address}")
    
    return registry
def mock_lead_capture(name, email, platform):
    """
    Simulates a backend call to capture lead information.
    """
    print(f"\n[TOOL EXECUTION] Lead captured successfully: {name}, {email}, {platform}")
    return f"Success: Lead details for {name} saved to the database."

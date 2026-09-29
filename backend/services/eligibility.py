def check_single_scheme_eligibility(user, scheme):
    """
    Compares a user profile against a single scheme's rules.
    Returns a dictionary with the result and the reasons.
    """
    is_eligible = True
    reasons = []

    # 1. State Check
    if scheme['state_applicability'] != 'All' and scheme['state_applicability'] != user['state']:
        is_eligible = False
        reasons.append(f"✗ Scheme is only for {scheme['state_applicability']} state.")
    else:
        reasons.append(f"✓ State requirement satisfied.")

    # 2. Age Check
    if user['age'] < scheme['min_age']:
        is_eligible = False
        reasons.append(f"✗ You are below the minimum age of {scheme['min_age']}.")
    elif scheme['max_age'] > 0 and user['age'] > scheme['max_age']:
        is_eligible = False
        reasons.append(f"✗ You are above the maximum age of {scheme['max_age']}.")
    else:
        reasons.append(f"✓ Age requirement satisfied.")

    # 3. Income Check (If max_income is 0, it means there is no limit)
    if scheme['max_income'] > 0 and user['annual_income'] > scheme['max_income']:
        is_eligible = False
        reasons.append(f"✗ Annual income exceeds the limit of ₹{scheme['max_income']}.")
    else:
        reasons.append(f"✓ Income requirement satisfied.")

    # 4. Gender Check
    if scheme['target_gender'] != 'All' and scheme['target_gender'] != user['gender']:
        is_eligible = False
        reasons.append(f"✗ Scheme is specifically for {scheme['target_gender']}s.")
    else:
        reasons.append(f"✓ Gender requirement satisfied.")

    # 5. Occupation Check
    if scheme['target_occupation'] != 'All' and scheme['target_occupation'] != user['occupation']:
        is_eligible = False
        reasons.append(f"✗ Scheme requires occupation to be {scheme['target_occupation']}.")
    else:
        reasons.append(f"✓ Occupation requirement satisfied.")

    return {
        "scheme": scheme,
        "is_eligible": is_eligible,
        "reasons": reasons
    }
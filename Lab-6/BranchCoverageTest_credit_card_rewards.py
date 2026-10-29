"""
BranchCoverageTest_credit_card_rewards.py
Comprehensive branch coverage test suite designed to evaluate all decision branches,
compound boolean conditions, boundary limits, and edge cases to achieve 100% branch coverage.
"""

import pytest
from credit_card_rewards import reward_points, late_payment_fee, card_status


# =====================================================================
# Branch Coverage Tests for reward_points()
# =====================================================================

def test_reward_points_invalid_tier():
    """Branch: card_tier not in POINTS_PER_100 -> True (raises ValueError)."""
    with pytest.raises(ValueError, match="unknown card tier"):
        reward_points("silver", 1000, "grocery", False)


def test_reward_points_zero_amount():
    """Branch: amount <= 0 -> True (amount == 0 boundary)."""
    with pytest.raises(ValueError, match="invalid amount"):
        reward_points("classic", 0, "grocery", False)


def test_reward_points_negative_amount():
    """Branch: amount <= 0 -> True (amount < 0 edge case)."""
    with pytest.raises(ValueError, match="invalid amount"):
        reward_points("gold", -100, "dining", False)


def test_reward_points_fuel_category():
    """Branch: category == 'fuel' -> True (returns 0)."""
    assert reward_points("platinum", 1000, "fuel", True) == 0


def test_reward_points_dining_category():
    """Branch: category == 'dining' (1st condition of OR is True)."""
    # (600 // 100) * 2 (gold) * 2 (dining) = 24
    assert reward_points("gold", 600, "dining", False) == 24


def test_reward_points_travel_category():
    """Branch: category == 'travel' (1st condition False, 2nd condition True)."""
    # (500 // 100) * 4 (platinum) * 2 (travel) = 40
    assert reward_points("platinum", 500, "travel", False) == 40


def test_reward_points_standard_category():
    """Branch: neither dining nor travel (both conditions of OR are False)."""
    # (1000 // 100) * 1 (classic) = 10
    assert reward_points("classic", 1000, "grocery", False) == 10


def test_reward_points_weekend_non_classic():
    """Branch: is_weekend=True AND card_tier != 'classic' -> True & True (+50)."""
    # (200 // 100) * 2 (gold) + 50 (weekend bonus) = 54
    assert reward_points("gold", 200, "shopping", True) == 54


def test_reward_points_weekend_classic():
    """Branch: is_weekend=True AND card_tier == 'classic' -> True & False (no bonus)."""
    # (500 // 100) * 1 (classic) = 5 (no weekend bonus for classic)
    assert reward_points("classic", 500, "shopping", True) == 5


def test_reward_points_weekday_non_classic():
    """Branch: is_weekend=False AND card_tier != 'classic' -> False (no bonus)."""
    # (300 // 100) * 4 (platinum) = 12
    assert reward_points("platinum", 300, "shopping", False) == 12


# =====================================================================
# Branch Coverage Tests for late_payment_fee()
# =====================================================================

def test_late_payment_fee_days_late_zero():
    """Branch: days_late <= 0 (1st condition of OR is True) -> returns 0."""
    assert late_payment_fee(5000, 0) == 0


def test_late_payment_fee_days_late_negative():
    """Branch: days_late < 0 (1st condition of OR is True) -> returns 0."""
    assert late_payment_fee(5000, -3) == 0


def test_late_payment_fee_outstanding_zero():
    """Branch: days_late > 0 AND outstanding <= 0 (2nd condition of OR is True) -> returns 0."""
    assert late_payment_fee(0, 10) == 0


def test_late_payment_fee_outstanding_negative():
    """Branch: days_late > 0 AND outstanding < 0 (2nd condition of OR is True) -> returns 0."""
    assert late_payment_fee(-500, 10) == 0


def test_late_payment_fee_tier1_boundary():
    """Branch: outstanding <= 1000 -> True at exact boundary 1000."""
    assert late_payment_fee(1000, 15) == 100


def test_late_payment_fee_tier1_interior():
    """Branch: outstanding <= 1000 -> True below boundary (500)."""
    assert late_payment_fee(500, 15) == 100


def test_late_payment_fee_tier2_boundary_lower():
    """Branch: outstanding > 1000 and <= 10000 -> True just above 1000 (1001)."""
    assert late_payment_fee(1001, 15) == 500


def test_late_payment_fee_tier2_boundary_upper():
    """Branch: outstanding <= 10000 -> True at exact boundary 10000."""
    assert late_payment_fee(10000, 15) == 500


def test_late_payment_fee_tier3():
    """Branch: outstanding > 10000 -> False for elif, fee = 1000."""
    assert late_payment_fee(10001, 15) == 1000


def test_late_payment_fee_days_late_boundary_no_surcharge():
    """Branch: days_late > 30 -> False at exact boundary 30 (no surcharge)."""
    assert late_payment_fee(5000, 30) == 500


def test_late_payment_fee_days_late_surcharge():
    """Branch: days_late > 30 -> True at boundary 31 (+750 surcharge)."""
    # 500 + 750 = 1250
    assert late_payment_fee(5000, 31) == 1250


# =====================================================================
# Branch Coverage Tests for card_status()
# =====================================================================

def test_card_status_frozen_priority():
    """Branch: is_frozen == True -> returns 'frozen' immediately."""
    assert card_status(95, 5, True) == "frozen"


def test_card_status_blocked_boundary():
    """Branch: missed_payments >= 3 -> True at exact boundary 3."""
    assert card_status(20, 3, False) == "blocked"


def test_card_status_blocked_above_boundary():
    """Branch: missed_payments >= 3 -> True for > 3."""
    assert card_status(20, 5, False) == "blocked"


def test_card_status_over_limit_risk_boundary_above():
    """Branch: utilisation_percent > 90 -> True just above boundary (90.1)."""
    assert card_status(90.1, 0, False) == "over limit risk"


def test_card_status_over_limit_risk_high():
    """Branch: utilisation_percent > 90 -> True for high utilisation (95)."""
    assert card_status(95, 1, False) == "over limit risk"


def test_card_status_watch_utilisation_branch():
    """Branch: utilisation_percent > 30 (1st condition of OR is True)."""
    assert card_status(30.1, 0, False) == "watch"


def test_card_status_watch_missed_payments_branch():
    """Branch: utilisation <= 30 AND missed_payments > 0 (2nd condition of OR is True)."""
    assert card_status(25, 1, False) == "watch"


def test_card_status_good_at_boundary():
    """Branch: utilisation == 30, missed_payments == 0 (both False at boundary)."""
    assert card_status(30, 0, False) == "good"


def test_card_status_good_healthy():
    """Branch: utilisation < 30, missed_payments == 0 -> returns 'good'."""
    assert card_status(10, 0, False) == "good"

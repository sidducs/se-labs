"""
CodeCoverageTest_credit_card_rewards.py
Test cases focused on achieving >= 90% statement (line) coverage
for the credit_card_rewards module.
"""

import pytest
from credit_card_rewards import reward_points, late_payment_fee, card_status


# --- Tests for reward_points statement coverage ---

def test_reward_points_unknown_card():
    # Covers lines 5-6 (raises ValueError for unknown card tier)
    with pytest.raises(ValueError, match="unknown card tier"):
        reward_points("titanium", 1000, "grocery", False)


def test_reward_points_invalid_amount():
    # Covers lines 7-8 (raises ValueError for non-positive amount)
    with pytest.raises(ValueError, match="invalid amount"):
        reward_points("classic", -50, "grocery", False)


def test_reward_points_fuel_category():
    # Covers lines 9-10 (category == "fuel" returns 0)
    assert reward_points("gold", 1000, "fuel", False) == 0


def test_reward_points_standard_classic():
    # Covers lines 11, 16 (standard point calculation and return)
    assert reward_points("classic", 1000, "grocery", False) == 10


def test_reward_points_dining_multiplier():
    # Covers lines 12-13 (dining doubles points)
    assert reward_points("gold", 500, "dining", False) == 20


def test_reward_points_weekend_bonus():
    # Covers lines 14-15 (weekend bonus adds 50 points for non-classic)
    assert reward_points("platinum", 200, "shopping", True) == 58


# --- Tests for late_payment_fee statement coverage ---

def test_late_payment_fee_on_time():
    # Covers lines 20-21 (returns 0 when days_late <= 0)
    assert late_payment_fee(5000, 0) == 0


def test_late_payment_fee_tier1():
    # Covers lines 22-23 (outstanding <= 1000 -> fee = 100)
    assert late_payment_fee(500, 10) == 100


def test_late_payment_fee_tier2():
    # Covers lines 24-25 (1000 < outstanding <= 10000 -> fee = 500)
    assert late_payment_fee(5000, 10) == 500


def test_late_payment_fee_tier3_and_over_30_days():
    # Covers lines 26-27, 28-29 (outstanding > 10000 -> fee = 1000; days_late > 30 -> +750)
    assert late_payment_fee(15000, 35) == 1750


# --- Tests for card_status statement coverage ---

def test_card_status_frozen():
    # Covers lines 34-35 (is_frozen -> "frozen")
    assert card_status(50, 0, True) == "frozen"


def test_card_status_blocked():
    # Covers lines 36-37 (missed_payments >= 3 -> "blocked")
    assert card_status(50, 3, False) == "blocked"


def test_card_status_over_limit_risk():
    # Covers lines 38-39 (utilisation_percent > 90 -> "over limit risk")
    assert card_status(95, 0, False) == "over limit risk"


def test_card_status_watch():
    # Covers lines 40-41 (utilisation_percent > 30 -> "watch")
    assert card_status(50, 0, False) == "watch"


def test_card_status_good():
    # Covers line 42 (default return "good")
    assert card_status(20, 0, False) == "good"

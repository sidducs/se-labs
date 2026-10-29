import pytest
from credit_card_rewards import reward_points, late_payment_fee, card_status


# =====================================================================
# Starter Example Test Cases
# =====================================================================

def test_classic_grocery():
    assert reward_points("classic", 1000, "grocery", False) == 10


def test_paid_on_time():
    assert late_payment_fee(5000, 0) == 0


# =====================================================================
# Additional Test Cases for Comprehensive Code & Branch Coverage (100%)
# =====================================================================

# --- reward_points() ---

def test_reward_points_unknown_card_tier():
    with pytest.raises(ValueError, match="unknown card tier"):
        reward_points("titanium", 1000, "grocery", False)


def test_reward_points_zero_amount():
    with pytest.raises(ValueError, match="invalid amount"):
        reward_points("classic", 0, "grocery", False)


def test_reward_points_negative_amount():
    with pytest.raises(ValueError, match="invalid amount"):
        reward_points("gold", -50, "dining", False)


def test_reward_points_fuel_category():
    assert reward_points("platinum", 1000, "fuel", True) == 0


def test_reward_points_dining_multiplier():
    # (500 // 100) * 2 (gold multiplier) * 2 (dining) = 20
    assert reward_points("gold", 500, "dining", False) == 20


def test_reward_points_travel_multiplier():
    # (500 // 100) * 4 (platinum multiplier) * 2 (travel) = 40
    assert reward_points("platinum", 500, "travel", False) == 40


def test_reward_points_weekend_bonus_gold():
    # (200 // 100) * 2 + 50 = 54
    assert reward_points("gold", 200, "shopping", True) == 54


def test_reward_points_weekend_classic_no_bonus():
    # (500 // 100) * 1 = 5 (no bonus for classic)
    assert reward_points("classic", 500, "shopping", True) == 5


def test_reward_points_weekday_non_classic():
    # (300 // 100) * 4 = 12
    assert reward_points("platinum", 300, "shopping", False) == 12


# --- late_payment_fee() ---

def test_late_payment_fee_negative_days():
    assert late_payment_fee(5000, -5) == 0


def test_late_payment_fee_zero_outstanding():
    assert late_payment_fee(0, 10) == 0


def test_late_payment_fee_negative_outstanding():
    assert late_payment_fee(-200, 10) == 0


def test_late_payment_fee_tier1_boundary():
    assert late_payment_fee(1000, 10) == 100


def test_late_payment_fee_tier1_interior():
    assert late_payment_fee(500, 10) == 100


def test_late_payment_fee_tier2_boundary_lower():
    assert late_payment_fee(1001, 10) == 500


def test_late_payment_fee_tier2_boundary_upper():
    assert late_payment_fee(10000, 10) == 500


def test_late_payment_fee_tier3():
    assert late_payment_fee(15000, 10) == 1000


def test_late_payment_fee_late_surcharge_boundary():
    assert late_payment_fee(5000, 30) == 500


def test_late_payment_fee_late_surcharge():
    # 500 + 750 = 1250
    assert late_payment_fee(5000, 35) == 1250


# --- card_status() ---

def test_card_status_frozen():
    assert card_status(95, 5, True) == "frozen"


def test_card_status_blocked_boundary():
    assert card_status(50, 3, False) == "blocked"


def test_card_status_blocked_above():
    assert card_status(50, 5, False) == "blocked"


def test_card_status_over_limit_risk():
    assert card_status(95, 0, False) == "over limit risk"


def test_card_status_watch_utilisation():
    assert card_status(50, 0, False) == "watch"


def test_card_status_watch_missed_payments():
    assert card_status(25, 1, False) == "watch"


def test_card_status_good():
    assert card_status(30, 0, False) == "good"


def test_card_status_good_low_utilisation():
    assert card_status(10, 0, False) == "good"

# Lab 6: Code and Branch Coverage Analysis — Credit Card Rewards

**Student Roll/ID:** 61  
**Module Under Test:** `credit_card_rewards.py`  
**Assigned Repository:** [SETAPESU26/L6_L7_61_credit_card_rewards](https://github.com/SETAPESU26/L6_L7_61_credit_card_rewards)

---

## 1. Overview & Objective

This lab focuses on measuring, analyzing, and improving code coverage and branch coverage using Python's `coverage` and `pytest` tools. The objective is to design comprehensive unit test suites that cover edge cases, decision branches, and boundary conditions to achieve **100% statement (line) coverage** and **100% branch coverage** (exceeding the target of >= 90%).

### Key Concepts

| Coverage Type | Description | Target | Achieved |
| :--- | :--- | :--- | :--- |
| **Line Coverage** | Percentage of executable code statements exercised at least once | $\ge 90\%$ | **100%** |
| **Branch Coverage** | Percentage of control flow branches (`if`, `elif`, boolean conditions) evaluating to both `True` and `False` | $\ge 90\%$ | **100%** |

---

## 2. Deliverables & File Structure

```text
Lab-6/
├── Lab_6_Code&BranchCoverage_Student_Handout.docx.pdf # Lab manual & instructions
├── README.md                                          # Complete documentation & analysis report
├── credit_card_rewards.py                             # Core application module under test
├── CodeCoverageTest_credit_card_rewards.py            # Test suite for code (line) coverage (100%)
├── BranchCoverageTest_credit_card_rewards.py          # Test suite for branch coverage (100%)
├── test_credit_card_rewards.py                        # Unified test suite with all test cases
└── screenshots/
    ├── code_coverage_report.png                       # Terminal output for code coverage (100% line coverage)
    └── branch_coverage_report.png                     # Terminal output for branch coverage (100% branch coverage)
```

---

## 3. Coverage Analysis Summary

### Baseline (Initial Test Case)
Running initial starter tests (`test_credit_card_rewards.py` with 2 tests):
- **Line Coverage:** 37% (22 missed statements out of 35)
- **Branch Coverage:** 31% (6 partial branches out of 26)

### After Code Coverage Test Cases (`CodeCoverageTest_credit_card_rewards.py`)
- **Statements Executed:** 35 / 35
- **Statement (Line) Coverage:** **100%**
- **Tests Passed:** 15 / 15

### After Branch Coverage Test Cases (`BranchCoverageTest_credit_card_rewards.py`)
- **Statements Executed:** 35 / 35
- **Branches Covered:** 26 / 26 (0 partial branches)
- **Branch Coverage:** **100%**
- **Tests Passed:** 30 / 30

---

## 4. Decision & Branch Coverage Details

| Function | Decision / Expression | Branch Evaluated True | Branch Evaluated False |
| :--- | :--- | :--- | :--- |
| `reward_points` | `card_tier not in POINTS_PER_100` | Unknown tier (`"titanium"`) raises `ValueError` | Valid tiers (`"classic"`, `"gold"`, `"platinum"`) |
| `reward_points` | `amount <= 0` | Boundary `0` and negative `-50` raise `ValueError` | Valid positive amounts |
| `reward_points` | `category == "fuel"` | `"fuel"` returns 0 points | Other categories proceed |
| `reward_points` | `category == "dining" or category == "travel"` | `"dining"` (2x multiplier) and `"travel"` (2x multiplier) | `"grocery"` / `"shopping"` (standard points) |
| `reward_points` | `is_weekend and card_tier != "classic"` | Weekend with Gold/Platinum (+50 bonus) | Weekend with Classic (no bonus), Weekday (no bonus) |
| `late_payment_fee` | `days_late <= 0 or outstanding <= 0` | `days_late <= 0` (0 fee) or `outstanding <= 0` (0 fee) | Both positive (`days_late > 0` and `outstanding > 0`) |
| `late_payment_fee` | `outstanding <= 1000` | Outstanding `500` and boundary `1000` (fee = 100) | Outstanding > 1000 proceeds to `elif` |
| `late_payment_fee` | `outstanding <= 10000` | Boundary `1001` and `10000` (fee = 500) | Outstanding > 10000 (fee = 1000) |
| `late_payment_fee` | `days_late > 30` | Boundary `31` and `35` (+750 late fee surcharge) | Boundary `30` and `15` (no extra surcharge) |
| `card_status` | `is_frozen` | `True` returns `"frozen"` | `False` proceeds |
| `card_status` | `missed_payments >= 3` | Boundary `3` and `5` return `"blocked"` | Missed payments < 3 proceeds |
| `card_status` | `utilisation_percent > 90` | Boundary `90.1` and `95` return `"over limit risk"` | Utilisation $\le 90$ proceeds |
| `card_status` | `utilisation_percent > 30 or missed_payments > 0` | Utilisation `50` ("watch") and Missed payments `1` ("watch") | Both $\le$ threshold returns `"good"` |

---

## 5. Instructions to Run & Reproduce

### 1. Prerequisites
Ensure `pytest` and `coverage` are installed:
```bash
pip install pytest coverage
```

### 2. Measure Code Coverage
```bash
coverage erase
coverage run -m pytest CodeCoverageTest_credit_card_rewards.py
coverage report -m
```

### 3. Measure Branch Coverage
```bash
coverage erase
coverage run --branch -m pytest BranchCoverageTest_credit_card_rewards.py
coverage report -m
```

### 4. Run Unified Test Suite
```bash
coverage erase
coverage run --branch -m pytest test_credit_card_rewards.py
coverage report -m
```

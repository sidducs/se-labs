# Lab 7: Fuzzing for Input Validation Bugs — Credit Card Rewards

**Student Name:** Siddu Sanganna Shirasagi  
**SRN:** PES1UG25CS846  
**Roll / Problem ID:** 61 (Credit Card Rewards)  
**Assigned Repository:** [SETAPESU26/L6_L7_61_credit_card_rewards](https://github.com/SETAPESU26/L6_L7_61_credit_card_rewards/tree/main/LAB7)  
**Course:** Software Engineering Lab (UE23CS352A)

---

## 1. Overview & Objectives

This lab explores **property-based fuzz testing** as a dynamic security and quality assurance technique using Python's `Hypothesis` library. The primary objectives are:
1. Understand how fuzz testing feeds random, unexpected, and malformed inputs to expose hidden bugs, crashes, and edge-case vulnerabilities.
2. Formulate property-based tests using `@given(st.text() | st.none())` to stress-test module functions.
3. Identify and analyze unhandled exceptions (`AttributeError`, `IndexError`, `ValueError`) discovered by Hypothesis.
4. Harden the application functions with defensive programming so they handle any input safely without crashing.
5. Capture real terminal output screenshots (SS1 to SS4) and submit the final lab report PDF.

---

## 2. Deliverables & File Structure

```text
Lab-7/
├── Lab_7_FuzzTesting_Student_Handout.docx (1).pdf # Official lab handout manual
├── README.md                                      # Lab report & documentation
├── credit_card_rewards_parser.py                  # Fixed & hardened module (crash-proof)
├── test_credit_card_rewards_parser.py             # Completed Hypothesis fuzz testing suite
├── PES1UG25CS846_LAB7.pdf                         # Final report PDF with screenshots & reflection
└── screenshots/
    ├── SS1.png                                    # python credit_card_rewards_parser.py (buggy module)
    ├── SS2.png                                    # pytest test_credit_card_rewards_parser.py (failing on buggy)
    ├── SS3.png                                    # python credit_card_rewards_parser.py (fixed module)
    └── SS4.png                                    # pytest test_credit_card_rewards_parser.py (passing on fixed)
```

---

## 3. Bug Analysis & Discovered Falsifications (Hypothesis Fuzzing)

| Function Under Test | Buggy Assumption | Minimal Failing Input Discovered by Hypothesis | Exception Triggered |
| :--- | :--- | :--- | :--- |
| `mask_card_number(number)` | Assumed input is always a non-empty string | `s = None` | `AttributeError: 'NoneType' object has no attribute 'replace'` |
| `parse_transaction(line)` | Assumed all 3 fields (`date,category,amount`) exist and amount is an integer | 1. `s = None`<br/>2. `s = ''`<br/>3. `s = '2026-11-05,dining,abc'` | 1. `AttributeError: 'NoneType' object has no attribute 'split'`<br/>2. `IndexError: list index out of range`<br/>3. `ValueError: invalid literal for int() with base 10: 'abc'` |
| `parse_statement_total(text)` | Assumed line contains a colon followed by a valid number | 1. `s = None`<br/>2. `s = ''` (missing colon)<br/>3. `s = ':'` (empty number after colon) | 1. `AttributeError: 'NoneType' object has no attribute 'split'`<br/>2. `IndexError: list index out of range`<br/>3. `ValueError: invalid literal for int() with base 10: ''` |

---

## 4. Defensive Hardening Implementation

### 1. `mask_card_number(number)`
- Added type validation: `if not isinstance(number, str): return ""`
- Safely stripped formatting characters (` ` and `-`).
- Verified stripped length before slicing `digits[-4:]`.

### 2. `parse_transaction(line)`
- Added type validation: `if not isinstance(line, str): return None`
- Split on comma and verified token count: `if len(parts) < 3: return None`
- Extracted and normalized category (`parts[1].strip().lower()`).
- Wrapped integer amount parsing in `try...except (ValueError, TypeError): return None`.

### 3. `parse_statement_total(text)`
- Added type validation and delimiter check: `if not isinstance(text, str) or ':' not in text: return None`
- Split on first colon: `parts = text.split(':', 1)`
- Sanitized number string (`parts[1].replace(',', '').strip()`).
- Wrapped integer conversion in `try...except (ValueError, TypeError): return None`.

---

## 5. Screenshots Summary

| Screenshot | Description | Status |
| :--- | :--- | :---: |
| **SS1** | `python credit_card_rewards_parser.py` executed on the buggy module | Captured |
| **SS2** | `pytest test_credit_card_rewards_parser.py` showing Hypothesis failing tests on buggy code | Captured |
| **SS3** | `python credit_card_rewards_parser.py` executed on the fixed module | Captured |
| **SS4** | `pytest test_credit_card_rewards_parser.py` showing all Hypothesis tests passing | Captured |

---

## 6. Reflection Questions & Answers

### 1. What types of bugs does fuzz testing reveal that traditional unit testing usually misses?
**Answer:**  
Traditional unit tests only check inputs the developer thought of beforehand (the happy path and a few expected edge cases). Fuzz testing generates hundreds of unexpected, malformed, and boundary inputs automatically (such as None, empty strings, missing separators, and bad data types). This easily reveals unhandled crashes like AttributeError, IndexError, and ValueError that manual tests tend to miss.

### 2. What edge cases and malformed inputs did Hypothesis uncover in each of the three functions?
**Answer:**  
• `mask_card_number`: Failed on `s = None`, causing an AttributeError because NoneType does not have a `.replace()` method.  
• `parse_transaction`: Failed on `s = None` (AttributeError on split), empty string `s = ''` (IndexError because parts has only 1 element), and non-integer amounts like `'abc'` (ValueError on int()).  
• `parse_statement_total`: Failed on `s = None` (AttributeError), empty string or lines without a colon (IndexError on `text.split(':')[1]`), and strings like `':'` with no number after the colon (ValueError).

### 3. How did you harden the functions against invalid inputs, and what are the trade-offs between defensive parsing vs crashing?
**Answer:**  
I hardened the functions by adding `isinstance(..., str)` checks, checking list length and delimiter existence before indexing, and wrapping `int()` conversion in try-except blocks, returning `None` or `""` when input is invalid.

**Trade-offs:**  
Defensive parsing prevents unexpected crashes and keeps the service running even when users provide garbage input. However, returning fallback defaults like `None` can sometimes hide upstream bugs if the caller forgets to check the result. Raising exceptions makes bugs immediately obvious, but requires callers to add try-except blocks everywhere to prevent the program from crashing.

---

## 7. Instructions to Run & Reproduce

### 1. Prerequisites
```bash
pip install hypothesis pytest
```

### 2. Run Tests on Fixed Module
```bash
pytest test_credit_card_rewards_parser.py -q --no-header -W ignore
```

### 3. Run Interactive Parser
```bash
python credit_card_rewards_parser.py
```

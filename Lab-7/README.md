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
5. Capture real terminal output screenshots (SS1 to SS4) and generate the official lab deliverable DOCX report.

---

## 2. Deliverables & File Structure

```text
Lab-7/
├── Lab_7_FuzzTesting_Student_Handout.docx (1).pdf # Official lab handout manual
├── README.md                                      # Comprehensive lab report & documentation
├── credit_card_rewards_parser.py                  # Fixed & hardened module (crash-proof)
├── credit_card_rewards_parser_buggy.py            # Original buggy module for comparative testing
├── credit_card_rewards_parser_fixed.py            # Hardened reference module
├── test_credit_card_rewards_parser.py             # Completed Hypothesis fuzz testing suite
├── generate_lab7_docx.py                          # Automated DOCX report generator
├── PES1UG25CS846_Siddu_Shirasagi_LAB7.docx        # Final compiled submission document
├── SRN_NAME_LAB7.docx                             # Submission document alias
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
Traditional unit testing validates predictable behaviors, known paths, and developer-anticipated edge cases (e.g. testing with `"4111 1111 1111 1234"`). In contrast, property-based fuzz testing with Hypothesis generates hundreds of pseudo-random, malformed, and boundary inputs that humans rarely think to test—including `None`, empty strings `""`, missing delimiters, arbitrary Unicode characters, whitespace-only strings, negative quantities, and unformatted inputs. Fuzzing uncovers unhandled exceptions (`AttributeError`, `IndexError`, `ValueError`), injection risks, and unexpected application crashes that would otherwise escape to production.

### 2. What edge cases and malformed inputs did Hypothesis uncover in each of the three functions?
**Answer:**  
Hypothesis uncovered the following specific falsifying examples:
- **`mask_card_number`:** Failed immediately on `s = None` because `NoneType` lacks the `.replace()` method, raising an unhandled `AttributeError`.
- **`parse_transaction`:** Failed on `s = None` (`AttributeError`), empty string `s = ""` (`IndexError: list index out of range` because `parts` had only 1 element), and strings where amount is non-numeric (`ValueError`).
- **`parse_statement_total`:** Failed on `s = None` (`AttributeError`), strings without colons like `s = ""` (`IndexError` on index `[1]`), and colon-only strings `s = ":"` (`ValueError` trying to convert an empty string into an integer).

### 3. How did you harden the functions against invalid inputs, and what are the trade-offs between defensive parsing vs crashing?
**Answer:**  
The functions were hardened using:
1. **Type checking:** `isinstance(s, str)` to reject non-string/`None` inputs.
2. **Boundary and delimiter checks:** Explicitly verifying that required delimiters exist (`':' in text`) and lists have sufficient elements (`len(parts) >= 3`) before indexing.
3. **Protected type casting:** Encapsulating `int(...)` conversions inside `try...except (ValueError, TypeError)` blocks.
4. **Safe defaults:** Returning fallback values (`""` or `None`) instead of allowing unhandled exceptions.

**Trade-offs:**  
Defensive parsing increases application availability and prevents crashes from untrusted inputs. However, silently returning defaults (like `None` or `""`) can mask upstream bugs or pass empty values silently down the processing pipeline. Conversely, crashing or raising explicit custom exceptions makes bugs immediately visible to calling code, but requires every caller to implement thorough exception handling to prevent service termination.

---

## 7. Instructions to Run & Reproduce

### 1. Prerequisites
```bash
pip install hypothesis pytest python-docx
```

### 2. Run Tests on Fixed Module
```bash
pytest test_credit_card_rewards_parser.py -q --no-header -W ignore
```

### 3. Run Interactive Parser
```bash
python credit_card_rewards_parser.py
```

### 4. Regenerate Submission DOCX
```bash
python generate_lab7_docx.py
```

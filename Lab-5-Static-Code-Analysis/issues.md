# Static Analysis Issue Log

The baseline reports are preserved in `pylint_before.txt`, `bandit_before.txt`, and `flake8_before.txt`. The after reports are `pylint_after.txt`, `bandit_after.txt`, and `flake8_after.txt`.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| Weak MD5 voter identifier | Security, high | 17 | Bandit B324 identified MD5 as unsuitable for security-sensitive hashing. | Replaced MD5 with SHA-256. |
| Trojan Source control character | Security, high | 22 | Bandit B613 and Pylint E2502 identified bidirectional Unicode controls that obscured the officer check. | Removed the hidden characters and implemented an explicit `election_officer` role comparison. |
| Unsafe XML parsing | Security, medium/low | 7, 75 | Bandit B409 and B319 identified `pulldom` as unsafe for untrusted XML. | Replaced it with `defusedxml.ElementTree` and return zero for malformed XML. |
| Hardcoded administrator password | Security, low | 9 | Bandit B105 found a password literal embedded in source code. It was unused and created an unnecessary secret exposure. | Removed the unused password constant. |
| Insecure receipt randomness | Security, low | 72 | Bandit B311 identified the non-cryptographic `random` generator. | Replaced it with `secrets.randbelow`. |
| Bare exception handler | Reliability/style, low | 82-83 | Pylint W0702, Flake8 E722, and Bandit B110 found `except: pass`, which hid parsing failures. | Catch XML parse/value errors explicitly and return zero for invalid input. |
| Duplicate and invalid votes accepted | Logic bug | 26-34 | A voter could vote repeatedly, unknown candidates were added, and late votes were accepted at the closing hour. | Check voter status, candidate membership, and the closing-hour boundary before appending. |
| Empty totals could divide by zero | Logic bug | 51-56 | `votePercent` and `turnout` failed when there were no ballots or voters. | Return zero for empty denominators. |
| Announcement closure captured the final candidate | Logic bug | 65-69 | Each lambda captured the loop variable late, so every announcement used the last candidate. | Build announcements directly from the tally with a list comprehension. |
| Pylint/Flake8 quality findings | Quality/style | 1-104 | Reports identified unused imports/variables, missing docstrings, non-snake-case names, long lines, trailing whitespace, and a redefined parameter. | Removed unused code, renamed functions, added concise docstrings, and formatted the module consistently. |

## Verification

- Pylint after: **10.00/10**.
- Bandit after: **No issues identified**, with zero skipped findings.
- Flake8 after: **No output**, meaning no violations remain.
- Focused behavior checks passed for invalid candidates, repeated voting, empty totals, safe XML parsing, and announcements.

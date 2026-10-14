# Reflection

## 1. What is the purpose of static code analysis?

Static analysis examines source code without executing it to identify defects, security risks, maintainability problems, and style violations early. It is useful because it gives repeatable feedback before code reaches production or a reviewer has to discover the same issue manually.

## 2. How did Pylint, Bandit, and Flake8 differ?

Pylint provided the broadest review: naming, missing documentation, unused code, suspicious logic, and code structure. Bandit focused on security patterns such as MD5, hardcoded secrets, unsafe XML parsing, weak randomness, broad exception handling, and hidden bidirectional characters. Flake8 was narrower and fast, concentrating on imports, whitespace, line length, blank lines, and syntax-related style rules. Running all three was more useful than relying on one tool because their findings overlapped only partially.

## 3. Which finding was most important, and how was it fixed?

The highest-priority findings were the weak MD5 hash and the Trojan Source bidirectional control character. MD5 is not appropriate for security-sensitive data, so it was replaced with SHA-256. The hidden control character could make the officer check appear different from what Python executes, so it was removed and replaced with a clear role comparison. Unsafe XML parsing was also replaced with `defusedxml` because postal-ballot XML is external input.

## 4. What did you learn from this exercise?

Tool output must be interpreted against actual behavior. The tools found security and quality problems, but targeted execution also exposed duplicate voting, invalid candidates, late voting, empty-total division, and the lambda closure bug. The strongest workflow was to preserve the baseline reports, make focused fixes, rerun every analyzer, and then test the edge cases that static analysis could not fully prove.

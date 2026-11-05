def mask_card_number(number):
    """
    Hides all but the last four digits of a card number.
    Handles any input safely without crashing.
    """
    if not isinstance(number, str):
        return ""
    digits = number.replace(' ', '').replace('-', '')
    if not digits:
        return ""
    return '*' * 12 + digits[-4:]


def parse_transaction(line):
    """
    Parses 'date,category,amount' into a (category, amount) tuple.
    Handles any input safely without crashing. Returns None if invalid.
    """
    if not isinstance(line, str):
        return None
    parts = line.split(',')
    if len(parts) < 3:
        return None
    category = parts[1].strip().lower()
    amount_str = parts[2].strip()
    try:
        return category, int(amount_str)
    except (ValueError, TypeError):
        return None


def parse_statement_total(text):
    """
    Reads the amount from a line such as 'Total: 12,500'.
    Handles any input safely without crashing. Returns None if invalid.
    """
    if not isinstance(text, str) or ':' not in text:
        return None
    parts = text.split(':', 1)
    amount_str = parts[1].replace(',', '').strip()
    try:
        return int(amount_str)
    except (ValueError, TypeError):
        return None


def main():
    value = input("Enter a card number (e.g. 4111 1111 1111 1234): ")
    print("Masked card number:", mask_card_number(value))

    value = input("Enter a transaction as DATE,CATEGORY,AMOUNT (e.g. 2026-11-05,dining,1550): ")
    print("Category and amount:", parse_transaction(value))

    value = input("Enter the statement total line (e.g. Total: 12,500): ")
    print("Statement total:", parse_statement_total(value))


if __name__ == "__main__":
    main()

def mask_card_number(number):
    """
    Hides all but the last four digits of a card number.
    Assumes number is a non-empty string.
    """
    digits = number.replace(' ', '').replace('-', '')
    return '*' * 12 + digits[-4:]

def parse_transaction(line):
    """
    Parses 'date,category,amount' into a (category, amount) tuple.
    Assumes all three fields are present and amount is a whole number.
    """
    parts = line.split(',')
    return parts[1].strip().lower(), int(parts[2])

def parse_statement_total(text):
    """
    Reads the amount from a line such as 'Total: 12,500'.
    Assumes the line has a colon followed by a number.
    """
    amount = text.split(':')[1]
    return int(amount.replace(',', ''))

def main():
    value = input("Enter a card number (e.g. 4111 1111 1111 1234): ")
    print("Masked card number:", mask_card_number(value))

    value = input("Enter a transaction as DATE,CATEGORY,AMOUNT (e.g. 2026-11-05,dining,1550): ")
    print("Category and amount:", parse_transaction(value))

    value = input("Enter the statement total line (e.g. Total: 12,500): ")
    print("Statement total:", parse_statement_total(value))

if __name__ == "__main__":
    main()

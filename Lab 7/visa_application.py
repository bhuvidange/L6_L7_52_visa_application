import math


def parse_application(text):
    """Parse 'visa_type:entries' (e.g. 'tourist:2').

    Returns (Visa Type, entries) or None if the input is invalid.
    """
    if not isinstance(text, str):
        return None
    parts = text.split(':')
    if len(parts) != 2:                      # missing or extra ':'
        return None
    visa, entries = parts[0].strip(), parts[1].strip()
    if not visa:                             # empty visa type
        return None
    try:
        entries = int(entries)
    except ValueError:                       # non-numeric / empty / too long
        return None
    if entries < 0:                          # negative entries make no sense
        return None
    return visa.title(), entries


def processing_average(days_csv):
    """Average (integer division) of comma separated processing days.

    Returns None if the input is invalid.
    """
    if not isinstance(days_csv, str):
        return None
    try:
        values = [int(r.strip()) for r in days_csv.split(',')]
    except ValueError:                       # empty element or non-numeric
        return None
    if not values or any(v < 0 for v in values):
        return None
    return sum(values) // len(values)


def payable_fee(text):
    """Compute fee * 1.18 (GST) minus discount, never below zero.

    Input format 'fee|discount'. Returns None if the input is invalid.
    """
    if not isinstance(text, str):
        return None
    parts = text.split('|')
    if len(parts) != 2:                      # missing or extra '|'
        return None
    try:
        fee, discount = float(parts[0]), float(parts[1])
    except ValueError:
        return None
    if not (math.isfinite(fee) and math.isfinite(discount)):   # nan / inf
        return None
    if fee < 0 or discount < 0:
        return None
    total = fee * 1.18 - discount
    if not math.isfinite(total):             # overflow, e.g. 1e308 * 1.18
        return None
    return max(total, 0)


def main():
    print("==== Running parse_application ====")
    user_input = input("Enter visa type:entries (e.g. tourist:2): ")
    result = parse_application(user_input)
    print("Visa Type and Entries:", result)

    print("\n==== Running processing_average ====")
    user_input = input("Enter processing days as CSV (e.g. 5,10,21): ")
    result = processing_average(user_input)
    print("Average Processing Days:", result)

    print("\n==== Running payable_fee ====")
    user_input = input("Enter fee|discount (e.g. 6000|500): ")
    result = payable_fee(user_input)
    print("Payable Fee:", result)


if __name__ == "__main__":
    main()

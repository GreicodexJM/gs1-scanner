from data_extractors import (
    validate_gtin,
    parse_sscc,
    parse_expiration_or_best_before_date,
    parse_batch_or_serial_number,
    parse_weight_or_amount
)

def parse_code(ai, value, ai_dictionary):
    """
    Main function to route parsing to appropriate functions based on AI.
    Handles AIs with variable decimal precision (e.g., 310x, 311x).
    """
    ai_prefix = ai[:3]  # Get the first 3 characters of the AI to determine the type

    # Look up the parsing function based on AI in the dictionary
    if ai in ai_dictionary:
        interpretation = ai_dictionary[ai]
    elif f"{ai_prefix}x" in ai_dictionary:
        interpretation = ai_dictionary[ai_prefix]
    else:
        return {
            "error": True,
            "message": f"Unknown AI {ai}"
        }

    # Route to the appropriate parsing function
    if ai == '01':
        return validate_gtin(value)
    elif ai == '00':
        return parse_sscc(value)
    elif ai in ['17', '15']:
        date_type = interpretation
        return parse_expiration_or_best_before_date(value, date_type)
    elif ai in ['10', '21']:
        code_type = interpretation
        return parse_batch_or_serial_number(value, code_type)
    elif ai_dictionary[f"{ai_prefix}x"]:
        # Extract decimal precision from the last digit of the AI (e.g., 3102 => 2 decimal places)
        decimal_precision = int(ai[3])
        return parse_weight_or_amount(value, interpretation, decimal_precision)
    else:
        return {
            "error": True,
            "message": f"Unsupported AI {ai}"
        }

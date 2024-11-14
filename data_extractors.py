from gs1_constants import GS1_PREFIX_COUNTRIES

def calculate_check_digit(number):
    """Calculate and return the expected check digit using the GS1 Modulus-10 algorithm."""
    number_reversed = list(map(int, number[:-1][::-1]))
    total = sum(number_reversed[i] * (3 if i % 2 == 0 else 1) for i in range(len(number_reversed)))
    return (10 - (total % 10)) % 10

def get_country_from_prefix(company_prefix):
    """
    Returns the country based on the company prefix, accounting for ranges in GS1_PREFIX_COUNTRIES.
    """
    for prefix_range, country in GS1_PREFIX_COUNTRIES.items():
        if '-' in prefix_range:
            # Handle prefix ranges like '000-019'
            start, end = prefix_range.split('-')
            if start <= company_prefix[:len(start)] <= end:
                return country
        else:
            # Handle single prefix like '560'
            if company_prefix.startswith(prefix_range):
                return country
    return "Unknown Country"

def validate_gtin(gtin):
    """Validates and parses the GTIN, including check digit and company prefix country."""
    if len(gtin) not in [8, 12, 13, 14]:
        return {"error": True, "message": "Longitud de GTIN no válida"}

    expected_check_digit = calculate_check_digit(gtin)
    if int(gtin[-1]) != expected_check_digit:
        return {"error": True, "message": f"Dígito de control no válido (esperado {expected_check_digit}, obtubo {gtin[-1]})"}

    company_prefix = gtin[1:7] if len(gtin) == 14 else gtin[:7] if len(gtin) == 13 else gtin[:6]
    fields = {
        "Tipo GTIN": f"GTIN-{len(gtin)}",
        "Prefijo de la empresa": company_prefix,
        "Referencia del artículo": gtin[7:13] if len(gtin) >= 13 else gtin[6:11],
        "Dígito de control": gtin[-1],
        "País": get_country_from_prefix(company_prefix)
    }
    return {"error": False, "type": "GTIN", "fields": fields}

def parse_sscc(sscc):
    """Parses and validates SSCC, including check digit and company prefix country."""
    if len(sscc) != 18:
        return {"error": True, "message": "Longitud SSCC no válida"}

    expected_check_digit = calculate_check_digit(sscc)
    if int(sscc[-1]) != expected_check_digit:
        return {"error": True, "message": f"Dígito de control SSCC no válido (esperado {expected_check_digit}, obtubo {sscc[-1]})"}

    company_prefix = sscc[1:8]
    fields = {
        "Tipo SSCC": "SSCC-18",
        "Prefijo de la empresa": company_prefix,
        "Numero secuencia": sscc[8:17],
        "Dígito de control": sscc[-1],
        "País": get_country_from_prefix(company_prefix)
    }
    return {"error": False, "type": "SSCC", "fields": fields}

def parse_expiration_or_best_before_date(value, date_type):
    """Parses expiration or best before date."""
    if len(value) != 6:
        return {"error": True, "message": "Longitud de fecha no válida"}

    year = "20" + value[0:2]
    month = value[2:4]
    day = value[4:6]
    return {"error": False, "type": date_type, "fields": {"Date": f"{year}-{month}-{day}"}}

def parse_batch_or_serial_number(value, code_type):
    """Parses batch or lot numbers and serial numbers."""
    return {"error": False, "type": code_type, "fields": {f"{code_type}": value}}

def parse_weight_or_amount(value, code_type, decimal_places):
    """Parses net weight or monetary amount based on decimal precision."""
    if len(value) < 1:
        return {"error": True, "message": f"Codigo Inválido {code_type}"}

    integer_part = value[:-decimal_places] if decimal_places else value
    decimal_part = value[-decimal_places:] if decimal_places else ""
    formatted_value = f"{integer_part}.{decimal_part}" if decimal_places else integer_part

    return {"error": False, "type": code_type, "fields": {code_type: formatted_value}}

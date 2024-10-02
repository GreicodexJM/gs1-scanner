### **GS1 Barcode Parsing API Documentation**

This document describes the GS1 Barcode Parsing API, which can be accessed via the following Lambda URL:

**API URL**:  
`https://qtou4ilcqnjqovtgsznztbfkku0dipui.lambda-url.us-west-2.on.aws/`

---

### **Overview**

The GS1 Barcode Parsing API allows users to submit GS1-compliant barcodes for validation and parsing. It identifies various **Application Identifiers (AIs)** such as Global Trade Item Number (GTIN), Serial Shipping Container Code (SSCC), expiration dates, and more. The API extracts the relevant information, validates check digits, and returns the parsed data.

---

### **Supported Application Identifiers (AIs)**

- **GTIN** (`01`): Global Trade Item Number (supports GTIN-8, GTIN-12, GTIN-13, GTIN-14)
- **SSCC** (`00`): Serial Shipping Container Code
- **Expiration Date** (`17`): Date in YYMMDD format
- **Best Before Date** (`15`): Date in YYMMDD format
- **Batch/Lot Number** (`10`): Variable-length alphanumeric
- **Serial Number** (`21`): Variable-length alphanumeric
- **Net Weight** (`310n`): Net weight in kilograms, where `n` specifies the decimal point position
- **Monetary Amount** (`392n`): Monetary amount, where `n` specifies the decimal point position

---

### **Request Format**

The API accepts POST requests with a JSON payload containing the barcode string to be parsed. The barcode string must follow the GS1 format, where each Application Identifier (AI) is enclosed in parentheses.

#### **Request URL**

`POST https://qtou4ilcqnjqovtgsznztbfkku0dipui.lambda-url.us-west-2.on.aws/`

#### **Request Body**

The request body must be a JSON object with the following structure:

```json
{
    "gs1_barcode": "(AI1)Value1(AI2)Value2..."
}
```

- **gs1_barcode** (string): The GS1-compliant barcode string, where each part of the barcode starts with a GS1 Application Identifier (AI) enclosed in parentheses, followed by the value.

#### **Example Request**

```json
{
    "gs1_barcode": "(01)09507000193146(17)250101(10)AB1234(00)123456789012345678"
}
```

---

### **Response Format**

The API responds with a JSON object containing the parsed information or an error message if validation fails. The response has the following structure:

#### **Response Structure**

```json
{
    "error": false,
    "result": [
        {
            "type": "GTIN",
            "fields": {
                "GTIN Type": "GTIN-14",
                "Company Prefix": "095070",
                "Item Reference": "001931",
                "Check Digit": "6",
                "Country": "GS1 Global Office"
            }
        },
        {
            "type": "Expiration Date",
            "fields": {
                "Date": "2025-01-01"
            }
        },
        {
            "type": "Batch or Lot Number",
            "fields": {
                "Batch/Lot Number": "AB1234"
            }
        },
        {
            "type": "SSCC",
            "fields": {
                "SSCC Type": "SSCC-18",
                "Company Prefix": "1234567",
                "Serial Reference": "890123456",
                "Check Digit": "8",
                "Country": "Unknown Country"
            }
        }
    ]
}
```

#### **Response Fields**

- **error** (boolean): Indicates whether an error occurred during parsing.
- **result** (array): Contains one or more objects representing the parsed components of the barcode.

Each object in the `result` array contains:
- **type** (string): The type of the parsed component (e.g., `GTIN`, `SSCC`, `Expiration Date`, etc.).
- **fields** (object): Key-value pairs of the parsed data fields for the corresponding type.

---

### **Error Responses**

If the barcode is invalid or an error occurs during parsing, the API responds with an error message. The error response includes:

```json
{
    "error": true,
    "message": "Error message"
}
```

#### **Common Error Messages**
- `"Invalid GTIN length"`: The GTIN does not have the correct length.
- `"Invalid Check Digit"`: The check digit for a GTIN or SSCC is incorrect.
- `"Invalid Date Length"`: The date for an expiration or best-before AI is not in the correct YYMMDD format.
- `"Unsupported AI {AI}"`: The API encountered an unsupported or unrecognized Application Identifier (AI).
- `"No GS1 barcode provided"`: The request does not include the `gs1_barcode` field.

---

### **Examples**

#### **Example 1: Valid Request**

**Request**:
```json
{
    "gs1_barcode": "(01)12345678901231(17)251231(21)12345"
}
```

**Response**:
```json
{
    "error": false,
    "result": [
        {
            "type": "GTIN",
            "fields": {
                "GTIN Type": "GTIN-14",
                "Company Prefix": "123456",
                "Item Reference": "789012",
                "Check Digit": "1",
                "Country": "Unknown Country"
            }
        },
        {
            "type": "Expiration Date",
            "fields": {
                "Date": "2025-12-31"
            }
        },
        {
            "type": "Serial Number",
            "fields": {
                "Serial Number": "12345"
            }
        }
    ]
}
```

#### **Example 2: Error Response**

**Request**:
```json
{
    "gs1_barcode": "(01)0950700019314(17)250101(10)AB1234"
}
```

**Response**:
```json
{
    "error": true,
    "message": "Invalid GTIN length"
}
```

---

### **Testing Scenarios**

#### **1. Invalid GTIN Length**
- **Test Case**: `(01)0950700019314(17)250101`
- **Expected Response**: Error, "Invalid GTIN length"

#### **2. Invalid Check Digit**
- **Test Case**: `(01)12345678901231(17)251231`
- **Expected Response**: If the GTIN check digit is incorrect, expect an error message indicating invalid check digit.

#### **3. Valid SSCC and Expiration Date**
- **Test Case**: `(00)00370009908888(17)251231`
- **Expected Response**: Parsed SSCC and Expiration Date.

---

### **Conclusion**

This API enables efficient parsing of GS1-compliant barcodes, returning structured data for recognized AIs. It handles common GS1 fields like GTIN, SSCC, dates, and more, with proper validation, including check digit verification.
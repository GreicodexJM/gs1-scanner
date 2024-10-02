import json
from parsers import parse_code
from gs1_constants import GS1_AIs

def lambda_handler(event, context):
    if event.get('body') :
        body = json.loads(event.get('body'))
        gs1_barcode = body['gs1_barcode']
    else:
        gs1_barcode = event.get('gs1_barcode', '')

    if not gs1_barcode:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': True, 'message': 'No GS1 barcode provided.'})
        }

    parsed_data = {}
    current_ai = ''
    output = {
        "error": False,
        "result": []
    }

    # Parsing GS1 barcode
    index = 0
    while index < len(gs1_barcode):
        if gs1_barcode[index] == '(':
            end_ai_index = gs1_barcode.find(')', index)
            current_ai = gs1_barcode[index+1:end_ai_index]
            index = end_ai_index + 1
        else:
            if current_ai not in parsed_data:
                parsed_data[current_ai] = ''
            parsed_data[current_ai] += gs1_barcode[index]
            index += 1

    # Process each AI using the parsing rules
    for ai, value in parsed_data.items():
        result = parse_code(ai, value, GS1_AIs)
        output["result"].append(result)

    return {
        'statusCode': 200,
        'body': json.dumps(output)
    }

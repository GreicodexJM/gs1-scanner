#!/bin/bash

# Variables
LAMBDA_NAME="GS1BarcodeParserLambda"
ROLE_ARN="arn:aws:iam::your-account-id:role/your-lambda-role" # Replace with your role ARN
REGION="us-west-2"
HANDLER="lambda_function.lambda_handler"
RUNTIME="python3.9"
ZIP_FILE="lambda_function.zip"
TIMEOUT=15
MEMORY_SIZE=128

# Create a ZIP of the function code
echo "Zipping function code..."
zip -r9 ${ZIP_FILE} lambda_function.py parsers.py data_extractors.py gs1_constants.py

# Create the Lambda function
echo "Creating Lambda function..."
aws lambda create-function --function-name $LAMBDA_NAME \
--zip-file fileb://$ZIP_FILE \
--handler $HANDLER \
--runtime $RUNTIME \
--role $ROLE_ARN \
--timeout $TIMEOUT \
--memory-size $MEMORY_SIZE \
--region $REGION

# Update the Lambda function if it already exists
echo "Updating Lambda function..."
aws lambda update-function-code --function-name $LAMBDA_NAME \
--zip-file fileb://$ZIP_FILE \
--region $REGION

echo "Deployment complete!"

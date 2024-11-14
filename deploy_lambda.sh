#!/bin/bash

# Variables
LAMBDA_NAME="gs1-barcode-parser"
ROLE_ARN="arn:aws:iam::724451974334:role/gs1-barcode-parser-role-jhtrdu65" # Replace with your role ARN
REGION="us-west-2"
HANDLER="lambda_function.lambda_handler"
RUNTIME="python3.9"
ZIP_FILE="lambda_function.zip"
TIMEOUT=15
MEMORY_SIZE=128
PROFILE="greicodex"

# ANSI colors
GREEN="\033[1;32m"
YELLOW="\033[1;33m"
BLUE="\033[1;34m"
RED="\033[1;31m"
NC="\033[0m" # No Color

# Unicode emojis
ZIP_EMOJI="📦"
CREATE_EMOJI="🚀"
UPDATE_EMOJI="🔄"
CHECK_EMOJI="🔍"
DONE_EMOJI="✅"
ERROR_EMOJI="❌"

# Logging functions
function log_info() {
    echo -e "${BLUE}${1} ${2}${NC}"
}

function log_success() {
    echo -e "${GREEN}${1} ${2}${NC}"
}

function log_warning() {
    echo -e "${YELLOW}${1} ${2}${NC}"
}

function log_error() {
    echo -e "${RED}${1} ${2}${NC}"
}

# Function to create a ZIP of the Lambda function code
function zip_code() {
    log_info "${ZIP_EMOJI}" "Zipping function code..."
    zip -r9 ${ZIP_FILE} lambda_function.py parsers.py data_extractors.py gs1_constants.py gs1_constants_es.py
    if [ $? -eq 0 ]; then
        log_success "${DONE_EMOJI}" "Zipping completed successfully."
    else
        log_error "${ERROR_EMOJI}" "Error in zipping files."
        exit 1
    fi
}

# Function to check if the Lambda function exists
function lambda_exists() {
    log_info "${CHECK_EMOJI}" "Checking if Lambda function ${LAMBDA_NAME} exists..."
    aws lambda get-function --function-name $LAMBDA_NAME --region $REGION --profile $PROFILE > /dev/null 2>&1
    return $?
}

# Function to create the Lambda function
function create_lambda() {
    log_info "${CREATE_EMOJI}" "Creating Lambda function ${LAMBDA_NAME}..."
    aws lambda create-function \
        --function-name $LAMBDA_NAME \
        --zip-file fileb://$ZIP_FILE \
        --handler $HANDLER \
        --runtime $RUNTIME \
        --role $ROLE_ARN \
        --timeout $TIMEOUT \
        --memory-size $MEMORY_SIZE \
        --region $REGION \
        --profile $PROFILE
    if [ $? -eq 0 ]; then
        log_success "${DONE_EMOJI}" "Lambda function ${LAMBDA_NAME} created successfully."
    else
        log_error "${ERROR_EMOJI}" "Failed to create Lambda function ${LAMBDA_NAME}."
        exit 1
    fi
}

# Function to update the Lambda function code
function update_lambda() {
    log_info "${UPDATE_EMOJI}" "Updating Lambda function ${LAMBDA_NAME}..."
    aws lambda update-function-code \
        --function-name $LAMBDA_NAME \
        --zip-file fileb://$ZIP_FILE \
        --region $REGION \
        --profile $PROFILE
    if [ $? -eq 0 ]; then
        log_success "${DONE_EMOJI}" "Lambda function ${LAMBDA_NAME} updated successfully."
    else
        log_error "${ERROR_EMOJI}" "Failed to update Lambda function ${LAMBDA_NAME}."
        exit 1
    fi
}

# Main deployment logic
zip_code

if lambda_exists; then
    log_warning "${CHECK_EMOJI}" "Lambda function ${LAMBDA_NAME} exists. Updating..."
    update_lambda
else
    log_warning "${CHECK_EMOJI}" "Lambda function ${LAMBDA_NAME} does not exist. Creating..."
    create_lambda
fi

log_success "${DONE_EMOJI}" "Deployment complete!"

import replicate
import os
from config import REPLICATE_API_TOKEN

# Assuming you've set your Replicate API key in your environment variables
replicate.api_token = os.getenv(REPLICATE_API_TOKEN)

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
print("REPLICATE_API_TOKEN:", REPLICATE_API_TOKEN)

if REPLICATE_API_TOKEN is None:
    raise ValueError(
        "Replicate API token is not set in environment variables.")

text = ''' Transfer Funds

saction witn rererenc

Payee
DR DISTRIBUTOR
A/C No.0712866012

Name IFSC

DR DISTRIBUTOR CITIOOO0002
Bank Branch

CIT] BANK NEW DELHI
Debit Account Transfer Amount

918020054889899 13894.00

Payment Type Transaction Date
One-time 28-02-2024
Payment Via Remarks

NEFT JAIN PHARMACY
'''
# Define your JSON template as a string to improve readability in the prompt
JSON_SYNTAX = '''{
    "transaction_id": "Read transaction ID from the message it may be bank ref id, transaction id, reference no or similar texts",
    "sender_name": "Read sender name",
    "receiver_name": "Read receiver name",
    "sender_number": "Read sender number",
    "receiver_number": "Read receiver number",
    "timestamp": "Read timestamp from the text Format(YYYY-MM-DD HH:MM:SS)",
    "transaction_amount": "Read Transaction Amount from the text"
}'''


def generate_json_from_text(text):
    prompt = f"""Please read the below text carefully and generate a JSON object based on the following structure oNLY RETURBN json and do not return any irrelevant text:
    {JSON_SYNTAX}
    Based on this text:
    {text}
    """

    print(prompt)

    # Replace the model with the name of the model you want to use
    model = "meta/llama-2-13b-chat"

    # Run the model and get the prediction
    prediction = replicate.run(model, input={"prompt": prompt,
                                             "max_new_tokens": 500,
                                             "min_new_tokens": -1,
                                             "temperature": 0.5,
                                             "top_p": 0.01,
                                             "repetition_penalty": 1.15,
                                             "top_k": 50, })
    prediction_string = ''.join(prediction[0:])
    lines = prediction_string.split('\n')
    final_json = '\n'.join(lines[1:])


    print("*"*50)
    # Print the prediction
    print(final_json)
    print("*"*50)

# Example usage
generated_json = generate_json_from_text(text)
print(generated_json)
